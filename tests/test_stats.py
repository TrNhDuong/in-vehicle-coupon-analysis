import pandas as pd
import pytest

from coupon_project.stats import (
    bootstrap_diff_ci,
    bootstrap_rate_ci,
    cluster_diff_ci,
    cluster_rates_ci,
    contrasts,
    pivot_expiration,
    rate_table,
    standardized_contrast,
    wilson_ci,
)


def test_wilson_and_bootstrap_cis():
    assert pd.isna(wilson_ci(0, 0)[0])
    assert wilson_ci(0, 10)[0] == 0.0
    assert wilson_ci(10, 10)[1] == 100.0
    assert bootstrap_rate_ci([1, 1, 1]) == (100.0, 100.0)
    res = bootstrap_diff_ci([1, 1, 0, 0], [0, 0, 0, 0], n_boot=300, seed=7)
    assert res["diff_pp"] == pytest.approx(50.0)
    assert res["ci_low_pp"] <= 50.0 <= res["ci_high_pp"]


def test_rate_table_contrasts_and_standardization():
    df = pd.DataFrame({
        "stratum": ["S1"] * 4 + ["S2"] * 4,
        "arm": ["A", "A", "B", "B"] * 2,
        "Y": [1, 1, 0, 0, 1, 0, 0, 0],
    })
    tbl = rate_table(df, ["arm"], min_n=2)
    assert tbl.loc[tbl["arm"] == "A", "rate_pct"].iloc[0] == pytest.approx(75.0)
    c = contrasts(df, ["stratum"], "arm", "A", "B", min_n=2, n_boot=300, key="t")
    assert len(c) == 2
    s = standardized_contrast(c, min_n=2, n_boot=300, key="t")
    assert s["status"] == "ok" and s["n_strata_used"] == 2
    assert s["diff_pp"] == pytest.approx(75.0)

    p_r, p_c, p_l = pivot_expiration(pd.DataFrame({"time": ["7AM", "7AM"], "expiration": ["1d", "2h"], "Y": [1, 0]}))
    assert p_r.loc["7AM", "diff_1d_minus_2h_pp"] == pytest.approx(100.0)
    assert len(p_l) == 10 and p_l["n"].sum() == 2


def test_cluster_rates_and_diff():
    df = pd.DataFrame({
        "respondent_id": [0, 0, 1, 1, 2, 2, 3, 3],
        "grp": pd.Categorical(["A", "A", "A", "A", "B", "B", "B", "B"], categories=["A", "B"], ordered=True),
        "stratum": ["S1", "S2"] * 4,
        "Y": [1, 1, 1, 0, 0, 0, 1, 0],
    })
    rates = cluster_rates_ci(df, "grp", n_boot=200, seed=42)
    assert rates.loc["A", "rate_pct"] == pytest.approx(75.0)
    diff = cluster_diff_ci(df, "grp", "A", "B", strata_cols=("stratum",), n_boot=200, seed=42)
    assert diff["diff_pp"] == pytest.approx(50.0)
    assert diff["ci_low_pp"] <= 50.0 <= diff["ci_high_pp"]
