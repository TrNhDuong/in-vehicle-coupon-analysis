"""Ham thong ke mo ta, Wilson CI va bootstrap cho EDA, Q3 va Q4."""
import hashlib
from statistics import NormalDist

import numpy as np
import pandas as pd

MIN_N = 30
SEED = 17104
N_BOOT = 10000
FREQUENCIES = ["never", "less1", "1~3", "4~8", "gt8"]

COUPON_FREQUENCY = {
    "Bar": "Bar",
    "Coffee House": "CoffeeHouse",
    "Carry out & Take away": "CarryAway",
    "Restaurant(<20)": "RestaurantLessThan20",
    "Restaurant(20-50)": "Restaurant20To50",
}
COUPONS = list(COUPON_FREQUENCY)
PASSENGERS = ["Alone", "Friend(s)", "Partner", "Kid(s)"]
DESTINATIONS = ["No Urgent Place", "Home", "Work"]


def validate_binary(frame):
    """Kiem tra cot Y chi gom 0 va 1."""
    if frame["Y"].isna().any() or not frame["Y"].isin([0, 1]).all():
        raise ValueError("Y must contain only observed 0/1 values")


def wilson(accepted, n):
    """Khoang tin cay Wilson 95% (don vi [0, 1])."""
    if n == 0:
        return np.nan, np.nan
    z = NormalDist().inv_cdf(0.975)
    p = accepted / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    low = 0.0 if accepted == 0 else max(0.0, center - half)
    high = 1.0 if accepted == n else min(1.0, center + half)
    return low, high


def rate_table(frame, groups):
    """Tong hop n, so chap nhan, ty le va Wilson CI 95% theo nhom."""
    validate_binary(frame)
    res = frame.groupby(groups, observed=True, dropna=False)["Y"].agg(
        n="size", accepted="sum", rate="mean"
    ).reset_index()
    cis = [wilson(k, n) for k, n in zip(res["accepted"], res["n"])]
    res["ci_low"] = [c[0] for c in cis]
    res["ci_high"] = [c[1] for c in cis]
    res["small_n"] = res["n"] < MIN_N
    return res


def matched_frequency(frame):
    """Anh xa loai coupon sang cot tan suat tuong ung (giu nguyen NaN)."""
    unknown = set(frame["coupon"].dropna()) - set(COUPON_FREQUENCY)
    if unknown or frame["coupon"].isna().any():
        raise ValueError(f"Unmapped or missing coupon labels: {sorted(unknown)}")

    res = pd.Series(pd.NA, index=frame.index, dtype="string", name="matched_frequency")
    for coupon, col in COUPON_FREQUENCY.items():
        mask = frame["coupon"].eq(coupon)
        if not mask.any():
            continue
        vals = frame.loc[mask, col]
        if not vals.dropna().isin(FREQUENCIES).all():
            raise ValueError(f"Unexpected frequency label in {col}")
        res.loc[mask] = vals.astype("string")
    return res


def rng_for(key):
    """Tao RNG co dinh theo key de chay lai ra dung ket qua."""
    digest = hashlib.sha256(str(key).encode("utf-8")).digest()
    return np.random.default_rng(SEED + int.from_bytes(digest[:4], "little"))


def contrasts(frame, groups, exposure, group_a, group_b, key="contrast"):
    """Chenh lech ty le (group_a - group_b, diem %) va bootstrap CI 95% theo tang."""
    validate_binary(frame)
    strata = frame.groupby(groups, observed=True, dropna=False) if groups else [((), frame)]

    rows = []
    for labels, part in strata:
        if not isinstance(labels, tuple):
            labels = (labels,)
        ya = part.loc[part[exposure].eq(group_a), "Y"]
        yb = part.loc[part[exposure].eq(group_b), "Y"]
        na, nb = len(ya), len(yb)
        small_n = min(na, nb) < MIN_N

        row = dict(zip(groups, labels))
        row.update(
            group_a=group_a, group_b=group_b, n_a=na, n_b=nb,
            accepted_a=int(ya.sum()), accepted_b=int(yb.sum()),
            rate_a=ya.mean(), rate_b=yb.mean(), small_n=small_n,
        )
        if na and nb:
            rng = rng_for((key, labels, group_a, group_b))
            draws = (rng.binomial(na, ya.mean(), N_BOOT) / na
                     - rng.binomial(nb, yb.mean(), N_BOOT) / nb) * 100
            low, high = np.quantile(draws, [0.025, 0.975])
            row.update(diff_pp=(ya.mean() - yb.mean()) * 100,
                       ci_low_pp=low, ci_high_pp=high,
                       status="small_n" if small_n else "ok")
        else:
            row.update(diff_pp=np.nan, ci_low_pp=np.nan, ci_high_pp=np.nan,
                       status="no_common_support")
        rows.append(row)
    return pd.DataFrame(rows)


def standardized_contrast(strata, key="standardized"):
    """Chenh lech gop theo trong so co mau tren cac tang co n >= MIN_N o ca 2 nhom."""
    keep = strata.loc[(strata["n_a"] >= MIN_N) & (strata["n_b"] >= MIN_N)].copy()
    total_n = int((strata["n_a"] + strata["n_b"]).sum())
    used_n = int((keep["n_a"] + keep["n_b"]).sum())
    summary = {
        "n_strata_total": len(strata), "n_strata_used": len(keep),
        "n_comparison_total": total_n, "n_comparison_used": used_n,
        "coverage": used_n / total_n if total_n else np.nan,
    }
    if keep.empty:
        return {**summary, "diff_pp": np.nan, "ci_low_pp": np.nan,
                "ci_high_pp": np.nan, "status": "no_common_support"}

    weights = (keep["n_a"] + keep["n_b"]).to_numpy() / used_n
    rng = rng_for(key)
    draws = np.zeros(N_BOOT)
    for w, row in zip(weights, keep.itertuples()):
        draws += w * (rng.binomial(row.n_a, row.rate_a, N_BOOT) / row.n_a
                      - rng.binomial(row.n_b, row.rate_b, N_BOOT) / row.n_b)
    low, high = np.quantile(draws * 100, [0.025, 0.975])
    return {**summary, "diff_pp": float(np.dot(weights, keep["diff_pp"])),
            "ci_low_pp": low, "ci_high_pp": high, "status": "ok"}


def audit_row(action, before, after, reason):
    """Ghi log so dong truoc/sau."""
    return {"action": action, "n_before": before, "n_after": after,
            "rows_removed": before - after, "reason": reason}


def save_table(table, root, name):
    """Luu CSV vao reports/tables/."""
    path = root / "reports" / "tables" / f"ha_{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def save_figure(fig, root, name):
    """Luu PNG vao reports/figures/."""
    path = root / "reports" / "figures" / f"ha_{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    return path


def heatmap_rates(table, row, column, row_order, col_order, ax, title):
    """Ve heatmap ty le (%) kem n va dau * neu n < MIN_N."""
    import matplotlib.pyplot as plt

    rates = table.pivot(index=row, columns=column, values="rate").reindex(index=row_order, columns=col_order)
    counts = table.pivot(index=row, columns=column, values="n").reindex(index=row_order, columns=col_order).fillna(0)
    cmap = plt.get_cmap("Blues").copy()
    cmap.set_bad("#F1F5F9")

    img = ax.imshow(rates.to_numpy(dtype=float) * 100, vmin=0, vmax=100, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(col_order)), col_order, rotation=25, ha="right")
    ax.set_yticks(range(len(row_order)), row_order)
    ax.set(xlabel=column, ylabel=row, title=title)

    for i in range(len(row_order)):
        for j in range(len(col_order)):
            n_val, rate_val = int(counts.iloc[i, j]), rates.iloc[i, j]
            if n_val == 0:
                ax.text(j, i, "No data\nn=0", ha="center", va="center", fontsize=8, color="#475569")
            else:
                star = "*" if n_val < MIN_N else ""
                color = "white" if pd.notna(rate_val) and rate_val > 0.6 else "black"
                ax.text(j, i, f"{rate_val * 100:.1f}%\nn={n_val}{star}",
                        ha="center", va="center", fontsize=8, color=color)
    return img
