import numpy as np
import pandas as pd
import pytest

from coupon_project.journey import (
    TRAVEL_BAND_ORDER,
    add_time_band,
    check_flags,
    q1_direction_diff,
    q1_distance_diff,
    q2_expiry_diff,
    q2_pivots,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "toCoupon_GEQ5min": [1, 1, 1, 1, 1, 1],
            "toCoupon_GEQ15min": [0, 0, 1, 1, 1, 1],
            "toCoupon_GEQ25min": [0, 0, 0, 0, 1, 1],
            "direction_same": [1, 0, 1, 0, 0, 0],
            "direction_opp": [0, 1, 0, 1, 1, 1],
            "destination": ["Home", "Home", "Work", "Work", "Home", "Work"],
            "coupon": ["Bar", "Bar", "Coffee House", "Coffee House", "Bar", "Bar"],
            "time": ["7AM", "7AM", "10AM", "10AM", "6PM", "6PM"],
            "expiration": ["1d", "2h", "1d", "2h", "1d", "2h"],
            "Y": [1, 0, 1, 0, 0, 1],
        }
    )


def test_check_flags_and_add_time_band():
    df = _sample_df()
    audit = check_flags(df)
    assert audit["geq5_always_one"] is True
    assert audit["invalid_geq_hierarchy_count"] == 0
    assert audit["direction_complement_ok"] is True

    out = add_time_band(df)
    assert list(out["travel_time_band"].cat.categories) == TRAVEL_BAND_ORDER
    assert list(out["travel_time_band"]) == [
        "5-<15 min",
        "5-<15 min",
        "15-<25 min",
        "15-<25 min",
        ">=25 min",
        ">=25 min",
    ]


def test_add_time_band_rejects_inconsistent_flags():
    bad = _sample_df().iloc[:2].copy()
    bad.loc[0, "toCoupon_GEQ15min"] = 0
    bad.loc[0, "toCoupon_GEQ25min"] = 1
    with pytest.raises(ValueError):
        add_time_band(bad)


def test_q1_distance_and_direction_diff():
    df = add_time_band(_sample_df())
    dist_df = q1_distance_diff(df, n_boot=200, seed=10)
    assert len(dist_df) == 1
    assert dist_df.loc[0, "n_a"] == 2
    assert dist_df.loc[0, "n_b"] == 2

    dir_df = q1_direction_diff(df, by=["destination"], n_boot=200, seed=10)
    assert set(dir_df["destination"]) == {"Home", "Work"}


def test_q2_pivots_and_expiry_diff_handle_missing_cells():
    df = _sample_df()
    rate_p, cnt_p, long_df = q2_pivots(df)
    assert list(rate_p.columns) == ["2h", "1d", "diff_1d_minus_2h_pp"]
    assert rate_p.loc["7AM", "1d"] == 100.0
    assert rate_p.loc["7AM", "2h"] == 0.0
    assert cnt_p.loc["2PM", "2h"] == 0
    assert np.isnan(rate_p.loc["2PM", "2h"])
    assert set(["time", "expiration", "rate_pct", "n"]).issubset(long_df.columns)

    diff_df = q2_expiry_diff(df, by=["coupon"], n_boot=200, seed=5)
    assert set(diff_df["coupon"]) == {"Bar", "Coffee House"}
