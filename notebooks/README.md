# Notebooks – cấu trúc 3 Phase

1. **`01_collection_exploration.ipynb`** *(Phase 1 — Dương & Hà)*: thu thập nguồn dữ liệu, kiểm tra chất lượng/schema, phân phối biến, quan hệ sơ bộ và xuất `data/processed/analysis_ready.csv`.
2. **`02_analysis.ipynb`** *(Phase 2 — Dương, Hà, Lý)*: phân tích thống kê non-ML Q1–Q5 theo giai đoạn (`2.1` Hành trình & thời hạn, `2.2` Thói quen & người đồng hành, `2.3` Tuổi & thu nhập theo người trả lời, `2.4` Tổng hợp & Individual reflections), bao phủ `D2, D3, D4, D5, D6`.
3. **`03_ml_question.ipynb`** *(Phase 3 — Lý)*: dự đoán ý định `Y` bằng Machine Learning (`Dummy`, `LogisticRegression`, `RandomForest`) qua `coupon_project.modeling` với split theo người trả lời, `Pipeline` chống leakage, 5-fold CV, kiểm tra test 1 lần, phân tích lỗi và permutation importance.

> Chạy toàn bộ pipeline 1 lệnh từ thư mục gốc bằng `python scripts/run_all.py`, hoặc mở `jupyter lab` và chạy theo thứ tự `01 → 02 → 03`.
