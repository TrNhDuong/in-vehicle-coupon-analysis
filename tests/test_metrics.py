import numpy as np
import pandas as pd
import pytest

from coupon_project.metrics import compare_groups, diff_ci, group_summary, rate_ci


def test_rate_ci_bounds_and_constant_cases():
    low, high = rate_ci([1, 0, 1, 1, 0, 1, 0, 1], n_boot=500, seed=7)
    assert 0.0 <= low <= 62.5 <= high <= 100.0
    assert rate_ci([1, 1, 1], n_boot=200, seed=7) == (100.0, 100.0)
    assert rate_ci([0, 0, 0], n_boot=200, seed=7) == (0.0, 0.0)

    empty_low, empty_high = rate_ci([])
    assert np.isnan(empty_low) and np.isnan(empty_high)


def test_rate_ci_rejects_non_binary():
    with pytest.raises(ValueError):
        rate_ci([0, 1, 2])


def test_diff_ci_detects_clear_gap():
    a = [1] * 80 + [0] * 20
    b = [1] * 30 + [0] * 70
    res = diff_ci(a, b, n_boot=1000, seed=42)
    assert res["n_a"] == 100
    assert res["n_b"] == 100
    assert res["diff_pp"] == pytest.approx(50.0)
    assert res["ci_low_pp"] < 50.0 < res["ci_high_pp"]
    assert res["ci_low_pp"] > 30.0


def test_diff_ci_handles_empty_group():
    res = diff_ci([1, 0], [])
    assert res["n_a"] == 2
    assert res["n_b"] == 0
    assert np.isnan(res["diff_pp"])
    assert np.isnan(res["ci_low_pp"])


def test_group_summary_and_small_sample_flag():
    df = pd.DataFrame(
        {
            "grp": ["A"] * 40 + ["B"] * 10,
            "Y": [1] * 30 + [0] * 10 + [1] * 4 + [0] * 6,
        }
    )
    summary = group_summary(df, ["grp"], min_n=30, n_boot=500, seed=1)
    assert list(summary["grp"]) == ["A", "B"]
    assert list(summary["n"]) == [40, 10]
    assert list(summary["accepted"]) == [30, 4]
    assert list(summary["rate_pct"]) == [75.0, 40.0]
    assert list(summary["small_sample"]) == [False, True]


def test_compare_groups_returns_clean_dict():
    df = pd.DataFrame({"grp": ["A", "A", "A", "B", "B"], "Y": [1, 1, 0, 0, 0]})
    res = compare_groups(
        df,
        df["grp"] == "A",
        df["grp"] == "B",
        label_a="Group A",
        label_b="Group B",
        min_n=5,
        n_boot=200,
    )
    assert res["group_a"] == "Group A"
    assert res["diff_pp"] == pytest.approx(66.67, abs=0.01)
    assert res["small_sample"] is True
