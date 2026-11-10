import pandas as pd
from coupon_project.quality import missing_table, target_is_binary


def test_missing_table_reports_percentage():
    sample = pd.DataFrame({"x": [1, None, 3, None], "Y": [0, 1, 1, 0]})
    result = missing_table(sample)
    assert result.loc["x", "missing_count"] == 2
    assert result.loc["x", "missing_pct"] == 50.0


def test_target_is_binary():
    assert target_is_binary(pd.DataFrame({"Y": [0, 1, 0]}))
    assert not target_is_binary(pd.DataFrame({"Y": [0, 2]}))
    assert not target_is_binary(pd.DataFrame({"Y": [0, None]}))
