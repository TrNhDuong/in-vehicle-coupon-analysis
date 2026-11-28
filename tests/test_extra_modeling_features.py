"""Extra tests for coupon_project.modeling and coupon_project.features."""

import numpy as np
import pandas as pd
import pytest

from coupon_project.features import COUPON_FREQUENCY, build_respondent_id, matched_frequency
from coupon_project.modeling import build_pipeline, cluster_bootstrap_metric, error_breakdown


def test_error_breakdown_fpr_fnr_definitions_and_missing_class():
    df = pd.DataFrame({"grp": ["a"] * 6 + ["b"] * 3})
    y_true = [0, 0, 1, 1, 1, 0, 1, 1, 1]
    y_pred = [1, 0, 1, 0, 0, 0, 1, 0, 1]
    out = error_breakdown(df, y_true, y_pred, "grp")
    # group a: 3 true negatives-or-FP rows (1 FP) and 3 true-positive-or-FN rows (2 FN)
    assert out.loc["a", "FPR"] == pytest.approx(100 / 3, abs=0.01)
    assert out.loc["a", "FNR"] == pytest.approx(200 / 3, abs=0.01)
    assert np.isnan(out.loc["b", "FPR"])  # group b has no y_true == 0 -> FPR undefined
    assert out.loc["b", "FNR"] == pytest.approx(100 / 3, abs=0.01)


def test_cluster_bootstrap_metric_weights_equal_replication():
    metrics = pytest.importorskip("sklearn.metrics")
    rng = np.random.default_rng(0)
    groups = np.repeat(np.arange(30), 5)
    y = rng.integers(0, 2, groups.size)
    p = np.clip(0.3 * y + 0.7 * rng.random(groups.size), 0, 1)
    draws = cluster_bootstrap_metric(metrics.roc_auc_score, y, p, groups, n_boot=10, seed=3)
    r = np.random.default_rng(3)
    for k in range(10):
        idx = np.repeat(np.arange(groups.size), r.multinomial(30, np.full(30, 1 / 30))[groups])
        assert draws[k] == pytest.approx(metrics.roc_auc_score(y[idx], p[idx]))


def test_build_pipeline_mixed_str_and_int_categoricals():
    pytest.importorskip("sklearn")
    from sklearn.dummy import DummyClassifier

    X = pd.DataFrame(
        {
            "weather": pd.array(["Sunny", None, "Rainy", "Sunny"], dtype="str"),
            "temperature": [30, 55, 80, 55],
            "flag": [0, 1, 0, 1],
        }
    )
    pipe = build_pipeline(DummyClassifier(), ["weather", "temperature"], ["flag"]).fit(
        X, [0, 1, 1, 0]
    )
    ohe = pipe.named_steps["preprocess"].named_transformers_["cat"].named_steps["ohe"]
    assert "missing" in list(ohe.categories_[0]) and list(ohe.categories_[1]) == [30, 55, 80]


def test_matched_frequency_equals_rowwise_lookup():
    df = pd.DataFrame({"coupon": list(COUPON_FREQUENCY)})
    for i, col in enumerate(COUPON_FREQUENCY.values()):
        df[col] = ["never"] * 5
        df.loc[i, col] = ["1~3", "4~8", "gt8", "less1", None][i]
    got = matched_frequency(df)
    assert got.tolist()[:4] == ["1~3", "4~8", "gt8", "less1"] and pd.isna(got.iloc[4])


def test_build_respondent_id_treats_nan_as_a_level():
    df = pd.DataFrame({"age": ["21", "21", "21", "31"], "car": [None, None, "SUV", None]})
    assert build_respondent_id(df, ["age", "car"]).tolist() == [0, 0, 1, 2]
