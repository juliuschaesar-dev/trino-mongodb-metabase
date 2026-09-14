# mongodb-trino-metabase

Retail sales analytics dashboard: raw CSV data loaded into MongoDB via a
pymongo script, transformed into datamarts via Trino SQL, visualized in Metabase. Demonstrates staging -> datamart pattern on top of MongoDB, with Trino as both transform and query engine.

## Architecture

![Architecture](docs/architecture.svg)

## Stack

| Layer | Tool |
|---|---|
| Source | 3 CSV files (`mst_cabang`, `mst_produk`, `trans_penjualan`) in `data/raw/` |
| Extract/Load | `scripts/load_to_mongo.py` (pymongo, CSV -> MongoDB `staging_db`) |
| Database | MongoDB (`staging_db`, `mart_db`) |
| Transform | Trino (MongoDB connector), driven by `scripts/run_transform.py` |
| Dashboard | Metabase (Starburst/Trino driver) |

## Setup

1. Copy the env template and adjust if needed:
   ```bash
   cp .env.example .env
   ```
   Make sure `MONGO_USER`/`MONGO_PASSWORD` here match `trino/catalog/mongodb.properties`
   (Trino catalog files don't support env var substitution).

2. Start MongoDB, Trino, and Metabase:
   ```bash
   docker compose up -d
   ```

3. Create a virtualenv, install dependencies, then load the CSVs into `staging_db` and run the
   Trino transforms to build `mart_db`:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python scripts/load_to_mongo.py
   python scripts/run_transform.py
   ```

4. Connect Metabase to Trino and build the dashboard (see
   [metabase/README.md](metabase/README.md)).

## Tests

Unit tests cover the pure logic in `scripts/` (CSV parsing, SQL statement splitting, the Trino
retry loop) with mocked MongoDB/Trino clients — no live services required. Same
`requirements.txt` as Setup step 3, just a different command:

```bash
pip install -r requirements.txt
pytest
```

## Repo structure

```
mongodb-trino-metabase/
├── docker-compose.yml          # MongoDB, Trino, Metabase
├── .env / .env.example
├── requirements.txt
├── data/raw/                   # source CSVs
├── trino/
│   ├── catalog/mongodb.properties
│   └── transform/               # 00_..07_ numbered transform SQL, run in order
├── scripts/
│   ├── load_to_mongo.py        # loads data/raw/*.csv into staging_db (pymongo)
│   └── run_transform.py        # runs every .sql file in trino/transform/
├── tests/
│   ├── conftest.py             # puts the repo root on sys.path so tests can import scripts/
│   ├── test_load_to_mongo.py
│   └── test_run_transform.py
├── metabase/README.md          # Metabase -> Trino connection + dashboard panels
└── docs/architecture.svg
```
