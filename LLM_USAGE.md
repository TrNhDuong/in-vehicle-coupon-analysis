# LLM Usage Log – CSC17104 Final Project

> **Bắt buộc ghi lại mỗi lần dùng LLM đáng kể.** Theo đề, LLM (ChatGPT, Claude, Copilot...) có thể dùng như gia sư để giải thích khái niệm, lỗi hoặc API, **không dùng để viết hộ phân tích, kết luận hoặc reflection**. Mọi nội dung nộp phải được người làm hiểu và chịu trách nhiệm.

## Nhật ký sử dụng theo thành viên

| Ngày | Thành viên | Công cụ | Câu hỏi/prompt (tóm tắt chính xác) | Đã sử dụng / kiểm chứng / thay đổi như thế nào? |
| --- | --- | --- | --- | --- |
| `2026-11-17` | `Trần Nhật Dương` | `Antigravity (Gemini)` | `Hỗ trợ tách module thống kê/trực quan dùng chung và triển khai phần Q1, Q2, data collection, related work theo đúng yêu cầu đồ án; rút gọn code và hoàn thiện tài liệu/slide tổng hợp` | `Sinh viên tự kiểm tra số liệu thực từ CSV UCI #603, chạy lại toàn bộ unit test (pytest) và notebook 02A_duong_q1_q2.ipynb từ kernel mới; đối chiếu nguồn UCI/Wang et al. (2017) trước khi chốt nội dung.` |
| `2026-11-16` | `Nguyễn Mạnh Hà (người yêu cầu)` | `ChatGPT / Codex` | `Đọc toàn bộ repo và file phân công PHAN_CONG_CHI_TIET_DUONG_HA_LY.md; xác định và triển khai phần Hà.` | `AI đọc các tệp của repo, đối chiếu phạm vi EDA/Q3/Q4 và quy định AI; chuẩn bị code thống kê, notebook, bảng/hình và bản nháp diễn giải; chạy kiểm tra tự động (chi tiết tại docs/ha_handoff.md). Hà cần tự đọc, chạy, chỉnh sửa và chịu trách nhiệm diễn giải trước khi nộp.` |
| `2026-11-17` | `Nguyễn Mạnh Hà (người yêu cầu)` | `ChatGPT / Codex` | `Kiểm tra phần Hà đã sẵn sàng push hay chưa.` | `AI rà diff, phạm vi thay đổi và file Git ignore; chạy lại tests và 2 notebook từ kernel mới; đối chiếu 32 bảng, báo cáo, processed data và Wilson CI (xem docs/ha_handoff.md).` |
| `2026-11-17` | `Hoàng Công Lý` | `(Bổ sung nếu có sử dụng LLM cho Q5/Q6)` | `(Ghi tóm tắt prompt nếu có)` | `(Ghi cách tự kiểm chứng lại code và số liệu Q5/Q6)` |

## Những điều từng thành viên tự chịu trách nhiệm

- Tự kiểm chứng toàn bộ số liệu trên dữ liệu thật (`data/raw/in-vehicle-coupon-recommendation.csv`), không dùng số liệu ước đoán.
- Tự đọc hiểu từng dòng code trong `src/` và `notebooks/`, sẵn sàng giải thích trong phần Q&A.
- Tự viết **Individual reflections** bằng trải nghiệm cá nhân trong `notebooks/02_analysis.ipynb`.
- Tự rà soát trích dẫn nguồn, giấy phép CC BY 4.0 và `docs/related_work.md`.
