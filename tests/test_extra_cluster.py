"""Extra tests for the cluster (respondent) bootstrap in coupon_project.stats."""

import numpy as np
import pandas as pd
import pytest

from coupon_project.stats import _cluster_bootstrap, cluster_diff_ci, cluster_rates_ci


def make_panel(n_people=40, rows_each=6, seed=0):
    rng = np.random.default_rng(seed)
    pid = np.repeat(np.arange(n_people), rows_each)
    return pd.DataFrame(
        {
            "respondent_id": pid,
            "grp": pd.Categorical(
                np.where(pid % 2 == 0, "A", "B"), categories=["A", "B"]
            ),  # person-level group
            "stratum": np.tile(["s1", "s2", "s3"], n_people * rows_each // 3),
            "Y": rng.integers(0, 2, pid.size),
        }
    )


def direct_standardised(data):
    """Plain pandas: sum over strata of rate(group, stratum) * share(stratum)."""
    share = data["stratum"].value_counts(normalize=True)
    cell = data.groupby(["grp", "stratum"], observed=True)["Y"].mean()
    return np.array([100 * sum(cell[(g, s)] * w for s, w in share.items()) for g in ["A", "B"]])


def test_point_estimate_is_direct_standardisation():
    df = make_panel()
    point, _ = _cluster_bootstrap(df, "grp", ("stratum",), n_boot=1)
    assert point == pytest.approx(direct_standardised(df))


def test_each_draw_equals_physically_resampled_people():
    """Weight k for a person drawn k times == copying that person's rows k times (same multinomial stream)."""
    df = make_panel()
    _, draws = _cluster_bootstrap(df, "grp", ("stratum",), n_boot=20, seed=7)
    rng = np.random.default_rng(7)
    uid = pd.factorize(df["respondent_id"])[0]
    for k in range(20):
        times = rng.multinomial(40, np.full(40, 1 / 40))
        boot = df.iloc[np.repeat(np.arange(len(df)), times[uid])]
        assert draws[k] == pytest.approx(direct_standardised(boot))


def test_cluster_ci_wider_than_row_ci_for_person_level_group():
    df = make_panel(n_people=60, rows_each=10, seed=1)
    df["Y"] = (df["respondent_id"] % 3 == 0).astype(int)  # strong within-person correlation
    person = cluster_diff_ci(df, "grp", "A", "B", n_boot=500)
    row = cluster_diff_ci(df, "grp", "A", "B", n_boot=500, unit="row")
    assert person["ci_high_pp"] - person["ci_low_pp"] > row["ci_high_pp"] - row["ci_low_pp"]


def test_nan_in_strata_gives_clear_error():
    df = make_panel()
    df.loc[3, "stratum"] = None
    with pytest.raises(ValueError, match="NaN|thiếu"):
        cluster_diff_ci(df, "grp", "A", "B", strata_cols=("stratum",), n_boot=50)


def test_nan_respondent_id_is_rejected():
    df = make_panel()
    df["respondent_id"] = df["respondent_id"].astype(float)
    df.loc[:5, "respondent_id"] = np.nan
    with pytest.raises(ValueError):
        cluster_rates_ci(df, "grp", n_boot=50)


def test_non_binary_target_is_rejected():
    df = make_panel()
    df.loc[0, "Y"] = 2
    with pytest.raises(ValueError):
        cluster_rates_ci(df, "grp", n_boot=50)


def test_unknown_unit_is_rejected():
    with pytest.raises(ValueError):
        cluster_diff_ci(make_panel(), "grp", "A", "B", unit="respondents", n_boot=50)
