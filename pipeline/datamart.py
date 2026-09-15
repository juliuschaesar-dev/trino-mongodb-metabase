"""Build the datamart layer (dm_db): runs every .sql file in trino/transform/datamart/, in
numeric-prefix order. Reads dwh_db (dim_/fact_ tables), writes dm_ tables.

Requires: pip install -r requirements.txt
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline.trino_utils import run_transform_dir  # noqa: E402

TRANSFORM_DIR = REPO_ROOT / "trino" / "transform" / "datamart"


def main() -> None:
    run_transform_dir(TRANSFORM_DIR)


if __name__ == "__main__":
    main()
