"""Vẽ biểu đồ cho slide từ các bảng output đã lưu, không chạy lại hay sửa phân tích."""
from html.parser import HTMLParser
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "presentation" / "assets"
BLUE, GREEN, GRAY = "#2563EB", "#059669", "#64748B"
LABELS = {
    "Bar": "Bar", "Coffee House": "Cà phê",
    "Carry out & Take away": "Đồ ăn mang đi",
    "Restaurant(<20)": "Nhà hàng <20 USD",
    "Restaurant(20-50)": "Nhà hàng 20–50 USD",
}


class OutputTable(HTMLParser):
    """Đọc bảng HTML mà pandas đã ghi trong notebook, kể cả cột index."""
    def __init__(self):
        super().__init__()
        self.section = self.cell = None
        self.row, self.header, self.rows = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag in {"thead", "tbody"}:
            self.section = tag
        elif tag == "tr":
            self.row = []
        elif tag in {"th", "td"}:
            self.cell = ""

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in {"th", "td"}:
            self.row.append(self.cell.strip())
            self.cell = None
        elif tag == "tr":
            if self.section == "thead" and not self.header:
                self.header = self.row
            elif self.section == "tbody":
                self.rows.append(self.row)
        elif tag in {"thead", "tbody"}:
            self.section = None


def table(name, cell, index=0):
    nb = json.loads((ROOT / "notebooks" / name).read_text(encoding="utf-8"))
    outputs = [o["data"]["text/html"] for o in nb["cells"][cell]["outputs"]
               if "text/html" in o.get("data", {})]
    parser = OutputTable()
    parser.feed("".join(outputs[index]))
    return pd.DataFrame(parser.rows, columns=["index", *parser.header[1:]])


def setup():
    plt.rcParams.update({
        "font.family": "Segoe UI", "font.size": 17, "axes.labelsize": 17,
        "xtick.labelsize": 16, "ytick.labelsize": 17, "svg.fonttype": "none",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.edgecolor": "#CBD5E1",
        "text.color": "#0F172A", "axes.labelcolor": "#334155",
        "xtick.color": "#475569", "ytick.color": "#334155",
    })


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def paired_bars(frame, first, second, first_label, second_label, name):
    fig, ax = plt.subplots(figsize=(11.3, 4.1))
    y = np.arange(len(frame))
    for offset, col, label, color in [
        (-.19, first, first_label, BLUE), (.19, second, second_label, GRAY)
    ]:
        vals = frame[col].astype(float).to_numpy()
        bars = ax.barh(y + offset, vals, .32, label=label, color=color)
        ax.bar_label(bars, labels=[f"{v:.1f}%" for v in vals], padding=7, fontsize=16)
    ax.set_yticks(y, [LABELS[x] for x in frame["coupon"]])
    ax.invert_yaxis()
    ax.set(xlim=(0, 104), xlabel="Tỷ lệ chấp nhận (%)")
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#E2E8F0", linewidth=.8)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2, frameon=False, fontsize=16)
    save(fig, name)


def main():
    setup()
    analysis = "02_analysis.ipynb"
    ml = "03_ml_question.ipynb"

    raw = pd.read_csv(ROOT / "data/raw/in-vehicle-coupon-recommendation.csv")
    missing = raw.isna().mean().mul(100)
    missing = missing[missing > 0].sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9.8, 4.1))
    bars = ax.barh(missing.index, missing.values, color=[BLUE] + [GRAY] * 5, height=.58)
    ax.bar_label(bars, labels=[f"{x:.2f}%" for x in missing], padding=8)
    ax.invert_yaxis()
    ax.set(xlim=(0, 117), xlabel="Dữ liệu thiếu (%)")
    save(fig, "eda_missing")

    paired_bars(table(analysis, 6, 3), "rate_a_pct", "rate_b_pct",
                "Gần: 5–<15 phút", "Xa: ≥25 phút", "cau_1")

    times = table(analysis, 10).set_index("index").loc[
        ["7AM", "10AM", "2PM", "6PM", "10PM"]]
    fig, ax = plt.subplots(figsize=(11.3, 4.0))
    x = np.arange(5)
    for offset, col, label, color in [(-.19, "1d", "Hạn 1 ngày", BLUE),
                                      (.19, "2h", "Hạn 2 giờ", GRAY)]:
        vals = times[col].astype(float)
        bars = ax.bar(x + offset, vals, .33, color=color, label=label)
        ax.bar_label(bars, labels=[f"{v:.1f}%" for v in vals], padding=6, fontsize=16)
    ax.set_xticks(x, ["7 giờ", "10 giờ", "14 giờ", "18 giờ", "22 giờ"])
    ax.set(ylim=(0, 88), ylabel="Tỷ lệ chấp nhận (%)")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False)
    save(fig, "cau_2")

    paired_bars(table(analysis, 18), "rate_a_pct", "rate_b_pct",
                "Ghé ≥1 lần/tháng", "Ghé <1 lần/tháng", "cau_3")

    crude, adjusted = table(analysis, 24), table(analysis, 24, 1)
    adjusted = adjusted[adjusted["adjustment"] == "coupon_destination"]
    fig, ax = plt.subplots(figsize=(11.3, 3.8))
    for offset, frame, label, color in [(-.15, crude, "Chưa điều chỉnh", GRAY),
                                        (.15, adjusted, "Đã điều chỉnh", BLUE)]:
        v = frame["diff_pp"].astype(float).to_numpy()
        low, high = [frame[c].astype(float).to_numpy() for c in ["ci_low_pp", "ci_high_pp"]]
        y = np.arange(2) + offset
        ax.errorbar(v, y, xerr=[v-low, high-v], fmt="o", color=color,
                    capsize=7, markersize=11, linewidth=3, label=label)
        for xx, yy in zip(v, y):
            ax.annotate(f"+{xx:.2f}", (xx, yy), xytext=(0, 17),
                        textcoords="offset points", ha="center", fontsize=17, color=color)
    ax.set_yticks([0, 1], ["Bạn bè − Một mình", "Bạn đời − Một mình"])
    ax.set(xlim=(-5, 23), ylim=(1.5, -.6), xlabel="Chênh lệch tỷ lệ nhận (pp), khoảng tin cậy 95%")
    ax.axvline(0, color="#94A3B8", linestyle="--")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2, frameon=False)
    save(fig, "cau_4")

    q5 = table(analysis, 30)
    q5 = q5[q5["pham_vi"] == "Tất cả coupon"]
    fig, ax = plt.subplots(figsize=(11.3, 3.8))
    for offset, mask, label, color in [
        (-.15, q5["dieu_chinh"].eq("Thô"), "Chưa điều chỉnh", GRAY),
        (.15, q5["dieu_chinh"].str.contains("thói quen"), "Cùng cơ cấu coupon và thói quen", BLUE)
    ]:
        part = q5[mask]
        v = part["diff_pp"].astype(float).to_numpy()
        low, high = [part[c].astype(float).to_numpy() for c in ["ci_low_pp", "ci_high_pp"]]
        assert len(v) == 2
        y = np.arange(2) + offset
        ax.errorbar(v, y, xerr=[v-low, high-v], fmt="o", color=color,
                    capsize=7, markersize=11, linewidth=3, label=label)
        for xx, yy in zip(v, y):
            ax.annotate(f"+{xx:.1f}", (xx, yy), xytext=(0, 17),
                        textcoords="offset points", ha="center", fontsize=17, color=color)
    ax.set_yticks([0, 1], ["Tuổi: <26 − 50+", "Thu nhập: Thấp − Cao"])
    ax.set(xlim=(-1, 18), ylim=(1.5, -.6), xlabel="Chênh lệch tỷ lệ nhận (pp), CI 95% theo người")
    ax.axvline(0, color="#94A3B8", linestyle="--")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2, frameon=False, fontsize=15)
    save(fig, "cau_5")

    scores = table(ml, 11)
    v = scores["test_roc_auc"].astype(float).to_numpy()
    low, high = [scores[c].astype(float).to_numpy() for c in ["auc_ci_low", "auc_ci_high"]]
    fig, ax = plt.subplots(figsize=(11.3, 3.9))
    bars = ax.bar(range(3), v, .5, color=[GRAY, BLUE, GREEN],
                  yerr=[v-low, high-v], capsize=9, error_kw={"linewidth": 2})
    ax.bar_label(bars, labels=[f"{x:.3f}" for x in v], padding=25, fontsize=24)
    ax.set_xticks(range(3), ["Đoán lớp đa số", "Logistic Regression", "Random Forest"])
    ax.set(ylim=(0, 1), ylabel="ROC-AUC trên tập test (CI 95%)")
    ax.axhline(.5, color="#CBD5E1", linestyle="--", zorder=0)
    save(fig, "cau_6_models")

    importance = table(ml, 17).iloc[:6]
    fig, ax = plt.subplots(figsize=(7.3, 4.1))
    names = ["Loại coupon", "Thói quen cà phê", "Thời hạn", "Thói quen bar", "Điểm đến", "Giờ"]
    bars = ax.barh(names, importance["mean_drop_auc"].astype(float), color=BLUE, height=.56)
    ax.bar_label(bars, labels=[f"{x:.4f}" for x in importance["mean_drop_auc"].astype(float)],
                 padding=7, fontsize=17)
    ax.invert_yaxis()
    ax.set(xlim=(0, .19), xlabel="Mức giảm ROC-AUC khi xáo trộn cột")
    save(fig, "cau_6_importance")

    print(f"Đã tạo {len(list(OUT.glob('*.svg')))} biểu đồ SVG từ dữ liệu/output gốc.")


if __name__ == "__main__":
    main()
