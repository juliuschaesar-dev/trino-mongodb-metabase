-- dm_penjualan_harian: daily total quantity + transaction count
DROP TABLE IF EXISTS mongodb.dm_db.dm_penjualan_harian;

CREATE TABLE mongodb.dm_db.dm_penjualan_harian AS
SELECT
    tgl_transaksi,
    SUM(qty_pembelian) AS total_qty,
    COUNT(*) AS transaction_count
FROM mongodb.dwh_db.fact_penjualan
GROUP BY tgl_transaksi;
