# Metabase Setup

1. Open Metabase at `http://localhost:3000` and complete first-run admin setup.
2. **Admin settings -> Databases -> Add database**:
   - **Database type:** Starburst / Trino (`MB_DB_TYPE=starburst` in `.env`)
   - **Host:** `trino` (Docker Compose service name), **Port:** `8080`
   - **Catalog:** `mongodb` (`MB_DB_CATALOG`)
   - **Schema (schema filter, "only these"):** `dm_db` (`MB_DB_SCHEMA`) — this restricts Metabase
     to the `dm_db` (datamart) schema only, so it **cannot** browse or query the `stg_db` (staging)
     or `dwh_db` (warehouse) layers, even though all three live under the same Trino `mongodb`
     catalog.
   - **User:** value of `TRINO_USER`
3. Sync/scan the database once tables exist (i.e. after running `pipeline/datawarehouse.py` and
   `pipeline/datamart.py`).

## Dashboard panels

| Panel | Source table | Visual type |
|---|---|---|
| Total qty sold & transaction count | `dm_penjualan_harian` | Number/KPI card |
| Daily/monthly sales trend (2020) | `dm_penjualan_harian` | Line chart |
| Top 10 branches by qty | `dm_penjualan_per_cabang` | Bar chart |
| Sales by city | `dm_penjualan_per_cabang` grouped by `city` | Bar chart / table |
| Qty distribution by category | `dm_penjualan_per_kategori` | Donut chart (3 categories) |
| Top 10 best-selling products | `dm_penjualan_per_produk` | Bar chart |

