# Báo cáo sửa đổi – nhánh `ly/final-fixes`

**Người thực hiện:** Hoàng Công Lý (`24120378`) · **Ngày:** 2026-11-26 · **So với:** `final_1`
**Người cần review:** Trần Nhật Dương, Nguyễn Mạnh Hà

> **Tóm tắt:** Nhánh này (1) hoàn thiện Q5–Q6 sau khi gộp notebook, (2) đồng bộ số liệu Q6 lên slide/README theo môi trường `python=3.11`, (3) Việt hóa docstring và thông báo lỗi, và (4) **rút gọn code toàn dự án** (đã được hai anh đồng ý) mà **không đổi bất kỳ con số, bảng hay hình nào**.

---

## 1. Rút gọn code toàn dự án (4 commit mới nhất)

### 1.1. Cách kiểm chứng "kết quả không đổi"

Chạy cả 3 notebook của **bản trước khi rút gọn** và **bản sau khi rút gọn** trong 2 thư mục tạm riêng, cùng env `python=3.11` (`environment.yml`), rồi so sánh tự động:

| Hạng mục | Kết quả |
| --- | --- |
| 22 bảng `reports/tables/*.csv` | **22/22 giống hệt** (`DataFrame.equals`) |
| `data/processed/analysis_ready.csv` | **Giống hệt** (cùng MD5) |
| Hình `reports/figures/*.png` | **Trùng từng byte** giữa hai lần chạy |
| Output in ra trong notebook (bảng, `print`) | **62/62 giống hệt**, kể cả các bảng không lưu file (bảng kiểm tra rò rỉ Q6) |
| `python -m pytest -q` | **11/11 pass** |
| `python scripts/check_project.py` | **Đạt** |

`key` và `seed` của mọi lệnh bootstrap được giữ nguyên, nên CI và số liệu không thay đổi.

### 1.2. Thay đổi trong `src/` (commit `200a05b`)

| File | Thay đổi | Lý do |
| --- | --- | --- |
| `stats.py` | Gộp `_cluster_rate_fn` + `_cluster_draws` thành **một hàm `_cluster_bootstrap`**, có chú thích theo 2 bước: gán dòng vào ô (nhóm × tầng) và chuẩn hóa trực tiếp → bootstrap theo người | Trước đây logic tách đôi qua closure, khó giải thích khi Q&A |
| `stats.py` | `rate_table`: bỏ các nhánh `if n` thừa | Nhóm từ `groupby(observed=True)` luôn có ≥ 1 dòng |
| `stats.py` | `contrasts`: bỏ rẽ nhánh khi gọi `bootstrap_diff_ci`, viết `status` bằng `if/else` rõ ràng | `bootstrap_diff_ci` đã tự xử lý nhóm rỗng |
| `modeling.py` | **`error_breakdown` bỏ tham số `y_proba`**; FPR/FNR viết đúng theo định nghĩa (trong các dòng thật sự từ chối/nhận, bao nhiêu % bị đoán sai) | Tham số `y_proba` không được dùng |
| `features.py` | `matched_frequency`: bỏ nhánh `continue` thừa | Mask rỗng vẫn chạy đúng |

> ⚠️ **Thay đổi hợp đồng API:** `error_breakdown(df, y_true, y_pred, group_col)` (không còn `y_proba`). Đã cập nhật `docs/workflow_and_api.md`, `tests/test_modeling.py` và nơi gọi duy nhất trong `03_ml_question.ipynb`. Không còn nơi nào khác gọi hàm này.

Các module `data.py`, `plotting.py` và `scripts/` vốn đã gọn nên **không sửa**.

### 1.3. Thay đổi trong notebook

| Notebook / phần | Thay đổi |
| --- | --- |
| `01` Phase 1.3 (commit `6bba952`) | Tạo `frequent_user` bằng bảng ánh xạ `IS_FREQUENT` thay cho 3 dòng `loc`/`isin`; `matched_frequency` được tính ngay tại cell dùng nó; chọn cột bảng tóm tắt sau khi `concat` |
| `02` Q1 (commit `3a54320`) | Gom 6 lệnh `contrasts` vào `dist_tables` / `dir_tables`; display và lưu bảng bằng 1 vòng lặp; đặt tên `NEAR`, `FAR` |
| `02` Q2 | Gom contrasts vào `q2_tables`; Hình 3 duyệt từng dòng bằng `iterrows()`, bỏ `reset_index`; đặt biến `at_10am` cho bảng giải thích nghịch lý |
| `02` Q3 | Tách 2 hàm `handle_missing()` (2 cách xử lý thiếu) và `frequent_contrast()`; vòng lặp D6 và kiểm tra bỏ trùng dùng chung 2 hàm này thay vì viết lặp |
| `02` Q4 | Gom tham số lặp lại thành `BOOT = {"n_boot": 10000, "seed": 17104}`; đặt biến `label`, `friend_ok` |
| `02` Q5 | Tách cell dài thành 3 cell: **chuẩn bị dữ liệu / D4+D5 / D6**; các mapping gộp nhóm có tên riêng (`AGE_GROUP`, `INCOME_GROUP`, `FREQ_1`, `FREQ_4`, `AGE_HALF`, `INCOME_HALF`) và dùng chung hàm `regroup()`; D6 dùng helper `sensitivity()`; Hình 3 bỏ câu `if … else` khó đọc |
| `03` Q6 (commit `4779cf3`) | `SCORING` thành list; bảng CV và bảng rò rỉ dùng vòng lặp thường; **kiểm tra rò rỉ dùng lại ROC-AUC CV theo người đã có** (không chạy lại 5 fold, nhanh hơn, số y hệt); bảng lỗi theo `coupon`/`passanger`/`destination` gom vào 1 vòng lặp; tách 2 cell dài thành 5 cell |

Notebook `02` dài thêm ~30 dòng vì các dòng dài được tách ra và có thêm chú thích (4 → 18 dòng chú thích). Mục tiêu là **dễ đọc và dễ giải thích**, không phải ít dòng nhất.

**Không thay đổi:** nội dung Markdown, kết luận, *Individual reflections*, file hình trong `reports/figures/`.

---

## 2. Các thay đổi trước đó trên nhánh (so với `final_1`)

| Nhóm | Commit | Nội dung |
| --- | --- | --- |
| Q5–Q6 | `d45d9b6`, `7836568` | Thêm Future work, điểm bất ngờ; Q6 thêm phân tích lỗi theo `destination`, ví dụ dự đoán sai rút ngẫu nhiên, sửa làm tròn importance của `Bar`; **sửa f-string không chạy được trên Python 3.11** |
| Hình Q6 | `2d71fa5`, `57c39b9`, `580a20d`, `9525344` | Xuất lại 4 hình Q6 từ lần chạy `python=3.11` |
| Slide | `4b8f285`, `2d36c94`, `ce16fde` | Đồng bộ số Q6 trên slide 8–10 (ROC-AUC **0,782**, bal. acc **0,705**, accuracy **72,3%**, `Bar` FNR **53,0%**) và xuất lại `slides.pdf` |
| EDA | `bd754fd`, `da84c33`, `4fb90c4` | Chạy lại notebook 01 và 2 hình EDA trên Python 3.11 |
| Việt hóa | `fb6df92` → `3790217` (9 commit) | Docstring, chú thích và thông báo lỗi tiếng Việt trong `src/` và `scripts/` (không đổi logic) |
| Tài liệu | `867cb9f`, `4257f8e` | README thêm 6 câu hỏi, kết quả chính, related work; cập nhật mục của Lý trong `LLM_USAGE.md` |

**Lý do số Q6 thay đổi nhẹ so với `final_1`:** bản trên `final_1` chạy trên Python ≥ 3.12, còn `environment.yml` khai báo `python=3.11`. Q1–Q5 không đổi số.

---

## 3. Cách tự kiểm tra lại

```bash
git checkout ly/final-fixes
conda activate csc17104-coupon
python scripts/check_project.py
python -m pytest -q          # 11 passed
python scripts/run_all.py    # chạy lại 01 → 02 → 03
```

Đề nghị review theo thứ tự: `src/coupon_project/stats.py` (hàm `_cluster_bootstrap`) → `modeling.py` (`error_breakdown`) → các cell code của phần mình phụ trách trong `02_analysis.ipynb`.
