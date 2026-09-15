from unittest.mock import MagicMock

from pipeline import datamart


def test_transform_dir_points_at_datamart_folder():
    assert datamart.TRANSFORM_DIR.parts[-2:] == ("transform", "datamart")


def test_main_runs_transform_dir_once(monkeypatch):
    run_transform_dir = MagicMock()
    monkeypatch.setattr(datamart, "run_transform_dir", run_transform_dir)

    datamart.main()

    run_transform_dir.assert_called_once_with(datamart.TRANSFORM_DIR)
