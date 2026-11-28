# LLM Usage Log – CSC17104 Final Project

## Quy tắc bắt buộc khi làm việc & dùng LLM

1. **Hỏi & xác nhận đúng người trước khi sửa:** Trước khi nhờ LLM chỉnh sửa, xác định rõ người dùng là **Dương (`23120243`)**, **Hà (`23120248`)** hay **Lý (`24120378`)**; đọc mục **[Phân công theo Phase](docs/CONTRIBUTING.md#1-thành-viên--phân-công-theo-phase)** trong `docs/CONTRIBUTING.md`.
2. **Chỉ sửa phần của chính mình:** Ai làm (hoặc dùng LLM hỗ trợ) **chỉ được chỉnh sửa đúng phần bài làm, code/notebook và mục nhật ký mang tên mình bên dưới** — không tự ý sửa phần việc hay nhật ký của thành viên khác.
3. **Giữ hợp đồng `src/` & không bịa số liệu:** Đọc [docs/workflow_and_api.md](docs/workflow_and_api.md) trước khi sửa hàm dùng chung; mọi con số báo cáo phải lấy từ kết quả chạy thật (`scripts/run_all.py`, `pytest`), **không** viết hộ phân tích kết luận hoặc *Individual reflections*.
4. **Ghi nhận trung thực & tự kiểm chứng:** Ghi rõ ngày, công cụ, tóm tắt prompt và kết quả kiểm chứng bằng `python scripts/check_project.py` + `python -m pytest -q`. *(Quy tắc tự động cho AI coding agent xem tại [AGENTS.md](AGENTS.md).)*

---

## Nhật ký riêng từng thành viên

### 1. Trần Nhật Dương (`23120243`)
*(Chỉ Trần Nhật Dương chỉnh sửa mục này)*

| Ngày | Công cụ | Câu hỏi / mục đích sử dụng (tóm tắt) | Tự kiểm chứng & thay đổi đã thực hiện |
| --- | --- | --- | --- |
| `2026-11-17` | `Antigravity (Gemini)` | Hỗ trợ tổ chức `src/coupon_project/` (5 module theo vai trò), gom 3 Phase notebooks, chuẩn hóa `docs/`, viết `scripts/run_all.py` và xuất `slides.pdf` | Tự kiểm tra số liệu thực từ CSV UCI #603, chạy `scripts/run_all.py` (`check_project.py`, `pytest`, 3 notebook từ kernel mới) và đối chiếu nguồn UCI/Wang et al. (2017) |
| `2026-11-28` | `Antigravity (Gemini)` | Chuẩn hóa câu chữ 6 câu hỏi nghiên cứu (dịch sang *phiếu ưu đãi*) trong `README.md`, `02_analysis.ipynb`, `slides.pdf` và gỡ `presentation/slides.html` | Tự kiểm tra `slides.pdf` sau xuất, chạy `scripts/check_project.py` và `pytest -q` |

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
| `2026-11-14` | `Claude` | Hỏi giải thích khái niệm & cách thiết kế phương pháp cho Q5–Q6: vì sao cần cluster-bootstrap theo cụm người thay vì bootstrap theo dòng, cách chuẩn hóa trực tiếp (`direct standardization`), cách dùng `GroupShuffleSplit` / `StratifiedGroupKFold`, `ColumnTransformer` + `Pipeline` chống data leakage và ý nghĩa `permutation_importance` | Tự kiểm tra phân bố `age`, `income`, `respondent_id` (567 hồ sơ) trên CSV thật; đối chiếu từng bảng kết quả Q5/Q6 với output chạy từ kernel mới trong môi trường Python 3.11; tự đọc hiểu và giải thích lại toàn bộ logic trước khi chốt diễn giải |
| `2026-11-26` | `Claude` | Gỡ lỗi tương thích cú pháp f-string trên Python 3.11 và rà soát đối chiếu yêu cầu đề cho phần Q5–Q6 (bổ sung bảng cỡ mẫu `n`, kiểm tra ô nhỏ, phân tích lỗi theo `destination` và ví dụ dự đoán sai ngẫu nhiên) | Tự kiểm tra kết quả sau khi chạy lại Phase 2.3 (`02_analysis.ipynb`) và `03_ml_question.ipynb` trong môi trường `python=3.11`; chạy `check_project.py` và `pytest` (`11/11` pass) |
| `2026-11-26` | `Antigravity (Gemini)` | Đóng vai gia sư giải thích kiến trúc codebase (`workflow_and_api.md`, `data.py`, `features.py`, lỗi `AttributeError`/`set()`), chuẩn hóa thống nhất tiếng Việt cho docstring/thông báo lỗi và đối chiếu toàn bộ dự án theo đề chính thức `CSC17104_2026_Final_Project.pdf` | Tự đọc và chỉnh sửa trực tiếp trong `data.py`, xác nhận `check_project.py` đạt và `pytest` pass `11/11`; rà soát danh mục các điểm còn thiếu (`Individual reflection`, `Future work`, `README.md`, đồng bộ số liệu Q6 và merge `final_1` vào `main`) để nhóm hoàn thiện trước khi nộp |

---

## Trách nhiệm cá nhân trước khi nộp

- Tự kiểm chứng toàn bộ số liệu trên `data/raw/in-vehicle-coupon-recommendation.csv` và hiểu từng dòng code trong phần mình phụ trách.
- Tự viết **Individual reflections** bằng trải nghiệm cá nhân trong [notebooks/02_analysis.ipynb](notebooks/02_analysis.ipynb) và rà soát trích dẫn tại [docs/related_work.md](docs/related_work.md).
