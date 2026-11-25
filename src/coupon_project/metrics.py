"""Thong ke nhom va bootstrap CI 95% dung chung cho Q1-Q5."""
import numpy as np
import pandas as pd

MIN_N = 30
N_BOOT = 2000
SEED = 42


def _clean_binary(values):
    """Chuyen ve mang 0/1 va bo NaN."""
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if arr.size > 0 and not np.all(np.isin(arr, [0.0, 1.0])):
        raise ValueError("Cot muc tieu chi duoc chua 0 va 1.")
    return arr


def rate_ci(values, n_boot=N_BOOT, seed=SEED):
    """Bootstrap CI 95% (%) cho mot ty le 0/1."""
    arr = _clean_binary(values)
    n = len(arr)
    if n == 0:
        return np.nan, np.nan
    if np.all(arr == arr[0]):
        val = float(arr[0] * 100.0)
        return val, val

    rng = np.random.default_rng(seed)
    boots = [rng.choice(arr, size=n, replace=True).mean() * 100.0 for _ in range(n_boot)]
    low, high = np.percentile(boots, [2.5, 97.5])
    return float(low), float(high)


def diff_ci(values_a, values_b, n_boot=N_BOOT, seed=SEED):
    """Chenh lech rate(A) - rate(B) (diem %) va bootstrap CI 95%."""
    a, b = _clean_binary(values_a), _clean_binary(values_b)
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return {
            "n_a": na, "n_b": nb,
            "rate_a_pct": float(a.mean() * 100.0) if na else np.nan,
            "rate_b_pct": float(b.mean() * 100.0) if nb else np.nan,
            "diff_pp": np.nan, "ci_low_pp": np.nan, "ci_high_pp": np.nan,
        }

    ra, rb = float(a.mean() * 100.0), float(b.mean() * 100.0)
    rng = np.random.default_rng(seed)
    diffs = [(rng.choice(a, na, True).mean() - rng.choice(b, nb, True).mean()) * 100.0
             for _ in range(n_boot)]
    low, high = np.percentile(diffs, [2.5, 97.5])
    return {"n_a": na, "n_b": nb, "rate_a_pct": ra, "rate_b_pct": rb,
            "diff_pp": ra - rb, "ci_low_pp": float(low), "ci_high_pp": float(high)}


def group_summary(df, cols, target="Y", min_n=MIN_N, n_boot=N_BOOT, seed=SEED):
    """Tong hop n, so chap nhan, ty le (%) va CI 95% theo nhom."""
    if not cols:
        raise ValueError("Can it nhat mot cot de nhom du lieu.")

    rows = []
    for idx, (keys, sub) in enumerate(df.groupby(list(cols), observed=True, dropna=False)):
        if not isinstance(keys, tuple):
            keys = (keys,)
        y = _clean_binary(sub[target])
        n = len(y)
        rate = y.mean() * 100.0 if n else np.nan
        low, high = rate_ci(y, n_boot=n_boot, seed=seed + idx)
        row = dict(zip(cols, keys))
        row.update(
            n=n, accepted=int(y.sum()) if n else 0,
            rate_pct=float(np.round(rate, 2)),
            ci_low_pct=float(np.round(low, 2)),
            ci_high_pct=float(np.round(high, 2)),
            small_sample=n < min_n,
        )
        rows.append(row)
    return pd.DataFrame(rows)


def compare_groups(df, mask_a, mask_b, label_a, label_b, target="Y",
                   min_n=MIN_N, n_boot=N_BOOT, seed=SEED):
    """So sanh ty le 2 nhom (A - B, diem %) kem CI 95%."""
    s = diff_ci(df.loc[mask_a, target], df.loc[mask_b, target], n_boot=n_boot, seed=seed)
    return {
        "group_a": label_a, "group_b": label_b,
        "n_a": s["n_a"], "n_b": s["n_b"],
        "rate_a_pct": float(np.round(s["rate_a_pct"], 2)),
        "rate_b_pct": float(np.round(s["rate_b_pct"], 2)),
        "diff_pp": float(np.round(s["diff_pp"], 2)),
        "ci_low_pp": float(np.round(s["ci_low_pp"], 2)),
        "ci_high_pp": float(np.round(s["ci_high_pp"], 2)),
        "small_sample": min(s["n_a"], s["n_b"]) < min_n,
    }
