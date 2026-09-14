-- agg_penjualan_per_produk: total qty per product, used for top-product ranking
DROP TABLE IF EXISTS mongodb.mart_db.agg_penjualan_per_produk;

CREATE TABLE mongodb.mart_db.agg_penjualan_per_produk AS
SELECT
    p.kode_produk,
    p.nama_produk,
    SUM(f.qty_pembelian) AS total_qty
FROM mongodb.mart_db.fact_penjualan f
JOIN mongodb.mart_db.dim_produk p ON f.kode_produk = p.kode_produk
GROUP BY p.kode_produk, p.nama_produk;
