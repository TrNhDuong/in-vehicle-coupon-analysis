# 📚 Dataset Dictionary – In-Vehicle Coupon Recommendation

**UCI Dataset #603:** <https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation>  
Số dòng công bố: **12.684** | Số features: **25** | Target: **`Y`**  
**Quan trọng:** các tên dưới đây dựa trên file CSV công khai; phải tự đối chiếu bằng `df.columns` sau khi tải. Ghi lại mọi lần đổi tên cột.

| Nhóm | Cột CSV | Ý nghĩa (giản lược) |
| --- | --- | --- |
| Hành trình | `destination` | Đi làm, về nhà, không có nơi cần đến gấp |
| Hành trình | `passanger` | Người đi cùng (tên cột CSV viết là **passanger**) |
| Hành trình | `weather` | Thời tiết giả định |
| Hành trình | `temperature` | Nhiệt độ của kịch bản (các mức như 30/55/80) |
| Hành trình | `time` | Thời điểm trong ngày, **không phải ngày tháng** |
| Ưu đãi | `coupon` | Loại coupon: quán cà phê, bar, takeaway, nhà hàng theo mức giá |
| Ưu đãi | `expiration` | Hạn sử dụng `2h` hoặc `1d` |
| Cá nhân | `gender` | Giới tính được khảo sát |
| Cá nhân | `age` | Nhóm tuổi: có cả `below21`, `50plus` |
| Cá nhân | `maritalStatus` | Tình trạng quan hệ/hôn nhân |
| Cá nhân | `has_children` | Có con hay không (0/1) |
| Cá nhân | `education` | Trình độ học vấn |
| Cá nhân | `occupation` | Nghề nghiệp |
| Cá nhân | `income` | Khoảng thu nhập (nhãn phân loại, cần thứ tự hợp lý) |
| Cá nhân | `car` | Điều kiện/phương tiện liên quan xe (cần kiểm tra độ thiếu thực tế) |
| Thói quen | `Bar` | Tần suất đến bar hàng tháng |
| Thói quen | `CoffeeHouse` | Tần suất đến quán cà phê hàng tháng |
| Thói quen | `CarryAway` | Tần suất mua đồ ăn mang đi |
| Thói quen | `RestaurantLessThan20` | Tần suất đến nhà hàng chi phí thấp |
| Thói quen | `Restaurant20To50` | Tần suất đến nhà hàng mức giá trung bình |
| Khoảng cách | `toCoupon_GEQ5min` | Đi đến điểm sử dụng coupon mất ít nhất khoảng 5 phút (kiểm tra phân phối) |
| Khoảng cách | `toCoupon_GEQ15min` | Thời gian đi đến điểm sử dụng coupon ≥ khoảng 15 phút |
| Khoảng cách | `toCoupon_GEQ25min` | Thời gian đi đến điểm sử dụng coupon ≥ khoảng 25 phút |
| Hướng | `direction_same` | Nơi sử dụng coupon cùng hướng đến điểm đích |
| Hướng | `direction_opp` | Nơi sử dụng coupon khác hướng đến điểm đích |
| Target | `Y` | `1` = dự định chấp nhận, `0` = không chấp nhận |

> **Lưu ý về địa lý:** Đây là kịch bản lái xe khảo sát, không có toạ độ GPS trong bảng; không kết luận về khoảng cách địa lý chính xác từ các cột `GEQ...`. Không suy ra quan hệ nhân quả từ tỷ lệ chấp nhận.

## Mapping dùng cho Q3 – thói quen phù hợp coupon

| Loại coupon trong CSV | Cột thói quen tương ứng |
| --- | --- |
| `Coffee House` | `CoffeeHouse` |
| `Bar` | `Bar` |
| `Carry out & Take away` | `CarryAway` |
| `Restaurant(<20)` / có thể khác cách hiển thị trên UCI | `RestaurantLessThan20` |
| `Restaurant(20-50)` / có thể khác cách hiển thị trên UCI | `Restaurant20To50` |

**Nhất thiết kiểm tra `df['coupon'].unique()` trước khi dùng mapping**, vì trang mô tả UCI và CSV có thể khác cách ghi ký hiệu `$`. Với tần suất `never`, `less1`, `1~3`, `4~8`, `gt8`, cần chỉ ra cách mã hoá thứ tự và cách xử lý NaN.

## Những kiểm tra nên có

- Giá trị thiếu (số lượng, phần trăm, nhóm dữ liệu liên quan) đặc biệt các cột thói quen và `car`.
- Cột hằng: kiểm tra `toCoupon_GEQ5min` và các cột khác bằng `nunique()` trước khi dùng mô hình.
- Kiểm tra trùng lặp dòng; không tự loại trùng vì có thể là các kịch bản khảo sát tương tự từ nhiều người.
- Không ép `age` hay `income` trực tiếp sang số khi còn nhãn chuỗi.
- Kiểm tra `direction_same` và `direction_opp` có tương thích với nhau hay không.
- Số hàng ở nhóm nhỏ trước khi so sánh, để tránh kết luận từ mẫu quá ít.
