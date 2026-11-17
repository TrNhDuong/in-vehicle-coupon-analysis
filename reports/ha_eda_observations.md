# EDA của Hà — bản nháp AI hỗ trợ

1. Có 12,684 dòng, 26 cột; Y=1 có 7,210/12,684 (56.84%; Wilson 95% CI [55.98, 57.70]%). Đây là ý định trong khảo sát.

2. car thiếu 12,576 dòng (99.15%); thói quen phù hợp thiếu 164 dòng (1.29%). Không dropna toàn bảng.

3. Có 74 dòng trùng thêm (0.58%); chưa có căn cứ xác định đó là lỗi. Phân tích chính giữ nguyên, kiểm tra độ bền riêng.

4. Cột hằng: toCoupon_GEQ5min. Có 0 vi phạm trong các kiểm tra miền/cờ đã liệt kê; không đồng nghĩa dữ liệu không còn bias.

5. Friend(s): No Urgent Place n=3298, Home n=0, Work n=0. Q4 phải giới hạn so sánh theo common support, không diễn giải crude là tác động của bạn bè.

Nguồn: UCI #603, DOI 10.24432/C5GS4P, CC BY 4.0. Xem ha_eda_*.csv và notebook 01.
