"""Statistical edge cases matter more than matching presentation details."""
import numpy as np
import pandas as pd
import pytest

from coupon_project.analysis import (
    contrasts, matched_frequency, rate_table, standardized_contrast, wilson,
)


def test_wilson_empty_and_extreme_cells():
    assert all(np.isnan(wilson(0, 0)))
    lo, hi = wilson(0, 10)
    assert lo == 0 and hi == pytest.approx(0.2775328)
    lo, hi = wilson(10, 10)
    assert lo == pytest.approx(0.7224672) and hi == 1


def test_mapping_does_not_use_unmatched_habits_or_fill_nulls():
    frame = pd.DataFrame({"coupon": ["Bar", "Coffee House"],
                          "Bar": [None, "never"], "CoffeeHouse": ["gt8", "1~3"]})
    result = matched_frequency(frame)
    assert pd.isna(result.iloc[0]) and result.iloc[1] == "1~3"
    frame.loc[0, "coupon"] = "unexpected"
    with pytest.raises(ValueError):
        matched_frequency(frame)


def test_rates_preserve_missing_groups_and_reject_invalid_targets():
    frame = pd.DataFrame({"group": ["x", None], "Y": [0, 1]})
    result = rate_table(frame, ["group"])
    assert result.n.sum() == 2 and result.accepted.sum() == 1
    with pytest.raises(ValueError):
        rate_table(frame.assign(Y=[0, None]), ["group"])


def test_missing_comparison_is_not_zero_and_bootstrap_is_reproducible():
    frame = pd.DataFrame({"stratum": ["x"] * 8 + ["y"],
                          "group": ["a"] * 4 + ["b"] * 4 + ["a"],
                          "Y": [1, 1, 1, 0, 1, 0, 0, 0, 1]})
    result = contrasts(frame, ["stratum"], "group", "a", "b")
    pd.testing.assert_frame_equal(result, contrasts(frame, ["stratum"], "group", "a", "b"))
    assert result.iloc[0].diff_pp == 50
    assert result.iloc[0].ci_low_pp <= 50 <= result.iloc[0].ci_high_pp
    assert result.iloc[1].status == "no_common_support"
    assert np.isnan(result.iloc[1].diff_pp)


def test_standardization_uses_same_weights_and_reports_support_loss():
    strata = pd.DataFrame({"n_a": [100, 30, 10], "n_b": [100, 30, 0],
                           "rate_a": [.8, .4, .5], "rate_b": [.5, .5, np.nan],
                           "diff_pp": [30., -10., np.nan]})
    result = standardized_contrast(strata)
    assert result["n_strata_used"] == 2
    assert result["coverage"] == pytest.approx(260 / 270)
    assert result["diff_pp"] == pytest.approx((200 * 30 - 60 * 10) / 260)
    assert standardized_contrast(strata.iloc[2:])["status"] == "no_common_support"
