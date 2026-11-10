import pytest
from coupon_project.data_io import row_count_log, load_raw_data


def test_row_count_log():
    assert row_count_log(100, 92, "drop na") == "drop na: 100 -> 92 rows (delta -8)"


def test_row_count_log_negative_rejected():
    with pytest.raises(ValueError):
        row_count_log(-1, 0, "bad")


def test_loader_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_raw_data(tmp_path / "missing.csv")
