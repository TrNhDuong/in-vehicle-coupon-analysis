import pandas as pd
import pytest

from coupon_project.modeling import (
    build_pipeline,
    cluster_bootstrap_metric,
    error_breakdown,
    probability_bins,
)


def test_error_breakdown_and_probability_bins():
    df = pd.DataFrame({"coupon": ["Bar", "Bar", "Coffee", "Coffee"]})
    y_true = [0, 1, 0, 1]
    y_pred = [1, 1, 0, 0]
    y_prob = [0.8, 0.9, 0.2, 0.45]

    err = error_breakdown(df, y_true, y_pred, "coupon")
    assert err.loc["Bar", "FPR"] == pytest.approx(100.0)
    assert err.loc["Bar", "FNR"] == pytest.approx(0.0)
    assert err.loc["Coffee", "FPR"] == pytest.approx(0.0)
    assert err.loc["Coffee", "FNR"] == pytest.approx(100.0)

    bins = probability_bins(y_true, y_pred, y_prob)
    assert bins["n"].sum() == 4


def test_cluster_bootstrap_metric_weighted():
    def weighted_acc(yt, yp, sample_weight=None):
        import numpy as np
        yt, yp = np.asarray(yt), np.asarray(yp)
        return float(np.average(yt == yp, weights=sample_weight))

    draws = cluster_bootstrap_metric(weighted_acc, [1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1], n_boot=50, seed=7)
    assert len(draws) == 50
    assert (draws >= 0.0).all() and (draws <= 1.0).all()


def test_build_pipeline_fits_cleanly():
    sklearn_dummy = pytest.importorskip("sklearn.dummy")
    pipe = build_pipeline(sklearn_dummy.DummyClassifier(strategy="most_frequent"), ["cat"], ["bin"])
    X = pd.DataFrame({"cat": ["a", None, "b", "a"], "bin": [0, 1, 0, 1]})
    y = pd.Series([0, 1, 1, 1])
    pipe.fit(X, y)
    assert len(pipe.predict(pd.DataFrame({"cat": ["unseen"], "bin": [1]}))) == 1
