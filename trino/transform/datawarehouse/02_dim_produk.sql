-- dim_produk: pass-through of product master data (already clean)
DROP TABLE IF EXISTS mongodb.dwh_db.dim_produk;

CREATE TABLE mongodb.dwh_db.dim_produk AS
SELECT
    kode_produk,
    kode_kategori,
    nama_produk,
    unit,
    kode_satuan
FROM mongodb.stg_db.stg_mst_produk;
