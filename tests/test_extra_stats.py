"""Extra tests for coupon_project.stats (audit 2026-11).  Each test guards a behaviour checked during the full audit."""

import numpy as np
import pandas as pd
import pytest

from coupon_project.stats import (
    bootstrap_diff_ci,
    bootstrap_rate_ci,
    contrasts,
    pivot_expiration,
    rate_table,
    rng_for,
    standardized_contrast,
    wilson_ci,
)

NUMPY_2 = np.lib.NumpyVersion(np.__version__) >= "2.0.0"


@pytest.mark.parametrize(
    "k,n", [(0, 1), (1, 1), (0, 10), (10, 10), (3, 10), (648, 1511), (0, 30), (29, 30)]
)
def test_wilson_matches_scipy(k, n):
    sstats = pytest.importorskip("scipy.stats")
    ci = sstats.binomtest(k, n).proportion_ci(confidence_level=0.95, method="wilson")
    assert wilson_ci(k, n) == pytest.approx((100 * ci.low, 100 * ci.high), abs=1e-9)


def test_wilson_rejects_impossible_counts():
    with pytest.raises(ValueError):
        wilson_ci(5, 3)


def test_binomial_shortcut_equals_row_resampling():
    """Resampling n rows of 0/1 data == drawing Binomial(n, p_hat): same 95% percentile interval."""
    y = np.r_[np.ones(80), np.zeros(120)]
    rng = np.random.default_rng(1)
    rows = rng.choice(y, size=(20000, y.size)).mean(axis=1) * 100
    assert bootstrap_rate_ci(y, n_boot=20000, seed=2) == pytest.approx(
        tuple(np.percentile(rows, [2.5, 97.5])), abs=1.0
    )


def test_bootstrap_ci_is_degenerate_for_constant_group():
    """Documented limitation: a constant group gets a zero-width CI (Wilson would not)."""
    assert bootstrap_rate_ci([0] * 5) == (0.0, 0.0)
    assert wilson_ci(0, 5)[1] > 40


def test_standardized_weights_and_point_by_hand():
    strata = pd.DataFrame(
        {
            "n_a": [40, 100, 10],
            "n_b": [60, 50, 300],
            "accepted_a": [20, 80, 9],
            "accepted_b": [15, 35, 30],
            "rate_a_pct": [50.0, 80.0, 90.0],
            "rate_b_pct": [25.0, 70.0, 10.0],
            "diff_pp": [25.0, 10.0, 80.0],
        }
    )
    res = standardized_contrast(strata, min_n=30, n_boot=500, key="t")
    # stratum 3 dropped (n_a=10 < 30); weights = (40+60, 100+50) / 250 = 0.4, 0.6
    assert res["n_strata_used"] == 2 and res["coverage"] == pytest.approx(250 / 560, abs=1e-4)
    assert res["diff_pp"] == pytest.approx(0.4 * 25 + 0.6 * 10)
    assert res["ci_low_pp"] < res["diff_pp"] < res["ci_high_pp"]


def test_contrasts_status_and_small_n():
    df = pd.DataFrame(
        {
            "s": ["a"] * 70 + ["b"] * 40 + ["c"] * 20,
            "x": ["A"] * 35 + ["B"] * 35 + ["A"] * 25 + ["B"] * 15 + ["A"] * 20,
            "Y": np.tile([0, 1], 65),
        }
    )
    out = contrasts(df, ["s"], "x", "A", "B", n_boot=200).set_index("s")
    assert out["status"].to_dict() == {"a": "ok", "b": "small_n", "c": "no_common_support"}
    assert out["small_n"].to_dict() == {"a": False, "b": True, "c": True}
    assert np.isnan(out.loc["c", "ci_low_pp"])


def test_contrasts_seed_does_not_depend_on_row_order():
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "s": rng.choice(["p", "q", "r"], 600),
            "x": rng.choice(["A", "B"], 600),
            "Y": rng.integers(0, 2, 600),
        }
    )
    a = contrasts(df, ["s"], "x", "A", "B", n_boot=300, key="k").set_index("s")
    b = contrasts(
        df.sample(frac=1, random_state=3), ["s"], "x", "A", "B", n_boot=300, key="k"
    ).set_index("s")
    pd.testing.assert_frame_equal(a.sort_index(), b.sort_index())


def test_rate_table_keeps_nan_stratum_as_own_group():
    df = pd.DataFrame({"g": ["u", None, "u", None], "Y": [1, 0, 0, 0]})
    out = rate_table(df, ["g"])
    assert len(out) == 2 and out["g"].isna().sum() == 1


def test_contrasts_rejects_unknown_group_label():
    df = pd.DataFrame({"x": pd.Categorical(["near", "far"] * 20), "Y": [0, 1] * 20})
    with pytest.raises(ValueError):
        contrasts(df, [], "x", "nearr", "far")


def test_golden_seed_and_ci_are_stable():
    """Reproducibility guard: if this fails after a numpy/pandas upgrade, the published CIs change too -> rerun notebooks."""
    assert int(rng_for("q1_overall").integers(0, 2**31 - 1)) == 1132313102
    res = bootstrap_diff_ci([1] * 30 + [0] * 20, [1] * 10 + [0] * 40, n_boot=2000, seed=42)
    assert (res["diff_pp"], res["ci_low_pp"], res["ci_high_pp"]) == (40.0, 22.0, 56.0)


def test_rng_for_same_seed_for_numpy_and_python_scalars():
    a = rng_for(("k", ("Bar", np.int64(1)))).integers(1_000_000_000)
    b = rng_for(("k", ("Bar", 1))).integers(1_000_000_000)
    assert a == b


def test_pivot_expiration_matches_groupby():
    df = pd.DataFrame(
        {
            "time": ["7AM", "7AM", "10PM", "10PM", "10PM", "2PM"],
            "expiration": ["2h", "1d", "1d", "1d", "2h", "1d"],
            "Y": [0, 1, 1, 0, 1, 1],
        }
    )
    rates, counts, long = pivot_expiration(df)
    assert list(rates.index) == [
        "7AM",
        "10AM",
        "2PM",
        "6PM",
        "10PM",
    ]  # observed=False keeps every slot
    assert counts.loc["10PM", "1d"] == 2 and rates.loc["10PM", "1d"] == pytest.approx(50.0)
    assert counts.loc["10AM", "2h"] == 0 and np.isnan(rates.loc["10AM", "2h"])
    assert rates.loc["10PM", "diff_1d_minus_2h_pp"] == pytest.approx(-50.0)
    assert len(long) == 10 and long["n"].sum() == len(df)


def test_pivot_expiration_with_single_expiration_level():
    rates, counts, _ = pivot_expiration(
        pd.DataFrame({"time": ["7AM", "2PM"], "expiration": ["1d", "1d"], "Y": [1, 0]})
    )
    assert counts["2h"].sum() == 0 and rates["2h"].isna().all()


def test_pivot_expiration_rejects_unknown_labels():
    with pytest.raises(ValueError):
        pivot_expiration(
            pd.DataFrame({"time": ["7AM", "11AM"], "expiration": ["2h", "1d"], "Y": [1, 0]})
        )
