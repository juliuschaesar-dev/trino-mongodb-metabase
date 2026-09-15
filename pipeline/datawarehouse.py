"""Build the datawarehouse layer (dwh_db): runs every .sql file in
trino/transform/datawarehouse/, in numeric-prefix order. Reads stg_db, writes dim_/fact_ tables.

Requires: pip install -r requirements.txt
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.trino_utils import run_transform_dir  # noqa: E402

TRANSFORM_DIR = REPO_ROOT / "trino" / "transform" / "datawarehouse"


def main() -> None:
    run_transform_dir(TRANSFORM_DIR)


if __name__ == "__main__":
    main()
