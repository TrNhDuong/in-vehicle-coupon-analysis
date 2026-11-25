# Từ điển biến & Quy ước phân tích – UCI Dataset #603

- **Nguồn:** *In-Vehicle Coupon Recommendation* — UCI ID **603** · DOI: `10.24432/C5GS4P` · **CC BY 4.0** · `12.684` dòng × `26` cột (`Y=1` chiếm **56,84%**).
- **Ý nghĩa 1 dòng:** Một kịch bản lái xe giả định trên Amazon Mechanical Turk kèm nhãn ý định `Y` (`1` = chấp nhận, `0` = từ chối; không phải giao dịch thật).

---

## 1. Danh mục 26 cột gốc

| Nhóm | Cột CSV | Kiểu & miền giá trị | Ý nghĩa / Lưu ý chất lượng |
| --- | --- | --- | --- |
| Hành trình | `destination` | Phân loại (`No Urgent Place`, `Home`, `Work`) | Mục đích chuyến đi |
| Hành trình | `passanger` | Phân loại (`Alone`, `Friend(s)`, `Partner`, `Kid(s)`) | Giữ nguyên tên cột gốc `passanger` |
| Hành trình | `weather` | Phân loại (`Sunny`, `Rainy`, `Snowy`) | Thời tiết kịch bản |
| Hành trình | `temperature` | Rời rạc (`30`, `55`, `80`) | Nhiệt độ (°F) |
| Hành trình | `time` | 5 mốc (`7AM`, `10AM`, `2PM`, `6PM`, `10PM`) | Giờ trong ngày (**không phải** chuỗi nhiều ngày) |
| Ưu đãi | `coupon` | 5 loại (bảng ánh xạ bên dưới) | Loại phiếu ưu đãi |
| Ưu đãi | `expiration` | Phân loại (`2h`, `1d`) | Thời hạn hiệu lực |
| Cá nhân | `gender`, `age`, `maritalStatus`, `has_children`, `education`, `occupation`, `income` | Phân loại / nhị phân / khoảng có thứ tự | `age` có `below21`, `50plus`; `income` là khoảng USD — không ép sang số |
| Cá nhân | `car` | Phân loại | **Thiếu 99,15%** (`12.576/12.684`) — loại khỏi ML features |
| Thói quen | `Bar`, `CoffeeHouse`, `CarryAway`, `RestaurantLessThan20`, `Restaurant20To50` | Thứ tự (`never`, `less1`, `1~3`, `4~8`, `gt8`) | Tần suất ghé/tháng; thiếu `0,84%–1,71%` |
| Khoảng cách | `toCoupon_GEQ5min`, `GEQ15min`, `GEQ25min` | Nhị phân (`0/1`) | `GEQ5min` **luôn bằng `1`** (hằng số); `0` vi phạm logic `GEQ25 ≤ GEQ15 ≤ GEQ5` |
| Hướng đi | `direction_same`, `direction_opp` | Nhị phân (`0/1`) | Luôn thỏa `direction_same + direction_opp = 1` |
| Nhãn | `Y` | Nhị phân (`0/1`) | Biến mục tiêu (`Y = 1` đạt **7.210 / 12.684**) |

---

## 2. Ánh xạ thói quen (`matched_frequency`) cho Q3 & Q5

| Nhãn `coupon` thực tế trong CSV | Cột thói quen tương ứng |
| --- | --- |
| `Coffee House` | `CoffeeHouse` |
| `Bar` | `Bar` |
| `Carry out & Take away` | `CarryAway` |
| `Restaurant(<20)` | `RestaurantLessThan20` |
| `Restaurant(20-50)` | `Restaurant20To50` |

- `frequent_user = 1` nếu `matched_frequency` thuộc `{1~3, 4~8, gt8}`, `0` nếu `{never, less1}`, giữ `NaN` khi thiếu (`164` dòng = `1,29%`). Ngưỡng sensitivity Q3/Q5: `{4~8, gt8}`.

---

## 3. Quy ước thống kê & kiểm soát dữ liệu dùng chung

1. **Giữ dòng trùng ở bản chính:** Giữ nguyên `74` dòng trùng lặp hoàn toàn ở phân tích chính vì CSV gốc thiếu `participant_id`; kiểm tra riêng độ nhạy sau `drop_duplicates()` ở Q1 & Q3.
2. **Định nghĩa metric & nhóm nhỏ:** `acceptance_rate = mean(Y) × 100 (%)`; chênh lệch biểu diễn theo **điểm phần trăm (pp)**. Nhóm có `n < 30` (`MIN_N = 30`) được gắn cờ `*`, không xếp hạng mạnh; ô `n = 0` để trống thay vì gán `0%`.
3. **Ước lượng bất định (D5):** Tỷ lệ đơn lẻ dùng **Wilson 95% CI**; chênh lệch giữa hai nhóm dùng **percentile bootstrap 95% CI** (`seed = 42` ở `metrics.py`/`demographics.py`, `seed = 17104` ở `analysis.py`). Riêng Q5 và Q6 dựng `respondent_id` suy ra (`567` hồ sơ duy nhất) để cluster-bootstrap theo người và tách `GroupShuffleSplit`.
4. **Chuẩn hóa confounder (D4):** Q4 chuẩn hóa trọng số `w_s = (n_As + n_Bs) / sum(n_As + n_Bs)` trên các tầng common support (`n ≥ 30` ở cả hai nhóm); Q5 chuẩn hóa trực tiếp theo phân bố tầng của mẫu. Mọi kết luận chỉ mang tính **mối liên hệ trong khảo sát**, không suy diễn nhân quả.
