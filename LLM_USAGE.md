# LLM Usage Log – CSC17104 Final Project

> **Bắt buộc ghi lại mỗi lần dùng LLM đáng kể.** Theo đề, LLM (ChatGPT, Claude, Copilot...) có thể dùng như gia sư để giải thích khái niệm, lỗi hoặc API, **không dùng để viết hộ phân tích, kết luận hoặc reflection**. Mọi nội dung nộp phải được người làm hiểu và chịu trách nhiệm.

## Cách ghi

| Ngày | Thành viên | Công cụ | Câu hỏi/prompt (tóm tắt chính xác) | Đã sử dụng / kiểm chứng / thay đổi như thế nào? |
| --- | --- | --- | --- | --- |
| `YYYY-MM-DD` | `Tên` | `ChatGPT / ...` | `Mô tả câu hỏi` | `Cách tự kiểm chứng và kết quả áp dụng` |
| 2026-11-16 | Nguyễn Mạnh Hà (người yêu cầu) | ChatGPT / Codex | Đọc toàn bộ repo và file phân công `PHAN_CONG_CHI_TIET_DUONG_HA_LY.md`; xác định và triển khai phần Hà. | AI đọc các tệp của repo, đối chiếu phạm vi EDA/Q3/Q4 và quy định AI; chuẩn bị code thống kê, notebook, bảng/hình và bản nháp diễn giải; chạy kiểm tra tự động. Chi tiết và kết quả kiểm tra được ghi trong `docs/ha_handoff.md`. **Đây là hỗ trợ vượt vai trò gia sư mà repo cho phép; không được coi là phần Hà đã tự thực hiện hay bản đủ điều kiện nộp.** Chưa xác nhận Hà tự đọc, chạy, sửa hoặc kiểm chứng; Hà cần tự thực hiện theo quy định trước khi sử dụng trong bài nộp. |
| 2026-11-17 | Nguyễn Mạnh Hà (người yêu cầu) | ChatGPT / Codex | Kiểm tra phần Hà đã sẵn sàng push hay chưa. | AI rà diff, phạm vi thay đổi và file Git ignore; chạy lại 10 tests và kiểm tra cấu trúc; thực thi hai notebook từ kernel mới trong bản sao tạm không có processed/reports; đối chiếu 32 bảng, hai báo cáo, processed data và 180 Wilson CI. Kết quả kỹ thuật đạt cho bản nháp gửi nhóm review. Không xác nhận review của Hà/đồng đội, không commit hoặc push. Xem mục kiểm tra ngày 17/11 trong `docs/ha_handoff.md`. |

Phần trình bày của phiên 2026-11-16 gồm nguồn Markdown 5 slide và ghi chú EDA/Q3/Q4; chưa xuất PPTX/PDF vì thiếu runtime skill Presentations. Không có xác nhận Hà đã luyện nói hay viết reflection.

### Ghi nhận cần bổ sung cho việc tạo scaffold

Nhóm cần tự bổ sung thông tin chính xác về việc dùng AI hỗ trợ **tạo bộ khung thư mục, mẫu README và hướng dẫn notebook** trong cuộc trao đổi hiện tại. Ghi rõ thành viên yêu cầu, thời điểm, công cụ và những nội dung nhóm đã tự kiểm tra/sửa đổi. Không xem bản mẫu này là nhật ký đã hoàn tất.

## Những điều phải tự làm

- Tự thiết kế, kiểm tra và thực hiện phân tích trên dữ liệu thật.
- Tự diễn giải kết quả, viết nhận xét, limitations và reflection cá nhân.
- Tự kiểm tra tài liệu, giấy phép và trích dẫn code/notebook tham khảo.
- Tự kiểm tra toàn bộ dòng code trước khi đưa vào bài nộp.
