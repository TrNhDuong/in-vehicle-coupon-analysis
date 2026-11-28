"""Định nghĩa thứ tự danh mục và tạo các biến đặc trưng cho Q1–Q6."""
import pandas as pd

# Thứ tự chuẩn cho các biến phân loại để giữ nhất quán bảng và biểu đồ
TRAVEL_BAND_ORDER = ["5-<15 min", "15-<25 min", ">=25 min"]
TIME_ORDER = ["7AM", "10AM", "2PM", "6PM", "10PM"]
EXPIRATION_ORDER = ["2h", "1d"]
FREQUENCIES = ["never", "less1", "1~3", "4~8", "gt8"]

# Bảng ánh xạ từ nhãn coupon trong CSV sang đúng cột thói quen đi quán tương ứng
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


def check_journey_flags(df: pd.DataFrame) -> dict:
    """Kiểm tra tính nhất quán của cờ khoảng cách (GEQ5/15/25) và cờ hướng di chuyển."""
    # Dòng vô lý: thời gian >= 25 phút nhưng cờ >= 15 phút lại bằng 0
    invalid = (df["toCoupon_GEQ25min"] == 1) & (df["toCoupon_GEQ15min"] == 0)
    return {
        "n_rows": len(df),
        "geq5_always_one": bool((df["toCoupon_GEQ5min"] == 1).all()),
        "invalid_geq_hierarchy_count": int(invalid.sum()),
        "direction_complement_ok": bool((df["direction_same"] + df["direction_opp"] == 1).all()),
    }


def add_travel_time_band(df: pd.DataFrame, col_name: str = "travel_time_band") -> pd.DataFrame:
    """Tạo biến phân loại có thứ tự travel_time_band (D3) trên bản sao df."""
    if check_journey_flags(df)["invalid_geq_hierarchy_count"] > 0:
        raise ValueError("Có dòng bất hợp lý: toCoupon_GEQ25min == 1 nhưng toCoupon_GEQ15min == 0.")

    out = df.copy()
    band = pd.Series("15-<25 min", index=out.index)
    band[out["toCoupon_GEQ15min"] == 0] = "5-<15 min"
    band[out["toCoupon_GEQ25min"] == 1] = ">=25 min"
    out[col_name] = pd.Categorical(band, categories=TRAVEL_BAND_ORDER, ordered=True)
    return out


def matched_frequency(df: pd.DataFrame) -> pd.Series:
    """Ánh xạ mỗi loại coupon sang đúng cột tần suất thói quen tương ứng (giữ nguyên giá trị thiếu)."""
    unknown = set(df["coupon"].dropna()) - set(COUPON_FREQUENCY)
    if unknown or df["coupon"].isna().any():
        raise ValueError(f"Nhãn coupon bị thiếu hoặc không hợp lệ: {sorted(unknown)}")

    res = pd.Series(pd.NA, index=df.index, dtype="string", name="matched_frequency")
    for coupon, col in COUPON_FREQUENCY.items():
        mask = df["coupon"] == coupon
        vals = df.loc[mask, col]
        if not vals.dropna().isin(FREQUENCIES).all():
            raise ValueError(f"Giá trị tần suất không hợp lệ ở cột {col}.")
        res.loc[mask] = vals.astype("string")
    return res


def build_respondent_id(df: pd.DataFrame, profile_cols) -> pd.Series:
    """Suy ra mã người trả lời giả định (0..k-1) từ các dòng có cùng tổ hợp hồ sơ cá nhân."""
    return df.groupby(list(profile_cols), dropna=False, sort=False).ngroup()
