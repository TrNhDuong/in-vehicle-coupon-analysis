"""Leakage-safe sklearn Pipeline builder, respondent-clustered bootstrap, and error tables for Q6."""
import numpy as np
import pandas as pd


def build_pipeline(estimator, cat_cols, bin_cols):
    """Build ColumnTransformer (SimpleImputer + dense OneHotEncoder) + estimator Pipeline."""
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder

    prep = ColumnTransformer([
        ("cat", Pipeline([
            ("imp", SimpleImputer(strategy="constant", fill_value="missing")),
            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]), list(cat_cols)),
        ("bin", "passthrough", list(bin_cols)),
    ])
    return Pipeline([("preprocess", prep), ("model", estimator)])


def cluster_bootstrap_metric(metric_fn, y_true, y_values, groups, n_boot: int = 1000, seed: int = 42) -> np.ndarray:
    """Bootstrap metric_fn by resampling respondent clusters cleanly via sample weights."""
    rng = np.random.default_rng(seed)
    pid = pd.factorize(np.asarray(groups))[0]
    n_people = int(pid.max() + 1)
    probs = np.full(n_people, 1.0 / n_people)
    return np.array([metric_fn(y_true, y_values, sample_weight=rng.multinomial(n_people, probs)[pid]) for _ in range(n_boot)])


def error_breakdown(df: pd.DataFrame, y_true, y_pred, y_proba, group_col: str) -> pd.DataFrame:
    """Compute group acceptance rate, accuracy, FPR (%), and FNR (%) without mutating df."""
    work = pd.DataFrame({
        group_col: df[group_col].to_numpy(),
        "y_true": np.asarray(y_true),
        "y_pred": np.asarray(y_pred),
        "proba": np.asarray(y_proba),
    })
    work["ok"] = work["y_true"] == work["y_pred"]
    work["fp"] = (work["y_true"] == 0) & (work["y_pred"] == 1)
    work["fn"] = (work["y_true"] == 1) & (work["y_pred"] == 0)
    work["neg"] = work["y_true"] == 0
    work["pos"] = work["y_true"] == 1

    grouped = work.groupby(group_col, observed=False)
    neg_cnt = grouped["neg"].sum().replace(0, np.nan)
    pos_cnt = grouped["pos"].sum().replace(0, np.nan)
    out = pd.DataFrame({
        "n": grouped.size(),
        "true_rate": grouped["y_true"].mean().round(3),
        "acc": grouped["ok"].mean().round(3),
        "FPR": (grouped["fp"].sum() / neg_cnt * 100.0).round(2),
        "FNR": (grouped["fn"].sum() / pos_cnt * 100.0).round(2),
    })
    return out.sort_values("true_rate")


def probability_bins(y_true, y_pred, y_proba, bins=(0, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0)) -> pd.DataFrame:
    """Summarize calibration and accuracy across predicted probability bins."""
    work = pd.DataFrame({
        "y_true": np.asarray(y_true),
        "ok": np.asarray(y_true) == np.asarray(y_pred),
        "proba": np.asarray(y_proba),
    })
    work["p_bin"] = pd.cut(work["proba"], list(bins), include_lowest=True)
    return work.groupby("p_bin", observed=True).agg(
        n=("y_true", "size"), mean_p=("proba", "mean"), true_y=("y_true", "mean"), acc=("ok", "mean"),
    ).round(3)
