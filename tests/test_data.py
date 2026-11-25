import pandas as pd
import pytest

from coupon_project.data import audit_row, load_raw_data, missing_table, row_count_log, target_is_binary


def test_load_raw_data_rejects_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_raw_data(tmp_path / "missing.csv")


def test_row_count_log_and_audit():
    assert row_count_log(100, 90, "filter") == "filter: 100 -> 90 rows (delta -10)"
    with pytest.raises(ValueError):
        row_count_log(-1, 10, "bad")
    assert audit_row("dedup", 100, 95, "test")["rows_removed"] == 5


def test_missing_table_and_target_check():
    df = pd.DataFrame({"a": [1, None, None, 4], "Y": [1, 0, 1, 0]})
    tbl = missing_table(df)
    assert tbl.loc["a", "missing_count"] == 2
    assert tbl.loc["a", "missing_pct"] == pytest.approx(50.0)
    assert target_is_binary(df)
    assert not target_is_binary(pd.DataFrame({"Y": [1, 2]}))
    assert not target_is_binary(pd.DataFrame({"Y": [1, None]}))
