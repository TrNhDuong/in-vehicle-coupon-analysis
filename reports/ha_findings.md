# Hà — Q3/Q4: bản nháp AI hỗ trợ

Số liệu tự sinh từ CSV thật. Chưa xác nhận Hà tự thực hiện/diễn giải; xem LLM_USAGE.md.

## Q3

- Bar: frequent 68.79% (n=596, accepted=410), infrequent 29.21% (n=1400, accepted=409); chênh 39.58 điểm %, bootstrap 95% CI [35.09, 44.11].

- Carry out & Take away: frequent 74.37% (n=1986, accepted=1477), infrequent 68.57% (n=385, accepted=264); chênh 5.80 điểm %, bootstrap 95% CI [0.83, 10.87].

- Coffee House: frequent 66.02% (n=1922, accepted=1269), infrequent 34.62% (n=2002, accepted=693); chênh 31.41 điểm %, bootstrap 95% CI [28.37, 34.36].

- Restaurant(20-50): frequent 55.53% (n=506, accepted=281), infrequent 38.38% (n=964, accepted=370); chênh 17.15 điểm %, bootstrap 95% CI [11.76, 22.58].

- Restaurant(<20): frequent 71.54% (n=2245, accepted=1606), infrequent 66.15% (n=514, accepted=340); chênh 5.39 điểm %, bootstrap 95% CI [0.91, 9.98].

- Chênh lệch lớn nhất theo ước lượng điểm: Bar, 39.58 điểm %. Đây không phải kiểm định chênh lệch giữa các effect sizes.

- Bar: 4/4 lựa chọn ngưỡng/NaN có chênh lệch dương; khoảng ước lượng điểm [39.45, 39.82] điểm %. Khoảng này là sensitivity range, không phải CI.

- Carry out & Take away: 4/4 lựa chọn ngưỡng/NaN có chênh lệch dương; khoảng ước lượng điểm [2.65, 5.93] điểm %. Khoảng này là sensitivity range, không phải CI.

- Coffee House: 4/4 lựa chọn ngưỡng/NaN có chênh lệch dương; khoảng ước lượng điểm [22.54, 31.41] điểm %. Khoảng này là sensitivity range, không phải CI.

- Restaurant(20-50): 4/4 lựa chọn ngưỡng/NaN có chênh lệch dương; khoảng ước lượng điểm [17.15, 21.93] điểm %. Khoảng này là sensitivity range, không phải CI.

- Restaurant(<20): 4/4 lựa chọn ngưỡng/NaN có chênh lệch dương; khoảng ước lượng điểm [3.57, 5.60] điểm %. Khoảng này là sensitivity range, không phải CI.

- Độ bất định thay đổi: Carry out & Take away, at_least_4/complete_case, chênh 2.90 điểm % nhưng CI [-0.70, 6.42] chứa 0. Chiều ước lượng dương ổn định không đồng nghĩa mọi lựa chọn đều phân biệt được với 0.

- Độ bất định thay đổi: Carry out & Take away, at_least_4/within_coupon_mode, chênh 2.65 điểm % nhưng CI [-0.88, 6.20] chứa 0. Chiều ước lượng dương ổn định không đồng nghĩa mọi lựa chọn đều phân biệt được với 0.

- Bỏ 74 dòng trùng thêm làm thay đổi chênh lệch tối đa 0.29 điểm %; chưa giải quyết phụ thuộc cùng người.

- Điểm đáng chú ý: Bar, tỷ lệ ở 4~8 là 78.00% (n=150), ở gt8 là 73.47% (n=49). Frequent/infrequent không hàm ý tăng đơn điệu ở mọi cấp; các điểm ước lượng có bất định và không chứng minh tần suất cao hơn làm thay đổi ý định nhận.

- Điểm đáng chú ý: Coffee House, tỷ lệ ở 4~8 là 68.59% (n=538), ở gt8 là 65.79% (n=342). Frequent/infrequent không hàm ý tăng đơn điệu ở mọi cấp; các điểm ước lượng có bất định và không chứng minh tần suất cao hơn làm thay đổi ý định nhận.

- Giả thuyết lý giải: mức quen thuộc/sở thích có thể liên hệ với ý định nhận. Chưa kiểm soát mọi yếu tố, chưa xác định cơ chế.

- Ứng dụng có điều kiện: dùng thói quen như tín hiệu để thiết kế thử nghiệm cá nhân hóa; cần đo hành vi đổi coupon thực và kiểm chứng trên mẫu mới.

- Hạn chế: tần suất tự báo cáo theo khoảng, NaN và nhóm nhỏ, thiếu ID, CI giả định dòng độc lập; mode chỉ là sensitivity, không chứng minh thiếu ngẫu nhiên. Hà tự viết phần nhận xét/bất ngờ sau khi đối chiếu.

## Q4

- Bar: trong nhóm n≥30, cao nhất theo điểm ước lượng Friend(s) 55.79% (n=337; Wilson CI [50.45, 60.99]%), thấp nhất Kid(s) 20.87% (n=206; CI [15.88, 26.93]%). Không kiểm định mọi thứ hạng.

- Coffee House: trong nhóm n≥30, cao nhất theo điểm ước lượng Friend(s) 59.69% (n=1228; Wilson CI [56.92, 62.40]%), thấp nhất Alone 43.79% (n=2256; CI [41.76, 45.85]%). Không kiểm định mọi thứ hạng.

- Carry out & Take away: trong nhóm n≥30, cao nhất theo điểm ước lượng Friend(s) 75.78% (n=739; Wilson CI [72.56, 78.73]%), thấp nhất Kid(s) 70.39% (n=152; CI [62.71, 77.08]%). Không kiểm định mọi thứ hạng.

- Restaurant(<20): trong nhóm n≥30, cao nhất theo điểm ước lượng Friend(s) 80.15% (n=826; Wilson CI [77.29, 82.72]%), thấp nhất Alone 63.83% (n=1435; CI [61.31, 66.28]%). Không kiểm định mọi thứ hạng.

- Restaurant(20-50): trong nhóm n≥30, cao nhất theo điểm ước lượng Partner 63.12% (n=141; Wilson CI [54.91, 70.64]%), thấp nhất Kid(s) 37.36% (n=174; CI [30.51, 44.74]%). Không kiểm định mọi thứ hạng.

- Thô Friend(s) - Alone: 67.34% (n=3298) so với 52.58% (n=7305); chênh 14.76 điểm %, CI [12.81, 16.70].

- Thô Partner - Alone: 59.53% (n=1075) so với 52.58% (n=7305); chênh 6.95 điểm %, CI [3.78, 10.01].

- Chuẩn hóa Friend(s) - Alone, coupon_destination: chênh 1.33 điểm %, CI [-1.78, 4.48]; 4/15 tầng, giữ 4414/10603 dòng của cặp (41.6%). Đây là quần thể common support.

- Chuẩn hóa Friend(s) - Alone, coupon_destination_children: chênh 2.15 điểm %, CI [-0.87, 5.27]; 7/30 tầng, giữ 4082/10603 dòng của cặp (38.5%). Đây là quần thể common support.

- Chuẩn hóa Partner - Alone, coupon_destination: chênh 3.03 điểm %, CI [-1.11, 7.08]; 8/15 tầng, giữ 4495/8380 dòng của cặp (53.6%). Đây là quần thể common support.

- Chuẩn hóa Partner - Alone, coupon_destination_children: chênh 2.31 điểm %, CI [-2.26, 6.72]; 8/30 tầng, giữ 2844/8380 dòng của cặp (33.9%). Đây là quần thể common support.

- Cùng Bar, No Urgent Place: Friend(s) 55.79% (n=337) so với Alone 37.80% (n=291), chênh 17.99 điểm %, CI [10.36, 25.67]. Chiều liên hệ không đồng nhất giữa coupon.

- Cùng Carry out & Take away, No Urgent Place: Friend(s) 75.78% (n=739) so với Alone 84.00% (n=75), chênh -8.22 điểm %, CI [-16.65, 0.96]. Chiều liên hệ không đồng nhất giữa coupon.

- Cùng Coffee House, No Urgent Place: Friend(s) 59.69% (n=1228) so với Alone 58.56% (n=473), chênh 1.13 điểm %, CI [-4.08, 6.33]. Chiều liên hệ không đồng nhất giữa coupon.

- Cùng Restaurant(<20), No Urgent Place: Friend(s) 80.15% (n=826) so với Alone 80.67% (n=445), chênh -0.53 điểm %, CI [-5.11, 4.02]. Chiều liên hệ không đồng nhất giữa coupon.

- Restaurant(20-50), Friend(s) - Alone: không có tầng nào đạt cả hai nhóm n≥30; không tính tỷ lệ/chênh lệch chuẩn hóa. Xem số mẫu ở ha_q4_joint_contrasts.csv.

- Restaurant(20-50), Partner - Alone: không có tầng nào đạt cả hai nhóm n≥30; không tính tỷ lệ/chênh lệch chuẩn hóa. Xem số mẫu ở ha_q4_joint_contrasts.csv.

- Có 6/12 tầng đủ n đổi dấu điểm ước lượng so với cùng coupon chưa phân tầng destination. Đổi dấu không chứng minh khác biệt chắc chắn hay Simpson's paradox; cần xem CI và quần thể.

- Điểm dễ bị bỏ qua: Friend(s) có n=3298 ở No Urgent Place, n=0 ở Home và n=0 ở Work. Không thể ước lượng so sánh bạn bè/một mình ở mọi mục đích chuyến đi.

- Giả thuyết lý giải: lựa chọn người đi cùng gắn với mục đích/bối cảnh; các thói quen và cấu trúc mẫu cũng có thể liên quan. Không chứng minh cơ chế chỉ bằng phân tầng.

- Ứng dụng có điều kiện: thử nghiệm ưu đãi theo bối cảnh có dữ liệu hỗ trợ; không ngoại suy cho Home/Work nếu cặp so sánh không tồn tại.

- Hạn chế: thiếu người tham gia ID, quan sát phụ thuộc tiềm tàng, tự báo cáo, thiếu common support, nhiều so sánh khám phá; has_children không phải đang đi cùng trẻ. Hà cần tự đánh giá điều gì bất ngờ và diễn giải lại từ bảng gốc.

## Bằng chứng

- Q3: reports/tables/ha_q3_primary_contrasts.csv, ha_q3_sensitivity.csv, ha_q3_dedup_contrasts.csv.
- Q4: reports/tables/ha_q4_*rates.csv, ha_q4_*contrasts.csv, ha_q4_sign_reversals.csv.
- Row audit: reports/tables/ha_q3_q4_row_audit.csv.
- Hình: reports/figures/ha_q3_frequency_bars.png, ha_q3_frequency_heatmap.png, ha_q4_passanger_bars.png, ha_q4_destination_heatmaps.png.
- Nguồn: UCI Dataset 603, DOI https://doi.org/10.24432/C5GS4P, CC BY 4.0.
- CI giả định dòng độc lập; bootstrap percentile 10.000 lượt; seed 17104; MIN_N=30.
