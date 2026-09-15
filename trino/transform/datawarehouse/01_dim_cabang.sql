-- dim_cabang: parse city & branch sequence number out of nama_cabang
-- nama_cabang pattern: "PHI Mini Market - <City> <Sequence No.>"
DROP TABLE IF EXISTS mongodb.dwh_db.dim_cabang;

CREATE TABLE mongodb.dwh_db.dim_cabang AS
SELECT
    kode_cabang,
    nama_cabang,
    regexp_extract(nama_cabang, '- (.*) \d+$', 1) AS city,
    CAST(regexp_extract(nama_cabang, '(\d+)$', 1) AS INTEGER) AS branch_sequence_no
FROM mongodb.stg_db.stg_mst_cabang;
