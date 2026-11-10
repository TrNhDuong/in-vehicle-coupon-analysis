# 🗺️ Team workflow – đề xuất triển khai

## Giai đoạn 1: Chọn/duyệt và thống nhất dữ liệu

- Cả nhóm xem [dataset dictionary](dataset_dictionary.md), mở CSV, xác minh giá trị thật của cột.
- Dương dẫn phần nguồn, Hà hỗ trợ audit missing, Lý kiểm tra các cột phù hợp ML.
- Chốt lý do lựa chọn dataset, giấy phép, related work và xin duyệt.

## Giai đoạn 2: EDA dùng chung

- Tất cả thống nhất quy tắc nhập dữ liệu, ghi row count, cách handling missing.
- Không "clean" riêng mỗi người một cách mà không giải thích; nếu làm khác để kiểm tra robustness phải ghi lý do.
- Người khác review notebook `01_collection_exploration.ipynb`.

## Giai đoạn 3: Q1–Q6

| Thành viên | Notebook | Công việc |
| --- | --- | --- |
| Dương | `02A_duong_q1_q2.ipynb` | Q1 khoảng cách/hướng; Q2 thời hạn/thời điểm |
| Hà | `02B_ha_q3_q4.ipynb` | Q3 thói quen; Q4 đi cùng ai |
| Lý | `02C_ly_q5.ipynb` | Q5 tuổi/thu nhập |
| Lý + nhóm hỗ trợ | `03_ml_question.ipynb` | Q6 ML; người còn lại review leakage/split/metrics |

## Giai đoạn 4: Tích hợp & thuyết trình

- Tổng hợp vào `02_analysis.ipynb` bằng mô tả/tài liệu định hướng, không sao chép kết quả sai lệch hoặc không đồng bộ.
- Chọn **3–5 findings quan trọng** có chứng cứ, thảo luận bias của khảo sát.
- Hoàn thiện README, log LLM usage, reflection riêng và xuất `slides.pdf` tại repo root.

**Không có deadline trong repo**: nhóm tự điền mốc thời gian theo thông báo môn học.
