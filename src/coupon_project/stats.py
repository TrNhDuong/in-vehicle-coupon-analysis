"""Unified rate, CI, stratified contrast, and cluster-bootstrap statistics (% and pp)."""
import hashlib
from statistics import NormalDist

import numpy as np
import pandas as pd

from .features import EXPIRATION_ORDER, TIME_ORDER

MIN_N = 30
SEED = 42
N_BOOT = 2000


def validate_binary(values) -> np.ndarray:
    """Validate and return binary 0/1 float array without nulls."""
    arr = pd.Series(values).to_numpy(dtype=float)
    if np.isnan(arr).any() or (arr.size and not np.isin(arr, [0.0, 1.0]).all()):
        raise ValueError("Target values must contain only non-null 0/1.")
    return arr


def rng_for(key, seed: int = SEED) -> np.random.Generator:
    """Create a deterministic RNG seeded by SHA-256 of key."""
    digest = hashlib.sha256(str(key).encode("utf-8")).digest()
    return np.random.default_rng(seed + int.from_bytes(digest[:4], "little"))


def wilson_ci(accepted: int, n: int) -> tuple[float, float]:
    """95% Wilson score interval in percent [0, 100]."""
    if n == 0:
        return np.nan, np.nan
    z = NormalDist().inv_cdf(0.975)
    p = accepted / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = z * np.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
    low = 0.0 if accepted == 0 else max(0.0, center - half) * 100.0
    high = 100.0 if accepted == n else min(1.0, center + half) * 100.0
    return float(low), float(high)


def bootstrap_rate_ci(values, n_boot: int = N_BOOT, seed: int = SEED) -> tuple[float, float]:
    """95% percentile bootstrap CI in percent [0, 100] for binary values."""
    arr = validate_binary(values)
    n = len(arr)
    if n == 0:
        return np.nan, np.nan
    if np.all(arr == arr[0]):
        val = float(arr[0] * 100.0)
        return val, val
    rng = np.random.default_rng(seed)
    draws = rng.binomial(n, float(arr.mean()), n_boot) / n * 100.0
    low, high = np.percentile(draws, [2.5, 97.5])
    return float(low), float(high)


def bootstrap_diff_ci(values_a, values_b, n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    """Rate difference A - B (percentage points) with 95% bootstrap CI."""
    a, b = validate_binary(values_a), validate_binary(values_b)
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return {
            "n_a": na, "n_b": nb,
            "rate_a_pct": round(float(a.mean() * 100.0), 2) if na else np.nan,
            "rate_b_pct": round(float(b.mean() * 100.0), 2) if nb else np.nan,
            "diff_pp": np.nan, "ci_low_pp": np.nan, "ci_high_pp": np.nan,
        }
    ra, rb = float(a.mean() * 100.0), float(b.mean() * 100.0)
    rng = np.random.default_rng(seed)
    draws = (rng.binomial(na, a.mean(), n_boot) / na - rng.binomial(nb, b.mean(), n_boot) / nb) * 100.0
    low, high = np.percentile(draws, [2.5, 97.5])
    return {
        "n_a": na, "n_b": nb,
        "rate_a_pct": round(ra, 2), "rate_b_pct": round(rb, 2),
        "diff_pp": round(ra - rb, 2), "ci_low_pp": round(float(low), 2), "ci_high_pp": round(float(high), 2),
    }


def rate_table(df: pd.DataFrame, cols, ci_method: str = "wilson", target: str = "Y",
               min_n: int = MIN_N, n_boot: int = N_BOOT, seed: int = SEED) -> pd.DataFrame:
    """Summarize n, accepted count, rate (%), and 95% CI per group."""
    if not cols:
        raise ValueError("cols cannot be empty.")
    if ci_method not in {"wilson", "bootstrap"}:
        raise ValueError("ci_method must be 'wilson' or 'bootstrap'.")

    validate_binary(df[target])
    rows = []
    for idx, (keys, sub) in enumerate(df.groupby(list(cols), observed=True, dropna=False)):
        keys = keys if isinstance(keys, tuple) else (keys,)
        y = sub[target].to_numpy(dtype=float)
        n = len(y)
        accepted = int(y.sum()) if n else 0
        rate = float(y.mean() * 100.0) if n else np.nan
        low, high = wilson_ci(accepted, n) if ci_method == "wilson" else bootstrap_rate_ci(y, n_boot, seed + idx)
        rows.append({
            **dict(zip(cols, keys)), "n": n, "accepted": accepted,
            "rate_pct": round(rate, 2) if n else np.nan,
            "ci_low_pct": round(low, 2) if n else np.nan,
            "ci_high_pct": round(high, 2) if n else np.nan,
            "small_n": n < min_n,
        })
    return pd.DataFrame(rows)


def contrasts(df: pd.DataFrame, strata_cols, exposure: str, group_a, group_b, target: str = "Y",
              min_n: int = MIN_N, n_boot: int = N_BOOT, seed: int = SEED, key="contrast") -> pd.DataFrame:
    """Difference group_a - group_b (pp) with 95% bootstrap CI per stratum."""
    validate_binary(df[target])
    grouped = df.groupby(list(strata_cols), observed=True, dropna=False) if strata_cols else [((), df)]
    rows = []
    for labels, part in grouped:
        labels = labels if isinstance(labels, tuple) else (labels,)
        ya = part.loc[part[exposure] == group_a, target]
        yb = part.loc[part[exposure] == group_b, target]
        na, nb = len(ya), len(yb)
        small = min(na, nb) < min_n
        sub_seed = int(rng_for((key, labels, group_a, group_b), seed).integers(0, 2**31 - 1))
        diff = bootstrap_diff_ci(ya, yb, n_boot=n_boot, seed=sub_seed) if (na and nb) else bootstrap_diff_ci(ya, yb)
        status = "no_common_support" if (na == 0 or nb == 0) else ("small_n" if small else "ok")
        rows.append({
            **dict(zip(strata_cols, labels)),
            "group_a": str(group_a), "group_b": str(group_b),
            "accepted_a": int(ya.sum()) if na else 0, "accepted_b": int(yb.sum()) if nb else 0,
            **diff, "small_n": small, "status": status,
        })
    return pd.DataFrame(rows)


def standardized_contrast(strata_df: pd.DataFrame, min_n: int = MIN_N,
                          n_boot: int = N_BOOT, seed: int = SEED, key="standardized") -> dict:
    """Sample-weighted average difference across strata with n >= min_n in both arms."""
    keep = strata_df.loc[(strata_df["n_a"] >= min_n) & (strata_df["n_b"] >= min_n)]
    total_n = int((strata_df["n_a"] + strata_df["n_b"]).sum())
    used_n = int((keep["n_a"] + keep["n_b"]).sum())
    summary = {
        "n_strata_total": len(strata_df), "n_strata_used": len(keep),
        "n_comparison_total": total_n, "n_comparison_used": used_n,
        "coverage": round(used_n / total_n, 4) if total_n else np.nan,
    }
    if keep.empty:
        return {**summary, "diff_pp": np.nan, "ci_low_pp": np.nan, "ci_high_pp": np.nan, "status": "no_common_support"}

    weights = (keep["n_a"] + keep["n_b"]).to_numpy() / used_n
    rng = rng_for(key, seed)
    draws = np.zeros(n_boot)
    for w, row in zip(weights, keep.itertuples()):
        draws += w * (rng.binomial(row.n_a, row.rate_a_pct / 100.0, n_boot) / row.n_a
                      - rng.binomial(row.n_b, row.rate_b_pct / 100.0, n_boot) / row.n_b)
    low, high = np.quantile(draws * 100.0, [0.025, 0.975])
    return {
        **summary,
        "diff_pp": round(float(np.dot(weights, keep["diff_pp"])), 2),
        "ci_low_pp": round(float(low), 2),
        "ci_high_pp": round(float(high), 2),
        "status": "ok",
    }


def pivot_expiration(df: pd.DataFrame, index_cols=("time",), target: str = "Y"):
    """Build rate pivot (%), count pivot (n), and melted long DataFrame for 2h vs 1d (D2)."""
    work = df.copy()
    if "time" in work.columns:
        work["time"] = pd.Categorical(work["time"], categories=TIME_ORDER, ordered=True)
    work["expiration"] = pd.Categorical(work["expiration"], categories=EXPIRATION_ORDER, ordered=True)

    counts = work.pivot_table(index=list(index_cols), columns="expiration", values=target, aggfunc="count", observed=False).fillna(0).astype(int)
    rates = (work.pivot_table(index=list(index_cols), columns="expiration", values=target, aggfunc="mean", observed=False) * 100.0).reindex(counts.index).round(2)
    rates["diff_1d_minus_2h_pp"] = (rates["1d"] - rates["2h"]).round(2)

    long_r = rates[["2h", "1d"]].reset_index().melt(list(index_cols), ["2h", "1d"], "expiration", "rate_pct")
    long_c = counts[["2h", "1d"]].reset_index().melt(list(index_cols), ["2h", "1d"], "expiration", "n")
    return rates, counts, long_r.merge(long_c, on=[*index_cols, "expiration"], how="left")


def _cluster_rate_fn(data: pd.DataFrame, group_col: str, strata_cols=(), target: str = "Y"):
    group_code = data[group_col].cat.codes.to_numpy()
    n_groups = len(data[group_col].cat.categories)
    stratum_code = data.groupby(list(strata_cols), observed=True).ngroup().to_numpy() if strata_cols else np.zeros(len(data), dtype=int)
    n_strata = stratum_code.max() + 1
    y = data[target].to_numpy()
    cell_code = group_code * n_strata + stratum_code
    n_cells = n_groups * n_strata

    def fn(weights: np.ndarray) -> np.ndarray:
        accepted = np.bincount(cell_code, weights=weights * y, minlength=n_cells)
        total = np.bincount(cell_code, weights=weights, minlength=n_cells)
        with np.errstate(invalid="ignore", divide="ignore"):
            cell_rate = (accepted / total).reshape(n_groups, n_strata)
        share = np.bincount(stratum_code, weights=weights, minlength=n_strata) / weights.sum()
        return 100.0 * cell_rate @ share

    return fn


def _cluster_draws(data: pd.DataFrame, fn, unit: str = "respondent", id_col: str = "respondent_id",
                   n_boot: int = N_BOOT, seed: int = SEED):
    rng = np.random.default_rng(seed)
    unit_idx = pd.factorize(data[id_col])[0] if unit == "respondent" else np.arange(len(data))
    n_units = unit_idx.max() + 1
    probs = np.full(n_units, 1.0 / n_units)
    point = fn(np.ones(len(data)))
    draws = np.array([fn(rng.multinomial(n_units, probs)[unit_idx].astype(float)) for _ in range(n_boot)])
    return point, draws


def cluster_rates_ci(data: pd.DataFrame, group_col: str, strata_cols=(), unit: str = "respondent",
                     id_col: str = "respondent_id", target: str = "Y",
                     n_boot: int = N_BOOT, seed: int = SEED) -> pd.DataFrame:
    """Group rates (%) with 95% respondent-clustered bootstrap CI."""
    point, draws = _cluster_rate_fn(data, group_col, strata_cols, target), None
    point, draws = _cluster_draws(data, point, unit, id_col, n_boot, seed)
    low, high = np.nanpercentile(draws, [2.5, 97.5], axis=0)
    return pd.DataFrame(
        {"rate_pct": np.round(point, 2), "ci_low_pct": np.round(low, 2), "ci_high_pct": np.round(high, 2)},
        index=data[group_col].cat.categories,
    )


def cluster_diff_ci(data: pd.DataFrame, group_col: str, group_a: str, group_b: str, strata_cols=(),
                    unit: str = "respondent", id_col: str = "respondent_id", target: str = "Y",
                    n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    """Standardized rate difference group_a - group_b (pp) with 95% cluster-bootstrap CI."""
    cats = list(data[group_col].cat.categories)
    a, b = cats.index(group_a), cats.index(group_b)
    point, draws = _cluster_draws(data, _cluster_rate_fn(data, group_col, strata_cols, target), unit, id_col, n_boot, seed)
    diff_draws = draws[:, a] - draws[:, b]
    low, high = np.nanpercentile(diff_draws, [2.5, 97.5])
    return {
        "rate_a_pct": round(float(point[a]), 1), "rate_b_pct": round(float(point[b]), 1),
        "diff_pp": round(float(point[a] - point[b]), 1),
        "ci_low_pp": round(float(low), 1), "ci_high_pp": round(float(high), 1),
        "empty_strata_draws": int(np.isnan(diff_draws).sum()),
    }
