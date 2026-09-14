# Metabase Setup

1. Open Metabase at `http://localhost:3000` and complete first-run admin setup.
2. **Admin settings -> Databases -> Add database**:
   - **Database type:** Starburst / Trino (`MB_DB_TYPE=starburst` in `.env`)
   - **Host:** `trino` (Docker Compose service name), **Port:** `8080`
   - **Catalog:** `mongodb` (`MB_DB_CATALOG`)
   - **Schema (schema filter, "only these"):** `mart_db` (`MB_DB_SCHEMA`) — this restricts Metabase
     to the `mart_db` schema only, so it **cannot** browse or query `staging_db` even though both
     live under the same Trino `mongodb` catalog.
   - **User:** value of `TRINO_USER`
3. Sync/scan the database once tables exist (i.e. after running `scripts/run_transform.py`).

## Dashboard panels

| Panel | Source table | Visual type |
|---|---|---|
| Total qty sold & transaction count | `agg_penjualan_harian` | Number/KPI card |
| Daily/monthly sales trend (2020) | `agg_penjualan_harian` | Line chart |
| Top 10 branches by qty | `agg_penjualan_per_cabang` | Bar chart |
| Sales by city | `agg_penjualan_per_cabang` grouped by `city` | Bar chart / table |
| Qty distribution by category | `agg_penjualan_per_kategori` | Donut chart (3 categories) |
| Top 10 best-selling products | `agg_penjualan_per_produk` | Bar chart |

