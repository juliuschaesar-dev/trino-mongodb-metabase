-- dim_produk: pass-through of product master data (already clean)
DROP TABLE IF EXISTS mongodb.mart_db.dim_produk;

CREATE TABLE mongodb.mart_db.dim_produk AS
SELECT
    kode_produk,
    kode_kategori,
    nama_produk,
    unit,
    kode_satuan
FROM mongodb.staging_db.mst_produk;
