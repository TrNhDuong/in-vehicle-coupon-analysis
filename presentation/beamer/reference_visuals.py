"""Dựng 17 biểu đồ vector PDF gọn, thống nhất dấu phẩy thập phân tiếng Việt cho slide Beamer."""
from html.parser import HTMLParser
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

LABELS = {
    "Bar": "Bar",
    "Coffee House": "Cà phê",
    "Carry out & Take away": "Đồ mang đi",
    "Restaurant(<20)": "Nhà hàng <20",
    "Restaurant(20-50)": "Nhà hàng 20–50",
}
NAVY, BLUE, GRAY, GREEN, AMBER = "#18222B", "#365E7D", "#7C8893", "#527A67", "#B45309"
GRID = "#E6ECF1"


def fnum(val: float, dec: int = 1) -> str:
    """Định dạng số thập phân kiểu Việt Nam (dấu phẩy)."""
    return f"{val:.{dec}f}".replace(".", ",").replace("-", "−")


def fsign(val: float, dec: int = 2) -> str:
    """Định dạng chênh lệch có dấu +/− kiểu Việt Nam."""
    return f"{val:+.{dec}f}".replace(".", ",").replace("-", "−")


def fint(val: int) -> str:
    """Định dạng số nguyên phân tách hàng nghìn bằng dấu chấm."""
    return f"{int(val):,}".replace(",", ".")


class OutputTable(HTMLParser):
    """Đọc bảng HTML do pandas lưu trong output notebook (giữ cả cột index)."""

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


def table(name: str, cell: int, index: int = 0) -> pd.DataFrame:
    nb = json.loads((ROOT / "notebooks" / name).read_text(encoding="utf-8"))
    outputs = [
        o["data"]["text/html"]
        for o in nb["cells"][cell]["outputs"]
        if "text/html" in o.get("data", {})
    ]
    parser = OutputTable()
    parser.feed("".join(outputs[index]))
    return pd.DataFrame(parser.rows, columns=["index", *parser.header[1:]])


def build() -> int:
    out = HERE / "figures"
    out.mkdir(exist_ok=True)
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 15,
        "axes.labelsize": 14,
        "xtick.labelsize": 13.5,
        "ytick.labelsize": 15,
        "pdf.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.edgecolor": "#CBD5E1",
        "text.color": "#16202A",
        "axes.labelcolor": "#4A5568",
        "xtick.color": "#4A5568",
        "ytick.color": "#16202A",
    })

    def save(fig, name: str):
        fig.savefig(out / f"ref_{name}.pdf", bbox_inches="tight", facecolor="white")
        plt.close(fig)

    def pair(frame, a, b, labels, names, name, percent=True, c1=BLUE, c2=GRAY):
        fig, ax = plt.subplots(figsize=(8.2, 2.7))
        y = np.arange(len(frame))
        ax.set_axisbelow(True)
        ax.grid(axis="x", color=GRID, linewidth=0.9)
        for offset, col, label, color in [(-.18, a, names[0], c1), (.18, b, names[1], c2)]:
            vals = frame[col].astype(float)
            bars = ax.barh(y + offset, vals, 0.31, color=color, label=label)
            ax.bar_label(
                bars,
                labels=[fnum(v, 1) + ("%" if percent else "") for v in vals],
                padding=5, fontsize=13.5,
            )
        ax.set_yticks(y, labels)
        ax.invert_yaxis()
        ax.set(xlim=(0, 110), xlabel="Tỷ lệ chấp nhận (%)" if percent else "Tỷ lệ lỗi (%)")
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2, frameon=False, fontsize=13)
        save(fig, name)

    def forest(frame, labels, name, xlabel, colors=None):
        fig, ax = plt.subplots(figsize=(8.2, 2.6))
        v, lo, hi = [
            frame[c].astype(float).to_numpy()
            for c in ["diff_pp", "ci_low_pp", "ci_high_pp"]
        ]
        y = np.arange(len(frame))
        ax.set_axisbelow(True)
        ax.grid(axis="x", color=GRID, linewidth=0.9)
        ax.axvline(0, color="#94A3B8", linestyle="--", linewidth=1.2)
        for idx, (x_val, lo_v, hi_v, yy) in enumerate(zip(v, lo, hi, y)):
            col = colors[idx] if colors is not None else (AMBER if x_val < 0 else BLUE)
            ax.errorbar(
                x_val, yy, xerr=[[x_val - lo_v], [hi_v - x_val]],
                fmt="o", color=col, capsize=4.5, markersize=7.5, linewidth=2.2,
            )
            ax.annotate(
                fsign(x_val, 2), (x_val, yy), xytext=(0, 9),
                textcoords="offset points", ha="center", fontsize=12.5,
                fontweight="bold", color=col,
            )
        ax.set_yticks(y, labels)
        ax.set_ylim(len(y) - 0.4, -0.75)
        ax.set_xlabel(xlabel)
        ax.margins(x=0.14)
        save(fig, name)

    raw = pd.read_csv(ROOT / "data/raw/in-vehicle-coupon-recommendation.csv").copy()

    # 1. EDA: Missing values
    missing = raw.isna().mean().mul(100)
    missing = missing[missing > 0].sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8.2, 2.55))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.9)
    mnames = {
        "car": "Loại xe (car)", "CoffeeHouse": "Thói quen Cà phê",
        "Bar": "Thói quen Bar", "CarryAway": "Thói quen Đồ mang đi",
        "RestaurantLessThan20": "Nhà hàng <20", "Restaurant20To50": "Nhà hàng 20–50",
    }
    bar_cols = [AMBER if k == "car" else BLUE for k in missing.index]
    bars = ax.barh([mnames[x] for x in missing.index], missing.values, color=bar_cols, height=0.58)
    ax.bar_label(bars, labels=[fnum(x, 2) + "%" for x in missing], padding=5, fontsize=13.5)
    ax.invert_yaxis()
    ax.set(xlim=(0, 118), xlabel="Tỷ lệ ô trống (%)")
    save(fig, "missing")

    # 2. EDA: Coupon & Passenger distributions (2 panels)
    pass_labels = {"Alone": "Một mình", "Friend(s)": "Bạn bè", "Partner": "Bạn đời", "Kid(s)": "Con cái"}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 2.55))
    c_counts = raw["coupon"].value_counts()
    c_pct = c_counts / len(raw) * 100
    ax1.set_axisbelow(True)
    ax1.grid(axis="x", color=GRID, linewidth=0.8)
    b1 = ax1.barh([LABELS[k] for k in c_counts.index], c_pct.values, color=BLUE, height=0.58)
    ax1.bar_label(b1, labels=[fnum(p, 1) + "%" for p in c_pct], padding=4, fontsize=12)
    ax1.invert_yaxis()
    ax1.set(xlim=(0, 42), xlabel="Tỷ trọng loại dịch vụ (%)")
    ax1.tick_params(axis="y", labelsize=12.5)

    p_counts = raw["passanger"].value_counts()
    p_pct = p_counts / len(raw) * 100
    ax2.set_axisbelow(True)
    ax2.grid(axis="x", color=GRID, linewidth=0.8)
    b2 = ax2.barh([pass_labels[k] for k in p_counts.index], p_pct.values, color=NAVY, height=0.54)
    ax2.bar_label(b2, labels=[fnum(p, 1) + "%" for p in p_pct], padding=4, fontsize=12)
    ax2.invert_yaxis()
    ax2.set(xlim=(0, 72), xlabel="Tỷ trọng người đi cùng (%)")
    ax2.tick_params(axis="y", labelsize=12.5)
    fig.tight_layout(w_pad=2.0)
    save(fig, "distributions")

    # 3. Method: Baseline acceptance by service type with overall average line
    rates = raw.groupby("coupon")["Y"].mean().mul(100).sort_values(ascending=False)
    overall = raw["Y"].mean() * 100
    fig, ax = plt.subplots(figsize=(8.2, 3.15))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.9)
    ax.axvline(overall, color=AMBER, linestyle="--", linewidth=1.6, zorder=1)
    bars = ax.barh([LABELS[x] for x in rates.index], rates.values, color=BLUE, height=0.56, zorder=2)
    for bar, v in zip(bars, rates.values):
        ax.text(
            v + 1.4, bar.get_y() + bar.get_height() / 2, fnum(v, 2) + "%",
            va="center", ha="left", fontsize=14, color="#16202A", zorder=4,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.92),
        )
    ax.text(overall + 1.5, 4.38, f"Trung bình chung: {fnum(overall, 2)}%", color=AMBER,
            fontsize=12.5, fontweight="bold", zorder=4,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.0, alpha=0.9))
    ax.invert_yaxis()
    ax.set(xlim=(0, 100), xlabel="Tỷ lệ chấp nhận ban đầu (%)")
    save(fig, "acceptance")

    # 4–5. Q1: Distance & Direction
    q1 = table("02_analysis.ipynb", 6, 3)
    pair(q1, "rate_a_pct", "rate_b_pct", [LABELS[x] for x in q1["coupon"]],
         ["Gần: 5–<15 phút", "Xa: ≥25 phút"], "distance")
    direction = table("02_analysis.ipynb", 6, 6)
    direction = direction[direction["status"] == "ok"]
    dir_labels = [
        ("Về nhà" if r.destination == "Home" else "Đi làm") + " / "
        + r.travel_time_band.replace(" min", " phút")
        for r in direction.itertuples()
    ]
    forest(direction, dir_labels, "direction", "Cùng − ngược hướng (điểm %), CI 95%")

    # 6–7. Q2: Time & Simpson's paradox at 10AM
    times = table("02_analysis.ipynb", 10).set_index("index").loc[
        ["7AM", "10AM", "2PM", "6PM", "10PM"]
    ]
    fig, ax = plt.subplots(figsize=(8.2, 2.65))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, linewidth=0.9)
    x = np.arange(5)
    ax.axvspan(0.55, 1.45, color="#FEF3C7", alpha=0.65, zorder=0)
    for offset, col, label, color in [(-.18, "1d", "Hạn 1 ngày", BLUE), (.18, "2h", "Hạn 2 giờ", GRAY)]:
        vals = times[col].astype(float)
        bars = ax.bar(x + offset, vals, 0.32, color=color, label=label)
        ax.bar_label(bars, labels=[fnum(v, 1) for v in vals], padding=4, fontsize=12.5)
    ax.text(1.0, 81, "Đảo chiều khi gộp", ha="center", fontsize=11.5, color=AMBER, fontweight="bold")
    ax.set_xticks(x, ["7h", "10h", "14h", "18h", "22h"])
    ax.set(ylim=(0, 90), ylabel="Chấp nhận (%)")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2, frameon=False, fontsize=13)
    save(fig, "time")

    grouped = table("02_analysis.ipynb", 12, 1)
    at10 = grouped[grouped["time"] == "10AM"]
    within = table("02_analysis.ipynb", 12, 4)
    simpson_df = pd.concat([at10, within], ignore_index=True)
    forest(
        simpson_df,
        ["Gộp tất cả (10h)"] + [LABELS[x] for x in within["coupon"]],
        "10am",
        "1 ngày − 2 giờ lúc 10h (điểm %), CI 95%",
        colors=[AMBER] + [BLUE] * len(within),
    )

    # 8–9. Q3: Matched habit & frequency heatmap
    q3 = table("02_analysis.ipynb", 18)
    pair(q3, "rate_a_pct", "rate_b_pct", [LABELS[x] for x in q3["coupon"]],
         ["Thường ghé (≥1 lần/tháng)", "Ít ghé (<1 lần/tháng)"], "habit")

    habit_columns = {
        "Bar": "Bar", "Coffee House": "CoffeeHouse",
        "Carry out & Take away": "CarryAway",
        "Restaurant(<20)": "RestaurantLessThan20",
        "Restaurant(20-50)": "Restaurant20To50",
    }
    freq_parts = []
    for coupon, column in habit_columns.items():
        part = raw.loc[raw["coupon"].eq(coupon), [column, "Y"]].copy()
        part["frequency_display"] = part[column].fillna("Unknown")
        rate = part.groupby("frequency_display")["Y"].mean().mul(100)
        freq_parts.append(rate.rename("rate_pct").reset_index().assign(coupon=coupon))
    freq = pd.concat(freq_parts, ignore_index=True)
    levels = ["never", "less1", "1~3", "4~8", "gt8", "Unknown"]
    matrix = freq.pivot(index="coupon", columns="frequency_display", values="rate_pct")
    matrix = matrix.reindex(index=list(LABELS), columns=levels)
    fig, ax = plt.subplots(figsize=(8.2, 2.55))
    ax.imshow(matrix, cmap="Blues", vmin=0, vmax=100, aspect="auto")
    ax.set_yticks(range(5), list(LABELS.values()))
    ax.set_xticks(range(6), ["Không", "<1", "1–3", "4–8", ">8", "Thiếu"])
    ax.set_xlabel("Số lần ghé loại quán đó mỗi tháng")
    for i in range(5):
        for j in range(6):
            v = matrix.iloc[i, j]
            ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=13,
                    fontweight="bold" if v > 65 else "normal",
                    color="white" if v > 56 else "#16202A")
    save(fig, "frequency")

    # 10–11. Q4: Passenger crude vs standardized & support matrix
    crude = table("02_analysis.ipynb", 24)
    adjusted = table("02_analysis.ipynb", 24, 1)
    adjusted = adjusted[adjusted["adjustment"] == "coupon_destination"]
    fig, ax = plt.subplots(figsize=(8.2, 2.6))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.9)
    ax.axvline(0, color="#94A3B8", linestyle="--", linewidth=1.2)
    for offset, frame, label, color in [
        (-.16, crude, "Gộp chung (thô)", GRAY),
        (.16, adjusted, "Cùng dịch vụ × mục đích", BLUE),
    ]:
        v, lo, hi = [frame[c].astype(float).to_numpy() for c in ["diff_pp", "ci_low_pp", "ci_high_pp"]]
        y = np.arange(2) + offset
        ax.errorbar(v, y, xerr=[v - lo, hi - v], fmt="o", color=color, label=label,
                    markersize=7.5, capsize=4.5, linewidth=2.2)
        for xx, yy in zip(v, y):
            ax.annotate(fsign(xx, 2), (xx, yy), xytext=(0, 9), textcoords="offset points",
                        ha="center", fontsize=12.5, fontweight="bold", color=color)
    ax.set_yticks([0, 1], ["Bạn bè − Một mình", "Bạn đời − Một mình"])
    ax.set(xlim=(-5, 22), ylim=(1.55, -0.8), xlabel="Chênh lệch (điểm %), CI 95%")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=2, frameon=False, fontsize=13)
    save(fig, "passenger")

    support = pd.crosstab(raw["passanger"], raw["destination"]).reindex(
        index=list(pass_labels), columns=["No Urgent Place", "Home", "Work"], fill_value=0
    )
    fig, ax = plt.subplots(figsize=(8.2, 2.55))
    colors = plt.get_cmap("Blues").copy()
    colors.set_bad("#E9EEF4")
    ax.imshow(np.ma.masked_where(support.to_numpy() == 0, support.to_numpy()),
              cmap=colors, aspect="auto", vmin=0, vmax=3300)
    ax.set_yticks(range(4), list(pass_labels.values()))
    ax.set_xticks(range(3), ["Không gấp", "Về nhà", "Đi làm"])
    for i in range(4):
        for j in range(3):
            v = int(support.iloc[i, j])
            txt = "0 (trống)" if v == 0 else fint(v)
            ax.text(j, i, txt, ha="center", va="center",
                    fontsize=13 if v == 0 else 15.5,
                    fontweight="bold" if v > 0 else "normal",
                    color="white" if v > 1900 else ("#7B8794" if v == 0 else "#16202A"))
    save(fig, "support")

    # 12–13. Q5: Age by coupon & Raw vs Adjusted (+ Income fixed by Age crossing 0!)
    age = table("02_analysis.ipynb", 32, 3)
    age = age[age["so_sanh"].str.startswith("Tuổi") & age["dieu_chinh"].eq("Thô")].copy()
    age["coupon"] = age["pham_vi"]
    pair(age, "rate_a_pct", "rate_b_pct", [LABELS[x] for x in age["coupon"]],
         ["Dưới 26 tuổi", "Từ 50 tuổi"], "age")

    q5 = table("02_analysis.ipynb", 30)
    q5 = q5[q5["pham_vi"] == "Tất cả coupon"]
    sens = table("02_analysis.ipynb", 31, 0)
    inc_age = sens[sens["phuong_an"].str.contains("giữ tuổi")].iloc[0]

    fig, ax = plt.subplots(figsize=(8.2, 2.75))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.9)
    ax.axvline(0, color="#94A3B8", linestyle="--", linewidth=1.2)
    for offset, mask, label, color, dy in [
        (-.18, q5["dieu_chinh"].eq("Thô"), "Ban đầu (thô)", GRAY, 8),
        (.18, q5["dieu_chinh"].str.contains("thói quen"), "Chuẩn hóa dịch vụ × thói quen", BLUE, -15),
    ]:
        frame = q5[mask]
        v, lo, hi = [frame[c].astype(float).to_numpy() for c in ["diff_pp", "ci_low_pp", "ci_high_pp"]]
        y = np.arange(2) + offset
        ax.errorbar(v, y, xerr=[v - lo, hi - v], fmt="o", color=color, label=label,
                    markersize=7.2, capsize=4.2, linewidth=2.1)
        for xx, yy in zip(v, y):
            ax.annotate(fsign(xx, 1), (xx, yy), xytext=(0, dy), textcoords="offset points",
                        ha="center", fontsize=12, fontweight="bold", color=color)

    # Row 2: Income holding age fixed (crosses 0 -> Amber!)
    iv, ilo, ihi = float(inc_age["diff_pp"]), float(inc_age["ci_low_pp"]), float(inc_age["ci_high_pp"])
    ax.errorbar(iv, 2.15, xerr=[[iv - ilo], [ihi - iv]], fmt="D", color=AMBER,
                label="Giữ cố định thêm nhóm tuổi (cắt 0)", markersize=7.2, capsize=4.2, linewidth=2.1)
    ax.annotate(fsign(iv, 1) + " (cắt 0)", (iv, 2.15), xytext=(0, 9), textcoords="offset points",
                ha="center", fontsize=12, fontweight="bold", color=AMBER)

    ax.set_yticks([0, 1, 2.15], ["Tuổi: <26 − 50+", "Thu nhập: thấp − cao", "Thu nhập (giữ tuổi)"])
    ax.set_xticks([-2, 0, 3, 6, 9, 12, 15])
    ax.set(xlim=(-2.2, 16.5), ylim=(2.7, -0.75), xlabel="Chênh lệch (điểm %), CI 95% theo cụm người")
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.02), ncol=2, frameon=False, fontsize=11.5)
    save(fig, "demographic")

    # 14–15. Q6: 3-metric Model comparison (AUC, Balanced Acc, Accuracy) & Confusion matrix
    scores = table("03_ml_question.ipynb", 11)
    fig, ax = plt.subplots(figsize=(8.2, 2.7))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, linewidth=0.9)
    x = np.arange(3)
    for k, (name, color) in enumerate(zip(["Luôn đoán nhận", "Logistic", "Random Forest"], [GRAY, BLUE, GREEN])):
        vals = scores.iloc[k][["test_roc_auc", "test_bal_acc", "test_acc"]].astype(float)
        bars = ax.bar(x + (k - 1) * 0.25, vals, 0.23, label=name, color=color)
        ax.bar_label(
            bars,
            labels=[fnum(vals.iloc[0], 3), fnum(vals.iloc[1], 3), fnum(vals.iloc[2] * 100, 1) + "%"],
            padding=3, fontsize=11.5, fontweight="bold" if k == 2 else "normal",
        )
    ax.set_xticks(x, ["Xếp hạng (ROC-AUC)", "Balanced Acc.", "Tỷ lệ đoán đúng"])
    ax.set_yticks([0.0, 0.5, 1.0], ["0,0", "0,5", "1,0"])
    ax.set(ylim=(0, 1.06), ylabel="Thang điểm 0–1")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.02), ncol=3, frameon=False, fontsize=12.5)
    save(fig, "models")

    cm = np.array([[633, 391], [314, 1214]])
    assert cm.sum() == 2552 and cm[0, 1] + cm[1, 0] == 705
    fig, ax = plt.subplots(figsize=(6.2, 2.65))
    pct = cm / cm.sum(axis=1, keepdims=True) * 100
    ax.imshow(pct, cmap="Blues", vmin=0, vmax=100, aspect="auto")
    tag_cm = [["Đúng (TN)", "Đoán nhầm (FP)"], ["Bỏ sót (FN)", "Đúng (TP)"]]
    for i in range(2):
        for j in range(2):
            txt = f"{tag_cm[i][j]}\n{fint(cm[i, j])} ({fnum(pct[i, j], 1)}%)"
            ax.text(j, i, txt, ha="center", va="center", fontsize=14, fontweight="bold",
                    color="white" if pct[i, j] > 56 else "#16202A")
    ax.set_xticks([0, 1], ["Đoán từ chối", "Đoán nhận"], fontsize=13.5)
    ax.set_yticks([0, 1], ["Thật: từ chối", "Thật: nhận"], fontsize=13.5)
    save(fig, "confusion")

    # 16–17. Q6: Error breakdown & Permutation importance (Top 6 + Age/Income ≈ 0 comparison!)
    errors = table("03_ml_question.ipynb", 14)
    pair(
        errors, "FPR", "FNR", [LABELS[x] for x in errors["index"]],
        ["FPR: đoán nhầm nhận", "FNR: bỏ sót người nhận"],
        "errors", percent=False, c1=BLUE, c2=AMBER,
    )

    imp_all = table("03_ml_question.ipynb", 17).set_index("index")
    top6 = ["coupon", "CoffeeHouse", "expiration", "Bar", "destination", "time"]
    demo2 = ["age", "income"]
    imp_names = {
        "coupon": "Loại dịch vụ", "CoffeeHouse": "Thói quen cà phê",
        "expiration": "Thời hạn phiếu", "Bar": "Thói quen Bar",
        "destination": "Điểm đến", "time": "Khung giờ",
        "age": "Tuổi (nhân khẩu)", "income": "Thu nhập (nhân khẩu)",
    }
    sel_keys = top6 + demo2
    vals = [float(imp_all.loc[k, "mean_drop_auc"]) for k in sel_keys]
    bar_colors = [BLUE] * 6 + [GRAY, GRAY]
    fig, ax = plt.subplots(figsize=(8.2, 2.7))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.9)
    ax.axvline(0, color="#94A3B8", linewidth=1.0)
    bars = ax.barh([imp_names[k] for k in sel_keys], vals, height=0.6, color=bar_colors)
    for bar, v in zip(bars, vals):
        x_pos = max(v, 0.0) + 0.0035
        lbl = fnum(v, 4) if abs(v) >= 0.0005 else "≈ 0"
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2, lbl,
                va="center", ha="left", fontsize=12.5,
                color="#52606D" if abs(v) < 0.002 else "#16202A")
    ax.axhline(5.5, color="#CBD5E1", linestyle=":", linewidth=1.1)
    ax.invert_yaxis()
    xticks = [0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18]
    ax.set_xticks(xticks, [fnum(t, 2) for t in xticks])
    ax.set(xlim=(-0.004, 0.195), xlabel="Mức giảm ROC-AUC khi xáo trộn ngẫu nhiên từng cột")
    save(fig, "importance")

    return 17


if __name__ == "__main__":
    print(f"Đã dựng {build()} biểu đồ PDF vector.")
