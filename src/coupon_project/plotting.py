"""Shared Matplotlib helpers for clean annotated heatmaps and grouped CI bar charts."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .data import FIGURES_DIR


def set_style():
    """Apply clean defaults for project charts."""
    plt.rcParams.update({
        "figure.dpi": 120, "savefig.dpi": 160, "font.size": 10,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10.5,
        "axes.spines.top": False, "axes.spines.right": False,
    })


def save_figure(fig, name: str, out_dir: Path = FIGURES_DIR, dpi: int = 160) -> Path:
    """Save PNG figure cleanly into reports/figures/."""
    path = Path(out_dir) / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path


def plot_heatmap(rate_matrix, count_matrix, title, xlabel, ylabel, cbar_label="Acceptance (%)",
                 out_name=None, cmap="YlGnBu", vmin=0, vmax=100, value_suffix="%",
                 signed=False, min_n_warn=30, figsize=(8.0, 4.8), ax=None):
    """Plot annotated heatmap with counts and empty-cell shading (standalone or on Axes)."""
    set_style()
    vals = rate_matrix.to_numpy(dtype=float)
    n_rows, n_cols = vals.shape
    own_fig = ax is None
    fig, ax = plt.subplots(figsize=figsize) if own_fig else (ax.figure, ax)

    cmap_obj = plt.get_cmap(cmap).copy()
    cmap_obj.set_bad("#E9ECEF")
    im = ax.imshow(vals, cmap=cmap_obj, aspect="auto", vmin=vmin, vmax=vmax)
    if own_fig:
        fig.colorbar(im, ax=ax, pad=0.02).set_label(cbar_label)

    ax.set_xticks(range(n_cols), labels=[str(c) for c in rate_matrix.columns], rotation=22 if n_cols > 3 else 0, ha="right" if n_cols > 3 else "center")
    ax.set_yticks(range(n_rows), labels=[str(r) for r in rate_matrix.index])
    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set_title(title, pad=10)

    mid = (vmin + vmax) / 2.0 if (vmin is not None and vmax is not None) else 55.0
    fmt = "+.1f" if signed else ".1f"
    for i in range(n_rows):
        for j in range(n_cols):
            val = vals[i, j]
            n_val = int(count_matrix.iloc[i, j]) if count_matrix is not None else None
            if np.isnan(val) or n_val == 0:
                text, color = "No data\nn=0", "#475569"
            else:
                dark = abs(val) > 25 if signed else val > mid + 5
                color = "white" if dark else "#111827"
                star = "*" if (n_val is not None and n_val < min_n_warn) else ""
                text = f"{val:{fmt}}{value_suffix}" if n_val is None else f"{val:{fmt}}{value_suffix}\n(n={n_val:,}{star})"
            ax.text(j, i, text, ha="center", va="center", color=color, fontsize=8.3)

    if own_fig:
        fig.tight_layout()
        if out_name:
            save_figure(fig, out_name)
    return fig, ax, im


def plot_bars_ci(summary_df, x_col, hue_col, x_order, hue_order, title, xlabel,
                 ylabel="Acceptance rate (%)", out_name=None, colors=None,
                 figsize=(10.5, 4.8), ylim=(0, 102), rotate_xticks=0, show_n=True, legend_title=None):
    """Plot grouped bars with 95% CI error bars using rate_pct, ci_low_pct, ci_high_pct."""
    set_style()
    fig, ax = plt.subplots(figsize=figsize)
    palette = colors or ["#2563EB", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6"]
    n_hue = len(hue_order)
    width = min(0.78 / max(n_hue, 1), 0.28)
    x_pos = np.arange(len(x_order), dtype=float)

    for idx, hue_val in enumerate(hue_order):
        offset = (idx - (n_hue - 1) / 2.0) * width
        sub = summary_df[summary_df[hue_col].astype(str) == str(hue_val)].copy()
        sub[x_col] = sub[x_col].astype(str)
        sub = sub.set_index(x_col).reindex(x_order)

        heights = sub["rate_pct"].fillna(0.0).to_numpy(dtype=float)
        counts = sub["n"].fillna(0).astype(int).to_numpy()
        err_lo = np.maximum(0.0, heights - sub["ci_low_pct"].fillna(0.0).to_numpy(dtype=float))
        err_hi = np.maximum(0.0, sub["ci_high_pct"].fillna(0.0).to_numpy(dtype=float) - heights)

        bars = ax.bar(
            x_pos + offset, heights, width=width * 0.92, yerr=[err_lo, err_hi],
            capsize=3, label=str(hue_val), color=palette[idx % len(palette)],
            edgecolor="white", linewidth=0.7, error_kw={"elinewidth": 1.1, "ecolor": "#1F2937"},
        )
        for bar, val, h_err, n_val in zip(bars, heights, err_hi, counts):
            if n_val == 0:
                continue
            label = f"{val:.1f}%\n(n={n_val:,})" if show_n else f"{val:.1f}%"
            ax.text(bar.get_x() + bar.get_width() / 2.0, val + h_err + 1.5, label,
                    ha="center", va="bottom", fontsize=7.3, color="#1F2937")

    ax.set_xticks(x_pos, labels=x_order, rotation=rotate_xticks)
    ax.set(ylim=ylim, xlabel=xlabel, ylabel=ylabel)
    ax.set_title(title, pad=10)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.legend(title=legend_title or hue_col, frameon=False, ncol=min(n_hue, 4), loc="upper right")

    fig.tight_layout()
    if out_name:
        save_figure(fig, out_name)
    return fig
