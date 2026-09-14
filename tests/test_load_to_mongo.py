from scripts import load_to_mongo


def test_load_csv_parses_semicolon_delimited_rows(tmp_path):
    csv_path = tmp_path / "mst_cabang.csv"
    csv_path.write_text(
        "kode_cabang;nama_cabang\n"
        "CABANG-001;PHI Mini Market - Lhokseumawe 01\n"
        "CABANG-002;PHI Mini Market - Bau-Bau 01\n",
        encoding="utf-8",
    )

    rows = load_to_mongo.load_csv(csv_path)

    assert rows == [
        {"kode_cabang": "CABANG-001", "nama_cabang": "PHI Mini Market - Lhokseumawe 01"},
        {"kode_cabang": "CABANG-002", "nama_cabang": "PHI Mini Market - Bau-Bau 01"},
    ]


def test_load_csv_strips_utf8_bom(tmp_path):
    csv_path = tmp_path / "with_bom.csv"
    csv_path.write_bytes("kode_produk;unit\nPROD-01;1\n".encode("utf-8-sig"))

    rows = load_to_mongo.load_csv(csv_path)

    assert rows == [{"kode_produk": "PROD-01", "unit": "1"}]


def test_load_csv_header_only_file_returns_no_rows(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("kode_produk;unit\n", encoding="utf-8")

    assert load_to_mongo.load_csv(csv_path) == []
