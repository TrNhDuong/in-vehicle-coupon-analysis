---
marp: true
size: 16:9
paginate: true
title: Hà - EDA và Q3/Q4
---

# EDA và chất lượng dữ liệu

Nguyễn Mạnh Hà · Bản nháp có AI hỗ trợ

- 12.684 kịch bản khảo sát, 26 cột
- Ý định chấp nhận: 7.210/12.684, tương ứng **56,84%**
- `car` thiếu **99,15%**, thói quen phù hợp thiếu **1,29%**
- Giữ 74 dòng trùng thêm trong phân tích chính, kiểm tra độ bền riêng

Mỗi dòng là một kịch bản. Dataset không có participant ID rõ ràng.

Nguồn: UCI #603, DOI 10.24432/C5GS4P, CC BY 4.0. Bảng `ha_eda_*.csv`.

---

# Q3: Thói quen phù hợp và ý định nhận

So sánh trong cùng coupon, frequent = `1~3/4~8/gt8`, loại riêng thói quen phù hợp bị thiếu.

| Coupon | Frequent, % (n) | Infrequent, % (n) | Chênh điểm % [CI 95%] |
|---|---:|---:|---:|
| Bar | 68,79 (596) | 29,21 (1.400) | 39,58 [35,09; 44,11] |
| Coffee House | 66,02 (1.922) | 34,62 (2.002) | 31,41 [28,37; 34,36] |
| Carry out & Take away | 74,37 (1.986) | 68,57 (385) | 5,80 [0,83; 10,87] |
| Restaurant(<20) | 71,54 (2.245) | 66,15 (514) | 5,39 [0,91; 9,98] |
| Restaurant(20-50) | 55,53 (506) | 38,38 (964) | 17,15 [11,76; 22,58] |

CI percentile bootstrap 10.000 lượt, giả định dòng độc lập. Nguồn: `ha_q3_primary_contrasts.csv`.

---

# Q3: Độ bền phụ thuộc cách định nghĩa tần suất

- Cả 5 coupon có chênh lệch điểm dương ở cả 4 lựa chọn ngưỡng và xử lý NaN
- Carry out & Take away với ngưỡng `4~8/gt8`: **2,90 điểm %**, CI **[−0,70; 6,42]** ở complete-case
- Bỏ dòng trùng thêm làm thay đổi chênh lệch tối đa **0,29 điểm %**
- Frequent/infrequent không chứng minh tỷ lệ tăng đều ở từng cấp tần suất

Chiều ước lượng ổn định chưa bảo đảm CI luôn nằm cùng phía của 0.

Nguồn: `ha_q3_sensitivity.csv`, `ha_q3_dedup_contrasts.csv`. Hình bổ sung: `ha_q3_frequency_heatmap.png`.

---

# Q4: Mục đích chuyến đi giới hạn phép so sánh

Friend(s) có **3.298** dòng ở No Urgent Place, **0** ở Home và Work.

| So sánh Friend(s) với Alone | Chênh điểm % [CI 95%] | Phạm vi |
|---|---:|---|
| Gộp toàn mẫu | 14,76 [12,81; 16,70] | 10.603 dòng của cặp |
| Chuẩn hóa cùng coupon và destination | 1,33 [−1,78; 4,48] | 4 tầng, 4.414 dòng |

Phạm vi chuẩn hóa giữ **41,6%** dòng của cặp. Hai ước lượng dùng quần thể khác nhau.

Trong Bar và No Urgent Place: **17,99 điểm %** [10,36; 25,67], n=337 so với 291.

Nguồn: `ha_q4_crude_contrasts.csv`, `ha_q4_standardized_contrasts.csv`, `ha_q4_joint_contrasts.csv`.

---

# Giới hạn và hướng kiểm chứng

- Các kết quả mô tả mối liên hệ trong khảo sát về ý định
- Thói quen tự báo cáo, thiếu participant ID và nhóm ít mẫu hạn chế suy rộng
- Q4 không đủ dữ liệu cho mọi tổ hợp người đi cùng và mục đích đi
- Ứng dụng tiếp theo: thử nghiệm ưu đãi theo bối cảnh và đo hành vi đổi coupon thực

Đây là nguồn slide bản nháp, chưa render thành PPTX/PDF. Hà cần tự thực hiện,
kiểm chứng và diễn giải theo quy định AI của môn học.

Nguồn: UCI #603. Phương pháp và bằng chứng: `docs/ha_analysis_protocol.md`, `reports/ha_findings.md`.
