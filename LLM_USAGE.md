# LLM Usage Log – CSC17104 Final Project

## Quy tắc bắt buộc khi làm việc & dùng LLM

1. **Chỉ chỉnh sửa phần của chính mình:** Ai làm (hoặc dùng LLM hỗ trợ) **chỉ được chỉnh sửa đúng phần bài làm, code/notebook và mục nhật ký của người đó** — tuyệt đối không tự ý sửa phần việc hay nhật ký của thành viên khác.
2. **Đọc bảng phân chia công việc trước khi bắt đầu:** Trước khi làm hoặc nhờ LLM hỗ trợ, hãy đọc mục **[Thành viên & Phân công theo Phase](docs/CONTRIBUTING.md#1-thành-viên--phân-công-theo-phase)** trong `docs/CONTRIBUTING.md` để nắm rõ từng người phụ trách phần nào.
3. **Ghi nhận trung thực mỗi lần dùng đáng kể:** Ai dùng LLM tự ghi vào đúng bảng mang tên mình bên dưới (ngày, công cụ, tóm tắt prompt/mục đích và cách tự kiểm chứng lại trên dữ liệu thật).
4. **Phạm vi hợp lệ:** Chỉ dùng LLM như gia sư hỗ trợ giải thích khái niệm, debug, chuẩn hóa code/tài liệu; **không dùng để bịa số liệu hoặc viết thay kết luận, phân tích và Individual reflection**. Người đứng tên chịu trách nhiệm giải thích toàn bộ code và số liệu trong phần của mình.

---

## Nhật ký riêng từng thành viên

### 1. Trần Nhật Dương (`23120243`)
*(Chỉ Trần Nhật Dương chỉnh sửa mục này)*

| Ngày | Công cụ | Câu hỏi / mục đích sử dụng (tóm tắt) | Tự kiểm chứng & thay đổi đã thực hiện |
| --- | --- | --- | --- |
| `2026-11-17` | `Antigravity (Gemini)` | Hỗ trợ tổ chức `src/coupon_project/` (5 module theo vai trò), gom 3 Phase notebooks, chuẩn hóa `docs/`, viết `scripts/run_all.py` và xuất `slides.pdf` | Tự kiểm tra số liệu thực từ CSV UCI #603, chạy `scripts/run_all.py` (`check_project.py`, `pytest`, 3 notebook từ kernel mới) và đối chiếu nguồn UCI/Wang et al. (2017) |

### 2. Nguyễn Mạnh Hà (`23120248`)
*(Chỉ Nguyễn Mạnh Hà chỉnh sửa mục này)*

| Ngày | Công cụ | Câu hỏi / mục đích sử dụng (tóm tắt) | Tự kiểm chứng & thay đổi đã thực hiện |
| --- | --- | --- | --- |
| `2026-11-16` | `ChatGPT / Codex` | Đọc repo, xác định phạm vi và triển khai bản nháp EDA, Q3–Q4 | AI chuẩn bị code thống kê trong `src/coupon_project/analysis.py`, notebook nháp EDA/Q3–Q4 và đối chiếu Wilson CI; Hà tự đọc, chạy và chịu trách nhiệm diễn giải khi trình bày |
| `2026-11-17` | `ChatGPT / Codex` | Kiểm tra phần EDA và Q3–Q4 trước khi tích hợp | AI rà diff, chạy lại tests và notebook từ kernel mới trước khi tích hợp vào Phase 1 & Phase 2 |

### 3. Hoàng Công Lý (`24120378`)
*(Chỉ Hoàng Công Lý chỉnh sửa mục này)*

| Ngày | Công cụ | Câu hỏi / mục đích sử dụng (tóm tắt) | Tự kiểm chứng & thay đổi đã thực hiện |
| --- | --- | --- | --- |
| `—` | *(Tự điền nếu có dùng LLM cho Q5/Q6)* | *(Tóm tắt prompt/mục đích)* | *(Ghi cách tự kiểm chứng code, số liệu Q5/Q6 và pipeline ML)* |

---

## Trách nhiệm cá nhân trước khi nộp

- Tự kiểm chứng toàn bộ số liệu trên `data/raw/in-vehicle-coupon-recommendation.csv` và hiểu từng dòng code trong phần mình phụ trách.
- Tự viết **Individual reflections** bằng trải nghiệm cá nhân trong [notebooks/02_analysis.ipynb](notebooks/02_analysis.ipynb) và rà soát trích dẫn tại [docs/related_work.md](docs/related_work.md).
