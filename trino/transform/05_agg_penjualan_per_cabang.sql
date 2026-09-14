-- agg_penjualan_per_cabang: total qty + transaction count per branch, with city for grouping
DROP TABLE IF EXISTS mongodb.mart_db.agg_penjualan_per_cabang;

CREATE TABLE mongodb.mart_db.agg_penjualan_per_cabang AS
SELECT
    f.kode_cabang,
    c.nama_cabang,
    c.city,
    SUM(f.qty_pembelian) AS total_qty,
    COUNT(*) AS transaction_count
FROM mongodb.mart_db.fact_penjualan f
JOIN mongodb.mart_db.dim_cabang c ON f.kode_cabang = c.kode_cabang
GROUP BY f.kode_cabang, c.nama_cabang, c.city;
