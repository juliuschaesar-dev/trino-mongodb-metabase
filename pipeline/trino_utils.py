"""Shared Trino connection + SQL execution helpers, used by datawarehouse.py and datamart.py.

Reads connection details from .env (TRINO_HOST, TRINO_PORT, TRINO_CATALOG, TRINO_USER).
"""

import os
import time
from pathlib import Path

import trino
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

CONNECT_RETRIES = 30
CONNECT_RETRY_DELAY_SECONDS = 2


def connect():
    load_dotenv(REPO_ROOT / ".env")
    return trino.dbapi.connect(
        host=os.environ["TRINO_HOST"],
        port=int(os.environ["TRINO_PORT"]),
        user=os.environ["TRINO_USER"],
        catalog=os.environ["TRINO_CATALOG"],
    )


def wait_for_trino(conn) -> None:
    cursor = conn.cursor()
    for attempt in range(1, CONNECT_RETRIES + 1):
        try:
            cursor.execute("SELECT 1")
            cursor.fetchall()
            return
        except Exception as exc:  # Trino not ready yet (still starting up)
            if attempt == CONNECT_RETRIES:
                raise
            print(f"Waiting for Trino ({attempt}/{CONNECT_RETRIES}): {exc}")
            time.sleep(CONNECT_RETRY_DELAY_SECONDS)


def run_sql_file(cursor, path: Path) -> None:
    lines = [
        line for line in path.read_text(encoding="utf-8").splitlines()
        if not line.strip().startswith("--")
    ]
    sql = "\n".join(lines)
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for statement in statements:
        print(f"  -> {statement.splitlines()[0][:80]}...")
        cursor.execute(statement)
        cursor.fetchall()


def run_transform_dir(transform_dir: Path) -> None:
    """Connect to Trino and run every .sql file in transform_dir, in numeric-prefix order."""
    conn = connect()
    wait_for_trino(conn)
    cursor = conn.cursor()

    sql_files = sorted(transform_dir.glob("*.sql"))
    if not sql_files:
        raise SystemExit(f"No .sql files found in {transform_dir}")

    for path in sql_files:
        print(f"Running {path.name}")
        run_sql_file(cursor, path)

    print(f"Done. Ran {len(sql_files)} transform file(s) from {transform_dir.name}/.")
