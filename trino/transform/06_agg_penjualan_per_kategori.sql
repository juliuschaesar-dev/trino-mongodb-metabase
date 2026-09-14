-- agg_penjualan_per_kategori: total qty per product category
DROP TABLE IF EXISTS mongodb.mart_db.agg_penjualan_per_kategori;

CREATE TABLE mongodb.mart_db.agg_penjualan_per_kategori AS
SELECT
    p.kode_kategori,
    SUM(f.qty_pembelian) AS total_qty
FROM mongodb.mart_db.fact_penjualan f
JOIN mongodb.mart_db.dim_produk p ON f.kode_produk = p.kode_produk
GROUP BY p.kode_kategori;
