"""Smoke tests for the real trino/transform/*.sql files: no live Trino needed, just verifies
that every file still splits into valid statements and points at the right schemas for its layer.
"""

from unittest.mock import MagicMock

from pipeline.trino_utils import REPO_ROOT, run_sql_file

DATAWAREHOUSE_DIR = REPO_ROOT / "trino" / "transform" / "datawarehouse"
DATAMART_DIR = REPO_ROOT / "trino" / "transform" / "datamart"


def _executed_sql(transform_dir) -> str:
    cursor = MagicMock()
    for path in sorted(transform_dir.glob("*.sql")):
        run_sql_file(cursor, path)
    return "\n".join(call.args[0] for call in cursor.execute.call_args_list)


def test_datawarehouse_files_exist_in_numeric_order():
    files = sorted(p.name for p in DATAWAREHOUSE_DIR.glob("*.sql"))
    assert files == [
        "00_create_schema.sql",
        "01_dim_cabang.sql",
        "02_dim_produk.sql",
        "03_fact_penjualan.sql",
    ]


def test_datamart_files_exist_in_numeric_order():
    files = sorted(p.name for p in DATAMART_DIR.glob("*.sql"))
    assert files == [
        "00_create_schema.sql",
        "01_dm_penjualan_harian.sql",
        "02_dm_penjualan_per_cabang.sql",
        "03_dm_penjualan_per_kategori.sql",
        "04_dm_penjualan_per_produk.sql",
    ]


def test_datawarehouse_sql_reads_stg_db_and_writes_dwh_db():
    executed = _executed_sql(DATAWAREHOUSE_DIR)

    assert "mongodb.stg_db." in executed
    assert "mongodb.dwh_db." in executed
    assert "mongodb.dm_db." not in executed


def test_datamart_sql_reads_dwh_db_and_writes_dm_db():
    executed = _executed_sql(DATAMART_DIR)

    assert "mongodb.dwh_db." in executed
    assert "mongodb.dm_db." in executed
    assert "mongodb.stg_db." not in executed
