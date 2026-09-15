import time
from unittest.mock import MagicMock

import pytest

from pipeline import trino_utils


def test_run_sql_file_strips_comments_and_splits_statements(tmp_path):
    sql_path = tmp_path / "00_create_schema.sql"
    sql_path.write_text(
        "-- comment line, ignored\n"
        "CREATE SCHEMA IF NOT EXISTS mongodb.dwh_db;\n"
        "-- another comment\n"
        "DROP TABLE IF EXISTS mongodb.dwh_db.dim_cabang;\n"
        "CREATE TABLE mongodb.dwh_db.dim_cabang AS SELECT 1;\n",
        encoding="utf-8",
    )
    cursor = MagicMock()

    trino_utils.run_sql_file(cursor, sql_path)

    executed = [call.args[0] for call in cursor.execute.call_args_list]
    assert executed == [
        "CREATE SCHEMA IF NOT EXISTS mongodb.dwh_db",
        "DROP TABLE IF EXISTS mongodb.dwh_db.dim_cabang",
        "CREATE TABLE mongodb.dwh_db.dim_cabang AS SELECT 1",
    ]
    assert cursor.fetchall.call_count == 3


def test_run_sql_file_skips_comment_only_and_blank_statements(tmp_path):
    sql_path = tmp_path / "noop.sql"
    sql_path.write_text(";;  ;\n-- only comments\n", encoding="utf-8")
    cursor = MagicMock()

    trino_utils.run_sql_file(cursor, sql_path)

    cursor.execute.assert_not_called()


def test_wait_for_trino_returns_once_query_succeeds():
    conn = MagicMock()

    trino_utils.wait_for_trino(conn)

    conn.cursor.return_value.execute.assert_called_once_with("SELECT 1")


def test_wait_for_trino_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.execute.side_effect = [Exception("not ready"), Exception("not ready"), None]

    trino_utils.wait_for_trino(conn)

    assert cursor.execute.call_count == 3


def test_wait_for_trino_raises_after_exhausting_retries(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda seconds: None)
    monkeypatch.setattr(trino_utils, "CONNECT_RETRIES", 3)
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.execute.side_effect = Exception("still not ready")

    with pytest.raises(Exception, match="still not ready"):
        trino_utils.wait_for_trino(conn)

    assert cursor.execute.call_count == 3


def test_run_transform_dir_raises_when_no_sql_files(tmp_path, monkeypatch):
    monkeypatch.setattr(trino_utils, "connect", lambda: MagicMock())
    monkeypatch.setattr(trino_utils, "wait_for_trino", lambda conn: None)

    with pytest.raises(SystemExit):
        trino_utils.run_transform_dir(tmp_path)
