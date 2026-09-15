from unittest.mock import MagicMock

from pipeline import datawarehouse


def test_transform_dir_points_at_datawarehouse_folder():
    assert datawarehouse.TRANSFORM_DIR.parts[-2:] == ("transform", "datawarehouse")


def test_main_runs_transform_dir_once(monkeypatch):
    run_transform_dir = MagicMock()
    monkeypatch.setattr(datawarehouse, "run_transform_dir", run_transform_dir)

    datawarehouse.main()

    run_transform_dir.assert_called_once_with(datawarehouse.TRANSFORM_DIR)
