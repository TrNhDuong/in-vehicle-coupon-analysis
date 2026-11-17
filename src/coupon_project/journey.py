"""Cac ham xu ly cho Q1 (khoang cach/huong) va Q2 (thoi han/khung gio)."""
import pandas as pd

from .metrics import MIN_N, N_BOOT, SEED, compare_groups

TRAVEL_BAND_ORDER = ["5-<15 min", "15-<25 min", ">=25 min"]
TIME_ORDER = ["7AM", "10AM", "2PM", "6PM", "10PM"]
EXPIRATION_ORDER = ["2h", "1d"]


def check_flags(df: pd.DataFrame) -> dict:
    """Kiem tra tinh nhat quan cua co nguong thoi gian va huong di."""
    invalid = (df["toCoupon_GEQ25min"] == 1) & (df["toCoupon_GEQ15min"] == 0)
    return {
        "n_rows": len(df),
        "geq5_always_one": bool((df["toCoupon_GEQ5min"] == 1).all()),
        "invalid_geq_hierarchy_count": int(invalid.sum()),
        "direction_complement_ok": bool((df["direction_same"] + df["direction_opp"] == 1).all()),
    }


def add_time_band(df: pd.DataFrame, col_name: str = "travel_time_band") -> pd.DataFrame:
    """Tao bien travel_time_band (D3) tu toCoupon_GEQ15min va toCoupon_GEQ25min."""
    if check_flags(df)["invalid_geq_hierarchy_count"] > 0:
        raise ValueError("Co dong bat hop ly: toCoupon_GEQ25min == 1 nhung toCoupon_GEQ15min == 0.")

    out = df.copy()
    band = pd.Series("15-<25 min", index=out.index)
    band[out["toCoupon_GEQ15min"] == 0] = "5-<15 min"
    band[out["toCoupon_GEQ25min"] == 1] = ">=25 min"
    out[col_name] = pd.Categorical(band, categories=TRAVEL_BAND_ORDER, ordered=True)
    return out


def _diff_by_strata(
    df: pd.DataFrame,
    by: list[str],
    col: str,
    val_a,
    val_b,
    label_a: str,
    label_b: str,
    min_n: int = MIN_N,
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> pd.DataFrame:
    """Tinh chenh lech rate(val_a) - rate(val_b) kem 95% CI trong tung nhom."""
    if not by:
        res = compare_groups(
            df, df[col] == val_a, df[col] == val_b, label_a, label_b,
            min_n=min_n, n_boot=n_boot, seed=seed,
        )
        return pd.DataFrame([res])

    rows = []
    for idx, (keys, sub) in enumerate(df.groupby(list(by), observed=True, dropna=False)):
        if not isinstance(keys, tuple):
            keys = (keys,)
        res = compare_groups(
            sub, sub[col] == val_a, sub[col] == val_b, label_a, label_b,
            min_n=min_n, n_boot=n_boot, seed=seed + idx,
        )
        row = dict(zip(by, keys))
        row.update(res)
        rows.append(row)
    return pd.DataFrame(rows)


def q1_distance_diff(
    df: pd.DataFrame,
    by: list[str] = (),
    min_n: int = MIN_N,
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> pd.DataFrame:
    """So sanh nhom gan (5-<15 min) voi nhom xa (>=25 min) trong tung tang (D4, D5)."""
    return _diff_by_strata(
        df, list(by), "travel_time_band", "5-<15 min", ">=25 min",
        "5-<15 min", ">=25 min", min_n=min_n, n_boot=n_boot, seed=seed,
    )


def q1_direction_diff(
    df: pd.DataFrame,
    by: list[str] = (),
    min_n: int = MIN_N,
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> pd.DataFrame:
    """So sanh cung huong (1) voi khac huong (0) trong tung tang."""
    return _diff_by_strata(
        df, list(by), "direction_same", 1, 0,
        "same_direction (1)", "opposite_or_na (0)", min_n=min_n, n_boot=n_boot, seed=seed,
    )


def q2_pivots(df: pd.DataFrame, index_cols: tuple[str, ...] = ("time",), target: str = "Y"):
    """Tao pivot table ty le (%), so mau (n) va bang dang dai bang melt (D2)."""
    work = df.copy()
    if "time" in work.columns:
        work["time"] = pd.Categorical(work["time"], categories=TIME_ORDER, ordered=True)
    work["expiration"] = pd.Categorical(work["expiration"], categories=EXPIRATION_ORDER, ordered=True)

    counts = (
        work.pivot_table(index=list(index_cols), columns="expiration", values=target, aggfunc="count", observed=False)
        .fillna(0)
        .astype(int)
    )
    rates = (
        work.pivot_table(index=list(index_cols), columns="expiration", values=target, aggfunc="mean", observed=False)
        * 100.0
    ).reindex(counts.index).round(2)
    rates["diff_1d_minus_2h_pp"] = (rates["1d"] - rates["2h"]).round(2)

    long_rates = rates[["2h", "1d"]].reset_index().melt(
        id_vars=list(index_cols), value_vars=["2h", "1d"], var_name="expiration", value_name="rate_pct"
    )
    long_counts = counts[["2h", "1d"]].reset_index().melt(
        id_vars=list(index_cols), value_vars=["2h", "1d"], var_name="expiration", value_name="n"
    )
    long_df = long_rates.merge(long_counts, on=[*index_cols, "expiration"], how="left")
    return rates, counts, long_df


def q2_expiry_diff(
    df: pd.DataFrame,
    by: list[str] = (),
    min_n: int = MIN_N,
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> pd.DataFrame:
    """Tinh chenh lech 1d - 2h (diem %) kem 95% bootstrap CI theo tung tang (D4, D5)."""
    work = df.copy()
    if "time" in work.columns:
        work["time"] = pd.Categorical(work["time"], categories=TIME_ORDER, ordered=True)
    return _diff_by_strata(
        work, list(by), "expiration", "1d", "2h",
        "1d", "2h", min_n=min_n, n_boot=n_boot, seed=seed,
    )
