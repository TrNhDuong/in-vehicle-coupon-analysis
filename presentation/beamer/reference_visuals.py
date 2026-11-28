"""Biểu đồ gọn cho bố cục hai cột của bản PDF người dùng đã duyệt."""
from pathlib import Path
import importlib.util

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LABELS = {
    "Bar": "Bar", "Coffee House": "Cà phê",
    "Carry out & Take away": "Đồ mang đi",
    "Restaurant(<20)": "Nhà hàng <20",
    "Restaurant(20-50)": "Nhà hàng 20–50",
}
BLUE, GRAY, GREEN = "#365E7D", "#7C8893", "#527A67"


def build():
    spec = importlib.util.spec_from_file_location("slide_tables", HERE.parent / "build_visuals.py")
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    table = source.table
    out = HERE / "figures"
    out.mkdir(exist_ok=True)
    plt.rcParams.update({
        "font.family": "Segoe UI", "font.size": 16, "axes.labelsize": 15,
        "xtick.labelsize": 14, "ytick.labelsize": 16, "pdf.fonttype": 42,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.edgecolor": "#CBD5E1",
        "text.color": "#0F172A", "axes.labelcolor": "#475569",
    })

    def save(fig, name):
        for ext in ("pdf", "png"):
            fig.savefig(out / f"ref_{name}.{ext}", bbox_inches="tight",
                        facecolor="white", dpi=200)
        plt.close(fig)

    def pair(frame, a, b, labels, names, name, percent=True):
        fig, ax = plt.subplots(figsize=(8.3, 2.8))
        y = np.arange(len(frame))
        for offset, col, label, color in [(-.18, a, names[0], BLUE), (.18, b, names[1], GRAY)]:
            vals = frame[col].astype(float)
            bars = ax.barh(y + offset, vals, .3, color=color, label=label)
            ax.bar_label(bars, labels=[f"{v:.1f}" + ("%" if percent else "") for v in vals],
                         padding=5, fontsize=14)
        ax.set_yticks(y, labels)
        ax.invert_yaxis()
        ax.set(xlim=(0, 108), xlabel="Tỷ lệ chấp nhận (%)" if percent else "Tỷ lệ lỗi (%)")
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False, fontsize=13)
        save(fig, name)

    def forest(frame, labels, name, xlabel):
        fig, ax = plt.subplots(figsize=(8.3, 2.7))
        v, lo, hi = [frame[c].astype(float).to_numpy()
                     for c in ["diff_pp", "ci_low_pp", "ci_high_pp"]]
        y = np.arange(len(frame))
        ax.errorbar(v, y, xerr=[v-lo, hi-v], fmt="o", color=BLUE,
                    capsize=5, markersize=8, linewidth=2.2)
        for x, yy in zip(v, y):
            ax.annotate(f"{x:+.2f}", (x, yy), xytext=(0, 9), textcoords="offset points",
                        ha="center", fontsize=13, color=BLUE)
        ax.set_yticks(y, labels)
        ax.set_ylim(len(y)-.45, -.75)
        ax.axvline(0, color=GRAY, linestyle="--")
        ax.set_xlabel(xlabel)
        ax.margins(x=.12)
        save(fig, name)

    raw = pd.read_csv(ROOT / "data/raw/in-vehicle-coupon-recommendation.csv").copy()
    missing = raw.isna().mean().mul(100)
    missing = missing[missing > 0].sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8.3, 2.65))
    names = {"car": "Xe", "CoffeeHouse": "Cà phê", "Bar": "Bar", "CarryAway": "Đồ mang đi",
             "RestaurantLessThan20": "Nhà hàng <20", "Restaurant20To50": "Nhà hàng 20–50"}
    bars = ax.barh([names[x] for x in missing.index], missing.values, color=BLUE, height=.58)
    ax.bar_label(bars, labels=[f"{x:.2f}%" for x in missing], padding=5, fontsize=14)
    ax.invert_yaxis()
    ax.set(xlim=(0, 118), xlabel="Dữ liệu thiếu (%)")
    save(fig, "missing")

    pass_labels = {"Alone": "Một mình", "Friend(s)": "Bạn bè", "Partner": "Bạn đời", "Kid(s)": "Con cái"}
    rates = raw.groupby("coupon")["Y"].mean().mul(100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8.3, 4.0))
    bars = ax.barh([LABELS[x] for x in rates.index], rates.values, color=BLUE, height=.58)
    ax.bar_label(bars, labels=[f"{v:.2f}%" for v in rates], padding=6, fontsize=16)
    ax.invert_yaxis()
    ax.set(xlim=(0, 102), xlabel="Tỷ lệ chấp nhận (%)")
    save(fig, "acceptance")

    q1 = table("02_analysis.ipynb", 6, 3)
    pair(q1, "rate_a_pct", "rate_b_pct", [LABELS[x] for x in q1["coupon"]],
         ["Gần: 5–<15 phút", "Xa: ≥25 phút"], "distance")
    direction = table("02_analysis.ipynb", 6, 6)
    direction = direction[direction["status"] == "ok"]
    labels = [("Về nhà" if r.destination == "Home" else "Đi làm") + " / "
              + r.travel_time_band.replace(" min", " phút") for r in direction.itertuples()]
    forest(direction, labels, "direction", "Cùng − ngược hướng (điểm %), khoảng tin cậy 95%")

    times = table("02_analysis.ipynb", 10).set_index("index").loc[
        ["7AM", "10AM", "2PM", "6PM", "10PM"]]
    fig, ax = plt.subplots(figsize=(8.3, 2.7))
    x = np.arange(5)
    for offset, col, label, color in [(-.18, "1d", "1 ngày", BLUE), (.18, "2h", "2 giờ", GRAY)]:
        vals = times[col].astype(float)
        bars = ax.bar(x + offset, vals, .32, color=color, label=label)
        ax.bar_label(bars, labels=[f"{v:.1f}" for v in vals], padding=4, fontsize=13)
    ax.set_xticks(x, ["7h", "10h", "14h", "18h", "22h"])
    ax.set(ylim=(0, 90), ylabel="Chấp nhận (%)")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=13)
    save(fig, "time")
    grouped = table("02_analysis.ipynb", 12, 1)
    at10 = grouped[grouped["time"] == "10AM"]
    within = table("02_analysis.ipynb", 12, 4)
    forest(pd.concat([at10, within], ignore_index=True),
           ["Gộp tất cả"]+[LABELS[x] for x in within["coupon"]],
           "10am", "1 ngày − 2 giờ lúc 10h (điểm %), khoảng tin cậy 95%")

    q3 = table("02_analysis.ipynb", 18)
    pair(q3, "rate_a_pct", "rate_b_pct", [LABELS[x] for x in q3["coupon"]],
         ["Ghé ≥1 lần/tháng", "Ghé <1 lần/tháng"], "habit")
    # Output bổ sung trong cell 18 chỉ hiển thị mức 4–8 và >8 để kiểm tra plateau.
    # Dựng bảng đủ 6 mức từ CSV thật cho heatmap, không sửa notebook hoặc CSV.
    habit_columns = {
        "Bar": "Bar", "Coffee House": "CoffeeHouse",
        "Carry out & Take away": "CarryAway",
        "Restaurant(<20)": "RestaurantLessThan20",
        "Restaurant(20-50)": "Restaurant20To50",
    }
    frequency_parts = []
    for coupon, column in habit_columns.items():
        part = raw.loc[raw["coupon"].eq(coupon), [column, "Y"]].copy()
        part["frequency_display"] = part[column].fillna("Unknown")
        rate = part.groupby("frequency_display")["Y"].mean().mul(100)
        frequency_parts.append(rate.rename("rate_pct").reset_index().assign(coupon=coupon))
    freq = pd.concat(frequency_parts, ignore_index=True)
    levels = ["never", "less1", "1~3", "4~8", "gt8", "Unknown"]
    matrix = freq.pivot(index="coupon", columns="frequency_display", values="rate_pct")
    matrix = matrix.reindex(index=list(LABELS), columns=levels)
    assert matrix.notna().all().all(), "Heatmap phải có đủ loại coupon và mức thói quen."
    fig, ax = plt.subplots(figsize=(8.3, 2.65))
    im = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=100, aspect="auto")
    ax.set_yticks(range(5), list(LABELS.values()))
    ax.set_xticks(range(6), ["Không", "<1", "1–3", "4–8", ">8", "Thiếu"])
    ax.set_xlabel("Số lần ghé mỗi tháng")
    for i in range(5):
        for j in range(6):
            v = matrix.iloc[i, j]
            if pd.notna(v):
                ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=13,
                        color="white" if v>58 else "#0F172A")
    save(fig, "frequency")

    crude = table("02_analysis.ipynb", 24)
    adjusted = table("02_analysis.ipynb", 24, 1)
    adjusted = adjusted[adjusted["adjustment"] == "coupon_destination"]
    fig, ax = plt.subplots(figsize=(8.3, 2.7))
    for offset, frame, label, color in [(-.16, crude, "Gộp chung", GRAY), (.16, adjusted, "Cùng hoàn cảnh", BLUE)]:
        v, lo, hi = [frame[c].astype(float).to_numpy() for c in ["diff_pp", "ci_low_pp", "ci_high_pp"]]
        y = np.arange(2)+offset
        ax.errorbar(v, y, xerr=[v-lo, hi-v], fmt="o", color=color, label=label,
                    markersize=8, capsize=5, linewidth=2.2)
        for xx, yy in zip(v, y):
            ax.annotate(f"+{xx:.2f}", (xx, yy), xytext=(0, 10), textcoords="offset points",
                        ha="center", fontsize=13, color=color)
    ax.set_yticks([0, 1], ["Bạn bè − Một mình", "Bạn đời − Một mình"])
    ax.set(xlim=(-5, 22), ylim=(1.5, -.8), xlabel="Chênh lệch (điểm %), khoảng tin cậy 95%")
    ax.axvline(0, color=GRAY, linestyle="--")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False, fontsize=13)
    save(fig, "passenger")
    support = pd.crosstab(raw["passanger"], raw["destination"]).reindex(
        index=list(pass_labels), columns=["No Urgent Place", "Home", "Work"], fill_value=0)
    fig, ax = plt.subplots(figsize=(8.3, 2.65))
    colors = plt.get_cmap("Blues").copy()
    colors.set_bad("#E2E8F0")
    ax.imshow(np.ma.masked_where(support.to_numpy()==0,support.to_numpy()),
              cmap=colors, aspect="auto", vmin=0, vmax=3300)
    ax.set_yticks(range(4), list(pass_labels.values()))
    ax.set_xticks(range(3), ["Không gấp", "Về nhà", "Đi làm"])
    for i in range(4):
        for j in range(3):
            v = support.iloc[i, j]
            ax.text(j, i, f"{v:,}", ha="center", va="center", fontsize=16,
                    color="white" if v>1900 else "#0F172A")
    save(fig, "support")

    age = table("02_analysis.ipynb", 32, 3)
    age = age[age["so_sanh"].str.startswith("Tuổi") & age["dieu_chinh"].eq("Thô")].copy()
    age["coupon"] = age["pham_vi"]
    pair(age, "rate_a_pct", "rate_b_pct", [LABELS[x] for x in age["coupon"]],
         ["Dưới 26 tuổi", "Từ 50 tuổi"], "age")
    q5 = table("02_analysis.ipynb", 30)
    q5 = q5[q5["pham_vi"] == "Tất cả coupon"]
    fig, ax = plt.subplots(figsize=(8.3, 2.7))
    for offset, mask, label, color in [
        (-.16, q5["dieu_chinh"].eq("Thô"), "Ban đầu", GRAY),
        (.16, q5["dieu_chinh"].str.contains("thói quen"), "Cân bằng hai nhóm", BLUE)]:
        frame=q5[mask]
        v, lo, hi = [frame[c].astype(float).to_numpy() for c in ["diff_pp", "ci_low_pp", "ci_high_pp"]]
        y=np.arange(2)+offset
        ax.errorbar(v,y,xerr=[v-lo,hi-v],fmt="o",color=color,label=label,
                    markersize=8,capsize=5,linewidth=2.2)
        for xx,yy in zip(v,y):
            ax.annotate(f"+{xx:.1f}",(xx,yy),xytext=(0,10),textcoords="offset points",
                        ha="center",fontsize=13,color=color)
    ax.set_yticks([0,1],["Tuổi: <26 − 50+","Thu nhập: thấp − cao"])
    ax.set(xlim=(-1,17),ylim=(1.5,-.8),xlabel="Chênh lệch (điểm %), khoảng tin cậy 95% theo người")
    ax.axvline(0,color=GRAY,linestyle="--")
    ax.legend(loc="lower left",bbox_to_anchor=(0,1.01),ncol=2,frameon=False,fontsize=13)
    save(fig,"demographic")

    scores = table("03_ml_question.ipynb",11)
    fig,ax=plt.subplots(figsize=(8.3,2.7))
    x=np.arange(2)
    for k,(name,color) in enumerate(zip(["Luôn đoán nhận","Logistic","Random Forest"],[GRAY,BLUE,GREEN])):
        vals=scores.iloc[k][["test_roc_auc","test_acc"]].astype(float)
        bars=ax.bar(x+(k-1)*.23,vals,.21,label=name,color=color)
        ax.bar_label(bars,labels=[f"{vals.iloc[0]:.3f}",f"{vals.iloc[1]*100:.1f}%"],padding=3,fontsize=12)
    ax.set_xticks(x,["Khả năng xếp hạng (AUC)","Tỷ lệ đoán đúng"])
    ax.set(ylim=(0,1.05),ylabel="Thang điểm 0–1")
    ax.legend(loc="lower left",bbox_to_anchor=(0,1.01),ncol=3,frameon=False,fontsize=12)
    save(fig,"models")
    # Số đếm từ ma trận nhầm lẫn trong PDF đã duyệt và output Q6 (ngưỡng 0,5).
    cm=np.array([[633,391],[314,1214]])
    assert cm.sum()==2552 and cm[0,1]+cm[1,0]==705
    fig,ax=plt.subplots(figsize=(5.8,2.8))
    pct=cm/cm.sum(axis=1,keepdims=True)*100
    ax.imshow(pct,cmap="Blues",vmin=0,vmax=100,aspect="auto")
    for i in range(2):
        for j in range(2):
            ax.text(j,i,f"{cm[i,j]:,}\n{pct[i,j]:.1f}%",ha="center",va="center",
                    fontsize=19,color="white" if pct[i,j]>58 else "#0F172A")
    ax.set_xticks([0,1],["Đoán từ chối","Đoán nhận"],fontsize=14)
    ax.set_yticks([0,1],["Thật: từ chối","Thật: nhận"],fontsize=14)
    save(fig,"confusion")
    errors=table("03_ml_question.ipynb",14)
    pair(errors,"FPR","FNR",[LABELS[x] for x in errors["index"]],
         ["Đoán nhận khi thật ra từ chối","Đoán từ chối khi thật ra muốn nhận"],"errors",False)
    imp=table("03_ml_question.ipynb",17).iloc[:6]
    fig,ax=plt.subplots(figsize=(8.3,2.65))
    labels=["Loại coupon","Thói quen cà phê","Thời hạn","Thói quen Bar","Điểm đến","Giờ"]
    bars=ax.barh(labels,imp["mean_drop_auc"].astype(float),height=.56,color=BLUE)
    ax.bar_label(bars,labels=[f"{v:.4f}" for v in imp["mean_drop_auc"].astype(float)],padding=5,fontsize=14)
    ax.invert_yaxis()
    ax.set(xlim=(0,.19),xlabel="Điểm AUC giảm khi đảo ngẫu nhiên cột")
    save(fig,"importance")
    return 16
