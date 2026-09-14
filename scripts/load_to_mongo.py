"""Load the 3 source CSVs in data/raw/ into MongoDB staging_db, using pymongo.

Requires: pip install -r requirements.txt
Reads connection details from .env (MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD,
MONGO_STAGING_DB).

Each CSV is loaded as a full refresh: the target collection is dropped and re-inserted from
scratch.
"""

import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        return list(reader)


def main() -> None:
    load_dotenv(REPO_ROOT / ".env")

    client = MongoClient(
        host=os.environ["MONGO_HOST"],
        port=int(os.environ["MONGO_PORT"]),
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
    )
    db = client[os.environ["MONGO_STAGING_DB"]]

    csv_paths = sorted(RAW_DIR.glob("*.csv"))
    for csv_path in csv_paths:
        collection_name = csv_path.stem
        rows = load_csv(csv_path)
        print(f"Loading {csv_path.name} -> {collection_name} ({len(rows)} rows)")

        db[collection_name].drop()
        if rows:
            db[collection_name].insert_many(rows)

    print(f"Done. Loaded {len(csv_paths)} collection(s) into "
          f"{os.environ['MONGO_STAGING_DB']}.")


if __name__ == "__main__":
    main()
