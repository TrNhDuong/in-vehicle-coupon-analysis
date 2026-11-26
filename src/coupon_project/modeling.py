"""Xây dựng Pipeline sklearn chống rò rỉ dữ liệu, bootstrap theo cụm người và phân tích lỗi cho Q6."""
import numpy as np
import pandas as pd


def build_pipeline(estimator, cat_cols, bin_cols):
    """Đóng gói bước tiền xử lý (điền thiếu + One-Hot) và mô hình vào 1 Pipeline chống leakage."""
    # Import sklearn bên trong hàm để GitHub CI (không cài scikit-learn) vẫn chạy pass
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder

    prep = ColumnTransformer([
        # Các cột phân loại: điền ô trống bằng nhãn "missing" rồi mã hóa One-Hot thành 0/1
        ("cat", Pipeline([
            ("imp", SimpleImputer(strategy="constant", fill_value="missing")),
            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]), list(cat_cols)),
        # Các cột nhị phân 0/1 giữ nguyên không biến đổi
        ("bin", "passthrough", list(bin_cols)),
    ])
    return Pipeline([("preprocess", prep), ("model", estimator)])


def cluster_bootstrap_metric(metric_fn, y_true, y_values, groups, n_boot: int = 1000, seed: int = 42) -> np.ndarray:
    """Tính phân phối bootstrap của metric_fn bằng cách lấy mẫu lại theo cụm người trả lời."""
    rng = np.random.default_rng(seed)
    pid = pd.factorize(np.asarray(groups))[0]
    n_people = int(pid.max() + 1)
    probs = np.full(n_people, 1.0 / n_people)
    return np.array([metric_fn(y_true, y_values, sample_weight=rng.multinomial(n_people, probs)[pid]) for _ in range(n_boot)])


def error_breakdown(df: pd.DataFrame, y_true, y_pred, group_col: str) -> pd.DataFrame:
    """Thống kê tỷ lệ nhận thật, độ chính xác, FPR (%) và FNR (%) theo từng nhóm mà không sửa df."""
    work = pd.DataFrame({
        group_col: df[group_col].to_numpy(),
        "y_true": np.asarray(y_true),
        "y_pred": np.asarray(y_pred),
    })
    work["correct"] = work["y_true"] == work["y_pred"]
    work["pred_accept"] = work["y_pred"] == 1
    work["pred_reject"] = work["y_pred"] == 0

    by_group = work.groupby(group_col)
    actual_reject = work[work["y_true"] == 0].groupby(group_col)  # các dòng thật sự từ chối
    actual_accept = work[work["y_true"] == 1].groupby(group_col)  # các dòng thật sự nhận
    out = pd.DataFrame({
        "n": by_group.size(),
        "true_rate": by_group["y_true"].mean().round(3),
        "acc": by_group["correct"].mean().round(3),
        # FPR: trong số dòng thật sự từ chối, bao nhiêu % bị đoán là nhận
        "FPR": (actual_reject["pred_accept"].mean() * 100.0).round(2),
        # FNR: trong số dòng thật sự nhận, bao nhiêu % bị đoán là từ chối
        "FNR": (actual_accept["pred_reject"].mean() * 100.0).round(2),
    })
    return out.sort_values("true_rate")


def probability_bins(y_true, y_pred, y_proba, bins=(0, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0)) -> pd.DataFrame:
    """Đánh giá độ khớp xác suất dự đoán (calibration) và độ chính xác theo từng khoảng xác suất."""
    work = pd.DataFrame({
        "y_true": np.asarray(y_true),
        "ok": np.asarray(y_true) == np.asarray(y_pred),
        "proba": np.asarray(y_proba),
    })
    work["p_bin"] = pd.cut(work["proba"], list(bins), include_lowest=True)
    return work.groupby("p_bin", observed=True).agg(
        n=("y_true", "size"), mean_p=("proba", "mean"), true_y=("y_true", "mean"), acc=("ok", "mean"),
    ).round(3)
