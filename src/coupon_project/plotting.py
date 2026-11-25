"""Ham ve bieu do Matplotlib gon gang cho ca nhom."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def set_style():
    """Thiet lap style chung cho bieu do."""
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 200, "font.size": 10,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10.5,
        "axes.spines.top": False, "axes.spines.right": False,
    })


def _save_fig(fig, out_path):
    if out_path is not None:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, bbox_inches="tight")


def plot_heatmap(rate_matrix, count_matrix, title, xlabel, ylabel, cbar_label,
                 out_path=None, cmap="YlGnBu", vmin=None, vmax=None,
                 value_suffix="%", signed=False, min_n_warn=30, figsize=(8.0, 4.8)):
    """Ve heatmap ghi gia tri (%, pp) va co mau n trong tung o."""
    set_style()
    vals = rate_matrix.to_numpy(dtype=float)
    n_rows, n_cols = vals.shape

    fig, ax = plt.subplots(figsize=figsize)
    cmap_obj = plt.get_cmap(cmap).copy()
    cmap_obj.set_bad("#E9ECEF")

    im = ax.imshow(vals, cmap=cmap_obj, aspect="auto", vmin=vmin, vmax=vmax)
    fig.colorbar(im, ax=ax, pad=0.02).set_label(cbar_label)
    ax.set_xticks(range(n_cols), labels=[str(c) for c in rate_matrix.columns])
    ax.set_yticks(range(n_rows), labels=[str(r) for r in rate_matrix.index])
    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set_title(title, pad=12)

    midpoint = (vmin + vmax) / 2.0 if (vmin is not None and vmax is not None) else 55.0
    for i in range(n_rows):
        for j in range(n_cols):
            val = vals[i, j]
            n_val = int(count_matrix.iloc[i, j]) if count_matrix is not None else None
            if np.isnan(val):
                text, color = "n=0\n(No obs)", "#495057"
            else:
                if signed:
                    color = "white" if abs(val) > 25 else "#111827"
                    val_str = f"{val:+.1f}{value_suffix}"
                else:
                    color = "white" if val > midpoint + 4 else "#111827"
                    val_str = f"{val:.1f}{value_suffix}"
                star = "*" if (n_val is not None and n_val < min_n_warn) else ""
                text = val_str if n_val is None else f"{val_str}\n(n={n_val:,}{' ' + star if star else ''})"
            ax.text(j, i, text, ha="center", va="center", color=color, fontsize=9)

    fig.tight_layout()
    _save_fig(fig, out_path)
    return fig


def plot_bars_ci(summary_df, x_col, hue_col, x_order, hue_order, title, xlabel,
                 ylabel="Acceptance rate (%)", out_path=None, colors=None,
                 figsize=(10.5, 5.2), ylim=(0, 100), rotate_xticks=0,
                 show_n=True, legend_title=None):
    """Ve bieu do cot nhom kem thanh CI 95% va nhan n."""
    set_style()
    fig, ax = plt.subplots(figsize=figsize)
    palette = colors or ["#2563EB", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6"]
    n_hue = len(hue_order)
    bar_width = min(0.78 / max(n_hue, 1), 0.28)
    x_pos = np.arange(len(x_order), dtype=float)

    for idx, hue_val in enumerate(hue_order):
        offset = (idx - (n_hue - 1) / 2.0) * bar_width
        sub = summary_df[summary_df[hue_col].astype(str) == str(hue_val)]
        lookup = {str(r[x_col]): r for _, r in sub.iterrows()}

        heights, err_lo, err_hi, counts = [], [], [], []
        for x_val in x_order:
            row = lookup.get(x_val)
            if row is None or int(row["n"]) == 0:
                heights.append(0.0); err_lo.append(0.0); err_hi.append(0.0); counts.append(0)
            else:
                r = float(row["rate_pct"])
                heights.append(r)
                err_lo.append(max(0.0, r - float(row["ci_low_pct"])))
                err_hi.append(max(0.0, float(row["ci_high_pct"]) - r))
                counts.append(int(row["n"]))

        bars = ax.bar(
            x_pos + offset, heights, width=bar_width * 0.92, yerr=[err_lo, err_hi],
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
    ax.set_title(title, pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.legend(title=legend_title or hue_col, frameon=False, ncol=min(n_hue, 4), loc="upper right")

    fig.tight_layout()
    _save_fig(fig, out_path)
    return fig
