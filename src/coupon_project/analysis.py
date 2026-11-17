"""Reproducible descriptive statistics for Ha's EDA/Q3/Q4 draft.

Intervals assume independent survey rows, not independent participants.
No helper fits preprocessing for the ML task.
"""
from __future__ import annotations

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
    if frame["Y"].isna().any() or not frame["Y"].isin([0, 1]).all():
        raise ValueError("Y must contain only observed 0/1 values")


def wilson(accepted, n):
    """95% Wilson interval; an empty cell has no estimated rate."""
    if n == 0:
        return np.nan, np.nan
    z = NormalDist().inv_cdf(0.975)
    p = accepted / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return (0.0 if accepted == 0 else max(0.0, centre - half),
            1.0 if accepted == n else min(1.0, centre + half))


def rate_table(frame, groups):
    """Counts, rates and Wilson intervals; retain missing group labels."""
    validate_binary(frame)
    result = frame.groupby(groups, observed=True, dropna=False)["Y"].agg(
        n="size", accepted="sum", rate="mean"
    ).reset_index()
    intervals = [wilson(k, n) for k, n in zip(result.accepted, result.n)]
    result["ci_low"] = [ci[0] for ci in intervals]
    result["ci_high"] = [ci[1] for ci in intervals]
    result["small_n"] = result.n < MIN_N
    return result


def matched_frequency(frame):
    """Map only exact CSV coupon labels; preserve nulls and reject drift."""
    unknown = set(frame["coupon"].dropna()) - set(COUPON_FREQUENCY)
    if unknown or frame["coupon"].isna().any():
        raise ValueError(f"Unmapped or missing coupon labels: {sorted(unknown)}")
    result = pd.Series(pd.NA, index=frame.index, dtype="string", name="matched_frequency")
    for coupon, column in COUPON_FREQUENCY.items():
        mask = frame["coupon"].eq(coupon)
        if not mask.any():
            continue
        values = frame.loc[mask, column]
        if not values.dropna().isin(FREQUENCIES).all():
            raise ValueError(f"Unexpected frequency label in {column}")
        result.loc[mask] = values.astype("string")
    return result


def rng_for(key):
    digest = hashlib.sha256(str(key).encode("utf-8")).digest()
    return np.random.default_rng(SEED + int.from_bytes(digest[:4], "little"))


def contrasts(frame, groups, exposure, a, b, key="contrast"):
    """A minus B, percentile bootstrap, separately within each stratum.

    For binary outcomes the bootstrap of a mean is exactly a binomial
    draw with p equal to the observed mean. Counts are held fixed.
    Missing exposure is excluded explicitly by the caller, never filled here.
    """
    validate_binary(frame)
    iterable = frame.groupby(groups, observed=True, dropna=False) if groups else [((), frame)]
    rows = []
    for labels, part in iterable:
        labels = labels if isinstance(labels, tuple) else (labels,)
        row = dict(zip(groups, labels))
        ya = part.loc[part[exposure].eq(a), "Y"]
        yb = part.loc[part[exposure].eq(b), "Y"]
        na, nb = len(ya), len(yb)
        row.update(group_a=a, group_b=b, n_a=na, n_b=nb,
                   accepted_a=int(ya.sum()), accepted_b=int(yb.sum()),
                   rate_a=ya.mean(), rate_b=yb.mean(),
                   small_n=min(na, nb) < MIN_N)
        if na and nb:
            rng = rng_for((key, labels, a, b))
            draws = (rng.binomial(na, ya.mean(), N_BOOT) / na
                     - rng.binomial(nb, yb.mean(), N_BOOT) / nb) * 100
            low, high = np.quantile(draws, [0.025, 0.975])
            row.update(diff_pp=(ya.mean() - yb.mean()) * 100,
                       ci_low_pp=low, ci_high_pp=high,
                       status="small_n" if row["small_n"] else "ok")
        else:
            row.update(diff_pp=np.nan, ci_low_pp=np.nan, ci_high_pp=np.nan,
                       status="no_common_support")
        rows.append(row)
    return pd.DataFrame(rows)


def standardized_contrast(strata, key="standardized"):
    """Fixed pooled-n weights on strata with >=MIN_N in BOTH groups.

    The estimand covers common-support strata only, not the entire dataset.
    Bootstrap conditions on observed strata sizes and weights.
    """
    keep = strata.loc[(strata.n_a >= MIN_N) & (strata.n_b >= MIN_N)].copy()
    total = int((strata.n_a + strata.n_b).sum())
    retained = int((keep.n_a + keep.n_b).sum())
    result = dict(n_strata_total=len(strata), n_strata_used=len(keep),
                  n_comparison_total=total, n_comparison_used=retained,
                  coverage=retained / total if total else np.nan)
    if keep.empty:
        return {**result, "diff_pp": np.nan, "ci_low_pp": np.nan,
                "ci_high_pp": np.nan, "status": "no_common_support"}
    weights = (keep.n_a + keep.n_b).to_numpy() / retained
    rng = rng_for(key)
    draws = np.zeros(N_BOOT)
    for weight, row in zip(weights, keep.itertuples()):
        draws += weight * (rng.binomial(row.n_a, row.rate_a, N_BOOT) / row.n_a
                           - rng.binomial(row.n_b, row.rate_b, N_BOOT) / row.n_b)
    low, high = np.quantile(draws * 100, [0.025, 0.975])
    return {**result, "diff_pp": float(np.dot(weights, keep.diff_pp)),
            "ci_low_pp": low, "ci_high_pp": high, "status": "ok"}


def audit_row(action, before, after, reason):
    return dict(action=action, n_before=before, n_after=after,
                rows_removed=before - after, reason=reason)


def save_table(table, root, name):
    path = root / "reports" / "tables" / f"ha_{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def save_figure(fig, root, name):
    path = root / "reports" / "figures" / f"ha_{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    return path


def heatmap_rates(table, row, column, row_order, col_order, ax, title):
    """Show empty cells as no data, with n and explicit small-n markers."""
    rates = table.pivot(index=row, columns=column, values="rate").reindex(
        index=row_order, columns=col_order
    )
    counts = table.pivot(index=row, columns=column, values="n").reindex(
        index=row_order, columns=col_order
    ).fillna(0)
    img = ax.imshow(rates.to_numpy(dtype=float) * 100, vmin=0, vmax=100,
                    cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(col_order)), col_order, rotation=25, ha="right")
    ax.set_yticks(range(len(row_order)), row_order)
    ax.set_xlabel(column)
    ax.set_ylabel(row)
    ax.set_title(title)
    for i in range(len(row_order)):
        for j in range(len(col_order)):
            n, rate = int(counts.iloc[i, j]), rates.iloc[i, j]
            label = "No data\nn=0" if n == 0 else f"{rate * 100:.1f}%\nn={n}{'*' if n < MIN_N else ''}"
            ax.text(j, i, label, ha="center", va="center", fontsize=8,
                    color="white" if pd.notna(rate) and rate > .6 else "black")
    return img
