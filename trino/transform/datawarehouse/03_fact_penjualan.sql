-- fact_penjualan: parse tgl_transaksi (DD/MM/YYYY string) into a real date, cast qty to INTEGER
DROP TABLE IF EXISTS mongodb.dwh_db.fact_penjualan;

CREATE TABLE mongodb.dwh_db.fact_penjualan AS
SELECT
    id_transaksi,
    date_parse(tgl_transaksi, '%d/%m/%Y') AS tgl_transaksi,
    kode_cabang,
    kode_kasir,
    kode_item,
    kode_produk,
    CAST(qty_pembelian AS INTEGER) AS qty_pembelian
FROM mongodb.stg_db.stg_trans_penjualan;
