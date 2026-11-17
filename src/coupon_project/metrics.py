"""Cac ham thong ke nhom va khoang tin cay bootstrap 95% dung chung cho Q1-Q5."""
import numpy as np
import pandas as pd

MIN_N = 30
N_BOOT = 2000
SEED = 42


def _clean_binary(values) -> np.ndarray:
    """Chuyen du lieu ve mang 0/1 va bo qua NaN."""
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if arr.size > 0 and not np.all(np.isin(arr, [0.0, 1.0])):
        raise ValueError("Cot muc tieu chi duoc chua gia tri 0 va 1.")
    return arr


def rate_ci(values, n_boot: int = N_BOOT, seed: int = SEED):
    """Tinh khoang tin cay bootstrap 95% (%) cho mot ty le 0/1."""
    arr = _clean_binary(values)
    n = len(arr)
    if n == 0:
        return (np.nan, np.nan)
    if np.all(arr == arr[0]):
        val = float(arr[0] * 100.0)
        return (val, val)

    rng = np.random.default_rng(seed)
    boot_rates = [
        rng.choice(arr, size=n, replace=True).mean() * 100.0
        for _ in range(n_boot)
    ]
    low, high = np.percentile(boot_rates, [2.5, 97.5])
    return (float(low), float(high))


def diff_ci(values_a, values_b, n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    """Tinh chenh lech rate(A) - rate(B) (diem %) va bootstrap CI 95%."""
    arr_a = _clean_binary(values_a)
    arr_b = _clean_binary(values_b)
    n_a, n_b = len(arr_a), len(arr_b)

    if n_a == 0 or n_b == 0:
        return {
            "n_a": n_a,
            "n_b": n_b,
            "rate_a_pct": float(arr_a.mean() * 100.0) if n_a > 0 else np.nan,
            "rate_b_pct": float(arr_b.mean() * 100.0) if n_b > 0 else np.nan,
            "diff_pp": np.nan,
            "ci_low_pp": np.nan,
            "ci_high_pp": np.nan,
        }

    rate_a = float(arr_a.mean() * 100.0)
    rate_b = float(arr_b.mean() * 100.0)

    rng = np.random.default_rng(seed)
    boot_diffs = []
    for _ in range(n_boot):
        mean_a = rng.choice(arr_a, size=n_a, replace=True).mean()
        mean_b = rng.choice(arr_b, size=n_b, replace=True).mean()
        boot_diffs.append((mean_a - mean_b) * 100.0)

    low, high = np.percentile(boot_diffs, [2.5, 97.5])
    return {
        "n_a": n_a,
        "n_b": n_b,
        "rate_a_pct": rate_a,
        "rate_b_pct": rate_b,
        "diff_pp": rate_a - rate_b,
        "ci_low_pp": float(low),
        "ci_high_pp": float(high),
    }


def group_summary(
    df: pd.DataFrame,
    cols: list[str],
    target: str = "Y",
    min_n: int = MIN_N,
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> pd.DataFrame:
    """Tong hop n, so chap nhan, ty le (%) va 95% CI theo tung nhom."""
    if not cols:
        raise ValueError("Can it nhat mot cot de nhom du lieu.")

    rows = []
    for idx, (keys, sub) in enumerate(df.groupby(list(cols), observed=True, dropna=False)):
        if not isinstance(keys, tuple):
            keys = (keys,)

        y = _clean_binary(sub[target])
        n = len(y)
        rate = y.mean() * 100.0 if n > 0 else np.nan
        low, high = rate_ci(y, n_boot=n_boot, seed=seed + idx)

        row = dict(zip(cols, keys))
        row.update(
            {
                "n": n,
                "accepted": int(y.sum()) if n > 0 else 0,
                "rate_pct": float(np.round(rate, 2)),
                "ci_low_pct": float(np.round(low, 2)),
                "ci_high_pct": float(np.round(high, 2)),
                "small_sample": n < min_n,
            }
        )
        rows.append(row)

    return pd.DataFrame(rows)


def compare_groups(
    df: pd.DataFrame,
    mask_a: pd.Series,
    mask_b: pd.Series,
    label_a: str,
    label_b: str,
    target: str = "Y",
    min_n: int = MIN_N,
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> dict:
    """So sanh ty le chap nhan giua 2 nhom (A - B theo diem %) kem CI 95%."""
    stats = diff_ci(df.loc[mask_a, target], df.loc[mask_b, target], n_boot=n_boot, seed=seed)
    return {
        "group_a": label_a,
        "group_b": label_b,
        "n_a": stats["n_a"],
        "n_b": stats["n_b"],
        "rate_a_pct": float(np.round(stats["rate_a_pct"], 2)),
        "rate_b_pct": float(np.round(stats["rate_b_pct"], 2)),
        "diff_pp": float(np.round(stats["diff_pp"], 2)),
        "ci_low_pp": float(np.round(stats["ci_low_pp"], 2)),
        "ci_high_pp": float(np.round(stats["ci_high_pp"], 2)),
        "small_sample": min(stats["n_a"], stats["n_b"]) < min_n,
    }
