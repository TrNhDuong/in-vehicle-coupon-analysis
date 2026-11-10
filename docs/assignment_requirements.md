# Đối chiếu yêu cầu chính thức – CSC17104 Final Project

Tóm tắt từ đề PDF `CSC17104_2026_Final_Project.pdf` do giảng viên cung cấp, **không thay thế đề gốc**.

| Mục | Yêu cầu | Trong starter |
| --- | --- | --- |
| Nhóm | 2–3 sinh viên | Dương, Hà, Lý |
| Dataset | Dữ liệu thực, public, có license, khoảng ≥3.000 dòng, ≥10 cột; cần duyệt | UCI #603, 12.684 dòng, 25 features; **chưa xác nhận việc duyệt** |
| Các giai đoạn | Collection → Exploration → Questions → Analysis → Reflection | Notebook & tài liệu mẫu |
| Số câu hỏi | 2 × số thành viên, ≥1 câu ML | Q1–Q6, Q6 ML |
| Non-ML | ≥2 tiêu chí/câu, cả nhóm ≥4/6 D1–D6 | Kế hoạch dùng D2,D3,D4,D5,D6; cần thực thi |
| ML | Baseline + ≥2 models; split phù hợp; Pipeline; tuning CV train; test once; errors & interpret | Kế hoạch và notebook Q6 |
| Kết quả | ≥2 biểu đồ/câu; giải thích số liệu và giới hạn | **Chưa có số liệu kết quả** |
| Repo | README, environment.yml, LLM_USAGE.md, data, src, notebooks, slides.pdf | Đã có trừ `slides.pdf` (làm sau) |
| Trình bày | 15 phút presentation + 10 phút Q&A | Dàn ý slide trong docs |
| AI | Chỉ dùng như tutor, ghi nguồn; phải giải thích mọi dòng code | LLM usage template |

## D1–D6

- **D1** Ghép dữ liệu/tables, kiểm tra unmatched keys và row count.
- **D2** Pivot/melt, resampling, rolling windows, lag hay so sánh theo thời kỳ.
- **D3** Tạo biến mới có cơ sở từ cột gốc.
- **D4** Kiểm soát confounders khi so sánh các nhóm.
- **D5** Quantify uncertainty: CI / statistical test / effect sizes.
- **D6** Robustness: kiểm tra kết luận có thay đổi với lựa chọn hợp lý khác.

Chú ý: thời điểm trong ngày `time` **không phải dữ liệu chuỗi thời gian qua nhiều ngày**. Q2 sử dụng **pivot theo `time` và `expiration`** để phù hợp D2.
