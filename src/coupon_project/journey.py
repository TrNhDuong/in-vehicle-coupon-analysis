"""Ham xu ly cho Q1 (khoang cach/huong) va Q2 (thoi han/khung gio)."""
import pandas as pd

from .metrics import MIN_N, N_BOOT, SEED, compare_groups

TRAVEL_BAND_ORDER = ["5-<15 min", "15-<25 min", ">=25 min"]
TIME_ORDER = ["7AM", "10AM", "2PM", "6PM", "10PM"]
EXPIRATION_ORDER = ["2h", "1d"]


def check_flags(df):
    """Kiem tra logic co thoi gian va huong di."""
    invalid = (df["toCoupon_GEQ25min"] == 1) & (df["toCoupon_GEQ15min"] == 0)
    return {
        "n_rows": len(df),
        "geq5_always_one": bool((df["toCoupon_GEQ5min"] == 1).all()),
        "invalid_geq_hierarchy_count": int(invalid.sum()),
        "direction_complement_ok": bool((df["direction_same"] + df["direction_opp"] == 1).all()),
    }


def add_time_band(df, col_name="travel_time_band"):
    """Tao bien travel_time_band (D3) tu GEQ15min va GEQ25min."""
    if check_flags(df)["invalid_geq_hierarchy_count"] > 0:
        raise ValueError("Co dong bat hop ly: GEQ25 == 1 nhung GEQ15 == 0.")
    out = df.copy()
    band = pd.Series("15-<25 min", index=out.index)
    band[out["toCoupon_GEQ15min"] == 0] = "5-<15 min"
    band[out["toCoupon_GEQ25min"] == 1] = ">=25 min"
    out[col_name] = pd.Categorical(band, categories=TRAVEL_BAND_ORDER, ordered=True)
    return out


def _diff_by_strata(df, by, col, val_a, val_b, label_a, label_b,
                    min_n=MIN_N, n_boot=N_BOOT, seed=SEED):
    """Chenh lech rate(val_a) - rate(val_b) kem CI 95% trong tung tang."""
    if not by:
        return pd.DataFrame([compare_groups(
            df, df[col] == val_a, df[col] == val_b, label_a, label_b,
            min_n=min_n, n_boot=n_boot, seed=seed,
        )])

    rows = []
    for idx, (keys, sub) in enumerate(df.groupby(list(by), observed=True, dropna=False)):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(by, keys))
        row.update(compare_groups(
            sub, sub[col] == val_a, sub[col] == val_b, label_a, label_b,
            min_n=min_n, n_boot=n_boot, seed=seed + idx,
        ))
        rows.append(row)
    return pd.DataFrame(rows)


def q1_distance_diff(df, by=(), min_n=MIN_N, n_boot=N_BOOT, seed=SEED):
    """So sanh nhom gan (5-<15 min) voi nhom xa (>=25 min)."""
    return _diff_by_strata(
        df, list(by), "travel_time_band", "5-<15 min", ">=25 min",
        "5-<15 min", ">=25 min", min_n, n_boot, seed,
    )


def q1_direction_diff(df, by=(), min_n=MIN_N, n_boot=N_BOOT, seed=SEED):
    """So sanh cung huong (1) voi khac huong (0)."""
    return _diff_by_strata(
        df, list(by), "direction_same", 1, 0,
        "same_direction (1)", "opposite_or_na (0)", min_n, n_boot, seed,
    )


def q2_pivots(df, index_cols=("time",), target="Y"):
    """Tao pivot table ty le (%), so mau (n) va bang melt (D2)."""
    work = df.copy()
    if "time" in work.columns:
        work["time"] = pd.Categorical(work["time"], categories=TIME_ORDER, ordered=True)
    work["expiration"] = pd.Categorical(work["expiration"], categories=EXPIRATION_ORDER, ordered=True)

    counts = work.pivot_table(
        index=list(index_cols), columns="expiration", values=target, aggfunc="count", observed=False
    ).fillna(0).astype(int)
    rates = (work.pivot_table(
        index=list(index_cols), columns="expiration", values=target, aggfunc="mean", observed=False
    ) * 100.0).reindex(counts.index).round(2)
    rates["diff_1d_minus_2h_pp"] = (rates["1d"] - rates["2h"]).round(2)

    long_r = rates[["2h", "1d"]].reset_index().melt(list(index_cols), ["2h", "1d"], "expiration", "rate_pct")
    long_c = counts[["2h", "1d"]].reset_index().melt(list(index_cols), ["2h", "1d"], "expiration", "n")
    return rates, counts, long_r.merge(long_c, on=[*index_cols, "expiration"], how="left")


def q2_expiry_diff(df, by=(), min_n=MIN_N, n_boot=N_BOOT, seed=SEED):
    """Tinh chenh lech 1d - 2h (diem %) kem CI 95% theo tang."""
    work = df.copy()
    if "time" in work.columns:
        work["time"] = pd.Categorical(work["time"], categories=TIME_ORDER, ordered=True)
    return _diff_by_strata(work, list(by), "expiration", "1d", "2h", "1d", "2h", min_n, n_boot, seed)
