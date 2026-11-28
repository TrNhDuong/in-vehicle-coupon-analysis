# Hướng dẫn cộng tác, Nguyên tắc code & Checklist nộp bài (CSC17104)

## 1. Thành viên & Phân công theo Phase

| Thành viên | MSSV | Nhánh | Phạm vi sở hữu (code, notebook, docs) | Kiểm tra chéo |
| --- | --- | --- | --- | --- |
| **Trần Nhật Dương** | `23120243` | `duong/q1-q2` | `01` Phase 1.1 (Collection) · `02` Phase 2.1 (**Q1–Q2**) · `plotting.py`, `stats.py` (CI), `docs/related_work.md`, `README.md`, `scripts/` | Hà |
| **Nguyễn Mạnh Hà** | `23120248` | `ha/q3-q4` | `01` Phase 1.2–1.3 (EDA) · `02` Phase 2.2 (**Q3–Q4**) · `data.py`, `features.py`, `docs/dataset_dictionary.md` | Dương |
| **Hoàng Công Lý** | `24120378` | `ly/q5-ml` | `02` Phase 2.3 (**Q5**) · `03` Phase 3 (**Q6 ML**) · `stats.py` (cluster CI), `modeling.py` | Dương + Hà |

**Nguyên tắc phân công:** Ai phụ trách (hoặc dùng LLM hỗ trợ) **chỉ chỉnh sửa đúng phần việc/file của người đó** và mục riêng mang tên mình trong `LLM_USAGE.md`; phần tích hợp chung (`02` Phase 2.4, `docs/research_questions.md`, `slides.pdf`) chỉ cập nhật khi ghép bài hoặc thống nhất chung. Mỗi thành viên trình bày 2 câu sở hữu và nắm toàn bộ project phục vụ **15 phút thuyết trình + 10 phút Q&A**.

---

## 2. Nguyên tắc phối hợp code dùng chung (5 quy tắc)

1. **Single Source of Truth (`src/` xử lý logic, notebook chỉ gọi hàm):** Không viết lặp hàm tính CI, bootstrap, mapping hay pipeline ML trong nhiều notebook; toàn bộ logic dùng chung nằm tại `src/coupon_project/` (`data`, `features`, `stats`, `plotting`, `modeling`).
2. **Contract-first (Giữ ổn định tham số & schema output):** Trước khi đổi signature, kiểu trả về hoặc tên cột output của một hàm, đối chiếu hợp đồng tại [docs/workflow_and_api.md](workflow_and_api.md) và cập nhật đồng bộ nơi gọi + unit tests.
3. **Pure Functions & Bất biến dữ liệu:** Không sửa `data/raw/`; mọi hàm biến đổi thao tác trên bản sao (`df.copy()`). Cả 3 Phase notebooks đọc lại dữ liệu độc lập qua `load_raw_data()`, không phụ thuộc biến ẩn từ notebook khác.
4. **Cô lập môi trường CI:** Không import `matplotlib`/`scikit-learn` ở top-level của `data.py`, `features.py`, `stats.py`, `modeling.py` để GitHub CI (chỉ cài `pandas + pytest`) luôn chạy pass nhanh.
5. **Fail-fast & Tái lập 1 lệnh trước khi merge:** Mọi bước lọc dòng phải ghi `row_count_log`/`audit_row`; trước khi merge vào `main` chạy:
   ```bash
   python scripts/check_project.py
   python -m pytest -q
   python scripts/run_all.py    # Chạy check -> pytest -> execute 01, 02, 03
   ```

---

## 3. Tiêu chí môn học & Kịch bản thuyết trình (15' + 10' Q&A)

| Tiêu chí | Định nghĩa ngắn | Áp dụng trong đồ án |
| --- | --- | --- |
| **D1** | Ghép bảng / kiểm tra unmatched keys | *(Không áp dụng — dùng D2–D6 = 5/6 ≥ 4/6)* |
| **D2** | Pivot / melt / so sánh theo khung giờ | **Q2** (`time × expiration` pivot & melt) |
| **D3** | Tạo biến mới có cơ sở từ cột gốc | **Q1** (`travel_time_band`), **Q3** (`matched_frequency`) |
| **D4** | Kiểm soát confounders khi so sánh | **Q1–Q5** (phân tầng & chuẩn hóa trực tiếp) |
| **D5** | Định lượng bất định (CI / effect size) | **Q1–Q5** (Wilson CI & bootstrap / cluster-bootstrap CI 95%) |
| **D6** | Kiểm tra độ bền (sensitivity analysis) | **Q3** (4 biến thể ngưỡng/NaN + dedup), **Q5** (ngưỡng, gộp nhóm, bootstrap unit) |

**Bố cục thuyết trình (`slides.pdf` ở root):**
1. Mở đầu & Bối cảnh/EDA (Slides 1–2, ~3') · 2. Dương Q1–Q2 (Slides 3–4, ~3') · 3. Hà Q3–Q4 (Slides 5–6, ~3') · 4. Lý Q5–Q6 ML (Slides 7–9, ~4') · 5. Tổng kết, Hạn chế & Reflection (Slide 10, ~2').

---

## 4. Checklist trước khi nộp cuối kỳ

- [x] Nguồn UCI #603 (`12.684 × 26`, DOI `10.24432/C5GS4P`, **CC BY 4.0**), `related_work.md` & attribution đầy đủ.
- [x] EDA, schema, missingness, duplicate audit, kiểm tra cờ logic & `analysis_ready.csv` trong `01_collection_exploration.ipynb`.
- [x] Đủ **6 câu hỏi (Q1–Q6)** có motivation, ≥2 biểu đồ/câu, kết luận định lượng, hạn chế & bao phủ **5/6 tiêu chí (`D2–D6`)** trong `02_analysis.ipynb`.
- [x] ML Q6 (`03_ml_question.ipynb` + `modeling.py`): prediction-time audit, `GroupShuffleSplit` theo `respondent_id`, `Pipeline` chống leakage, 5-fold CV, test once, error breakdown & permutation importance.
- [x] `README.md` đủ MSSV, `pyproject.toml`, `environment.yml` (đã ghim phiên bản) + `requirements.txt`, `scripts/run_all.py`; có `slides.pdf` ở root; `check_project.py` & `pytest` (44 test) pass.
- [x] Mỗi câu có **Câu hỏi → Lợi ích → Tiền xử lý → Phân tích → Kết quả**; Phase 1 trả lời đủ các câu hỏi khám phá của đề; có mục Tài liệu tham khảo; mọi con số trong markdown có output chứng minh (rà soát 28/11, xem `docs/BAO_CAO_KIEM_TRA.md`).
- [ ] **Thành viên tự hoàn tất trước khi nộp:** Xác nhận giảng viên đã duyệt dataset; mỗi thành viên tự viết *Reflection* (khó khăn, điều học được) trong `notebooks/02_analysis.ipynb`, rà soát mục cá nhân trong `LLM_USAGE.md` và tự giải thích được mọi đoạn code trước Q&A (ôn bằng `docs/HUONG_DAN_HE_THONG.md`, `docs/NGAN_HANG_VAN_DAP.md`).
- [ ] **Theo đề (teamwork & mốc thời gian):** dán link Google Sheets/Trello kế hoạch vào README (bản sao `docs/KE_HOACH_CONG_VIEC.md`); merge nhánh cuối vào `main` trước 9:00 ngày x−2 và mở GitHub issue báo hoàn thành; mỗi người review project một nhóm khác; nộp bản cuối lên GitHub + Moodle ngày x−1.
