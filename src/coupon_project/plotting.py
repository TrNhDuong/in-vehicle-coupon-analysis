"""Cac ham ve bieu do Matplotlib don gian, thong nhat cho ca nhom."""
"""Cac ham ve bieu do Matplotlib don gian, thong nhat cho ca nhom."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def set_style() -> None:
    """Thiet lap font chu va khung bieu do gon gang."""
    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 200,
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def _save_fig(fig: plt.Figure, out_path) -> None:
    if out_path is not None:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, bbox_inches="tight")


def plot_heatmap(
    rate_matrix: pd.DataFrame,
    count_matrix: pd.DataFrame | None,
    title: str,
    xlabel: str,
    ylabel: str,
    cbar_label: str,
    out_path=None,
    cmap: str = "YlGnBu",
    vmin: float | None = None,
    vmax: float | None = None,
    value_suffix: str = "%",
    signed: bool = False,
    min_n_warn: int = 30,
    figsize: tuple[float, float] = (8.0, 4.8),
) -> plt.Figure:
    """Ve heatmap ghi ro gia tri (%, pp) va co mau n trong tung o."""
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
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=12)

    midpoint = (vmin + vmax) / 2.0 if (vmin is not None and vmax is not None) else 55.0

    for i in range(n_rows):
        for j in range(n_cols):
            val = vals[i, j]
            n_val = int(count_matrix.iloc[i, j]) if count_matrix is not None else None

            if np.isnan(val):
                text = "n=0\n(No obs)"
                color = "#495057"
            else:
                if signed:
                    color = "white" if abs(val) > 25 else "#111827"
                    val_str = f"{val:+.1f}{value_suffix}"
                else:
                    color = "white" if val > midpoint + 4 else "#111827"
                    val_str = f"{val:.1f}{value_suffix}"

                if n_val is None:
                    text = val_str
                else:
                    star = " *" if n_val < min_n_warn else ""
                    text = f"{val_str}\n(n={n_val:,}{star})"

            ax.text(j, i, text, ha="center", va="center", color=color, fontsize=9)

    fig.tight_layout()
    _save_fig(fig, out_path)
    return fig


def plot_bars_ci(
    summary_df: pd.DataFrame,
    x_col: str,
    hue_col: str,
    x_order: list[str],
    hue_order: list[str],
    title: str,
    xlabel: str,
    ylabel: str = "Acceptance rate (%)",
    out_path=None,
    colors: list[str] | None = None,
    figsize: tuple[float, float] = (10.5, 5.2),
    ylim: tuple[float, float] = (0, 100),
    rotate_xticks: int = 0,
    show_n: bool = True,
    legend_title: str | None = None,
) -> plt.Figure:
    """Ve bieu do cot nhom kem thanh khoang tin cay 95% va nhan n."""
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

        heights, err_low, err_high, counts = [], [], [], []
        for x_val in x_order:
            row = lookup.get(x_val)
            if row is None or int(row["n"]) == 0:
                heights.append(0.0)
                err_low.append(0.0)
                err_high.append(0.0)
                counts.append(0)
            else:
                rate = float(row["rate_pct"])
                heights.append(rate)
                err_low.append(max(0.0, rate - float(row["ci_low_pct"])))
                err_high.append(max(0.0, float(row["ci_high_pct"]) - rate))
                counts.append(int(row["n"]))

        bars = ax.bar(
            x_pos + offset,
            heights,
            width=bar_width * 0.92,
            yerr=[err_low, err_high],
            capsize=3,
            label=str(hue_val),
            color=palette[idx % len(palette)],
            edgecolor="white",
            linewidth=0.7,
            error_kw={"elinewidth": 1.1, "ecolor": "#1F2937"},
        )

        for bar, val, h_err, n_val in zip(bars, heights, err_high, counts):
            if n_val == 0:
                continue
            label = f"{val:.1f}%\n(n={n_val:,})" if show_n else f"{val:.1f}%"
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                val + h_err + 1.5,
                label,
                ha="center",
                va="bottom",
                fontsize=7.3,
                color="#1F2937",
            )

    ax.set_xticks(x_pos, labels=x_order, rotation=rotate_xticks)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.legend(title=legend_title or hue_col, frameon=False, ncol=min(n_hue, 4), loc="upper right")

    fig.tight_layout()
    _save_fig(fig, out_path)
    return fig
