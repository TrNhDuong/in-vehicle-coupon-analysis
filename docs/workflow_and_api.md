# Workflow hệ thống, Quan hệ phụ thuộc & Output các hàm (`src/coupon_project`)

Tài liệu mô tả **luồng chạy 1 lệnh (`scripts/run_all.py`)**, **quan hệ phụ thuộc giữa 5 module**, và **hợp đồng Input/Output thống nhất (`%` và `pp`)** của từng hàm.

---

## 1. Workflow tổng thể (4 giai đoạn)

```text
data/raw/in-vehicle-coupon-recommendation.csv
  │
  ├──► Phase 1: 01_collection_exploration.ipynb (Dương + Hà)
  │      data.{load_raw_data, missing_table, target_is_binary, audit_row, save_table}
  │      + features.{matched_frequency, các hằng thứ tự} + stats.{rate_table, wilson_ci}
  │      + plotting.{set_style, save_figure}
  │      ──► data/processed/analysis_ready.csv + 6 bảng tables/eda_*.csv + figures/eda_*.png
  │
  ├──► Phase 2: 02_analysis.ipynb (đọc lại raw độc lập)
  │      ├── 2.1 Q1–Q2 (Dương): features.{add_travel_time_band, check_journey_flags}
  │      │     → stats.{rate_table, contrasts, pivot_expiration} → plotting.{plot_heatmap, plot_bars_ci, save_figure}
  │      ├── 2.2 Q3–Q4 (Hà): features.matched_frequency
  │      │     → stats.{rate_table, contrasts, standardized_contrast} → plotting.{plot_heatmap, save_figure}
  │      ├── 2.3 Q5 (Lý): features.{build_respondent_id, matched_frequency}
  │      │     → stats.{cluster_rates_ci, cluster_diff_ci} → plotting.{plot_heatmap, save_figure}
  │      └── 2.4 Tổng hợp (chung): stats.cluster_diff_ci kiểm tra lại kết luận Q1–Q4 theo người
  │      ──► 13 bảng reports/tables/{q1..q5, summary}_*.csv + reports/figures/{q1..q5}_*.png
  │
  ├──► Phase 3: 03_ml_question.ipynb (Lý, đọc lại raw độc lập)
  │      data.{load_raw_data, save_table} + features.{build_respondent_id, matched_frequency}
  │      → modeling.{build_pipeline, cluster_bootstrap_metric, error_breakdown, probability_bins}
  │      + plotting.{set_style, save_figure}
  │      ──► 8 bảng reports/tables/q6_*.csv + reports/figures/q6_fig1..4.png
  │
  └──► Phase 4: Kiểm chứng & Thuyết trình (Cả nhóm)
         python scripts/run_all.py  (check_project → pytest (44 test) → python -m nbconvert 01, 02, 03)
         slides.pdf (slide thuyết trình cuối kỳ 10 trang ở thư mục gốc)
```

---

## 2. Sơ đồ phụ thuộc giữa 5 module ("Hàm nào cần hàm nào?")

Import thật giữa các module: `plotting` → `data` (lấy `FIGURES_DIR`); `stats` → `features` (lấy `TIME_ORDER`, `EXPIRATION_ORDER`); `data`, `features`, `modeling` không import module nào khác của gói. Sơ đồ dưới đây nhóm các hàm theo vai trò:

```text
data.py (đường dẫn gốc, load_raw_data, missing_table, target_is_binary, save_table, row_count_log, audit_row)
  ├── features.py
  │     ├── add_travel_time_band() ──► gọi check_journey_flags()
  │     └── matched_frequency(), build_respondent_id()
  ├── stats.py  (cùng một chuẩn đơn vị: % cho rate/CI và pp cho diff)
  │     ├── pivot_expiration() ──► cần TIME_ORDER, EXPIRATION_ORDER từ features.py
  │     ├── rate_table()       ──► gọi validate_binary(), wilson_ci() / bootstrap_rate_ci()
  │     ├── contrasts()        ──► gọi validate_binary(), rng_for(), bootstrap_diff_ci()
  │     ├── standardized_contrast() ──► nhận output từ contrasts()
  │     └── cluster_rates_ci(), cluster_diff_ci() ──► gọi _cluster_bootstrap()
  ├── plotting.py (cần FIGURES_DIR từ data.py)
  │     ├── plot_heatmap()     ──► hỗ trợ cả heatmap đơn lẫn ô subplot (ax=)
  │     └── plot_bars_ci()     ──► nhận summary_df đúng schema của stats.rate_table()
  └── modeling.py (import sklearn nội hàm để CI không cần scikit-learn)
        ├── build_pipeline()   ──► ColumnTransformer(SimpleImputer + dense OneHotEncoder) + estimator
        ├── cluster_bootstrap_metric()
        └── error_breakdown(), probability_bins()
```

---

## 3. Hợp đồng Input / Output của từng module

### `data.py` (Cấu hình đường dẫn, Quality & I/O)

| Hàm | Input chính | Output trả về (kiểu & cấu trúc chính xác) |
| --- | --- | --- |
| `load_raw_data(path=RAW_CSV_PATH)` | Đường dẫn CSV | `pd.DataFrame` raw (`12.684 × 26`); tự kiểm tra đủ 26 cột `REQUIRED_COLUMNS` |
| `row_count_log(before, after, action)` | `int, int, str` | `str` dạng `"{action}: {before:,} -> {after:,} rows (delta {after - before:+,})"` |
| `audit_row(action, before, after, reason)` | `str, int, int, str` | `dict` khóa: `action`, `n_before`, `n_after`, `rows_removed`, `reason` |
| `missing_table(df)` | `pd.DataFrame` | `pd.DataFrame` index = tên cột, cột `["missing_count", "missing_pct"]` (%) |
| `target_is_binary(df, target="Y")` | `pd.DataFrame` | `bool` (`True` khi không NaN và chỉ gồm `0, 1`) |
| `save_table(df, name, out_dir=TABLES_DIR)` | `pd.DataFrame, str` | `Path` tới `reports/tables/{name}.csv` (`utf-8-sig`) |

### `features.py` (Biến dẫn xuất & Danh mục chuẩn)

| Hàm | Phụ thuộc nội bộ | Input chính | Output trả về (kiểu & cấu trúc chính xác) |
| --- | --- | --- | --- |
| `check_journey_flags(df)` | — | `df` raw | `dict` khóa: `n_rows`, `geq5_always_one`, `invalid_geq_hierarchy_count`, `direction_complement_ok` |
| `add_travel_time_band(df, col_name="travel_time_band")` | `check_journey_flags` | `df` raw | Bản sao `pd.DataFrame` thêm cột `Categorical` thứ tự `["5-<15 min", "15-<25 min", ">=25 min"]` |
| `matched_frequency(df)` | `COUPON_FREQUENCY`, `FREQUENCIES` | `df` raw | `pd.Series` kiểu `"string"` tên `"matched_frequency"` (giữ `pd.NA`) |
| `build_respondent_id(df, profile_cols)` | — | `df`, cột hồ sơ | `pd.Series` số nguyên ID (`0..k-1`) suy ra từ tổ hợp `profile_cols` |

### `stats.py` (Thống kê nhóm, CI, Contrasts & Cluster Bootstrap)

| Hàm | Phụ thuộc nội bộ | Input chính | Output trả về (kiểu & cấu trúc chính xác) |
| --- | --- | --- | --- |
| `wilson_ci(accepted, n)` | — | `int, int` | `tuple[float, float]`: `(ci_low_pct, ci_high_pct)` theo `%` `[0, 100]` |
| `bootstrap_rate_ci(values, n_boot=2000, seed=42)` | `validate_binary` | Dãy `0/1` | `tuple[float, float]`: `(ci_low_pct, ci_high_pct)` theo `%` |
| `bootstrap_diff_ci(values_a, values_b, n_boot=2000, seed=42)` | `validate_binary` | Hai dãy `0/1` | `dict` khóa: `n_a`, `n_b`, `rate_a_pct`, `rate_b_pct`, `diff_pp`, `ci_low_pp`, `ci_high_pp` |
| `rate_table(df, cols, ci_method="wilson", ...)` | `validate_binary`, `wilson_ci` / `bootstrap_rate_ci` | `df`, list cột | `pd.DataFrame` cột: `[...cols, "n", "accepted", "rate_pct", "ci_low_pct", "ci_high_pct", "small_n"]` |
| `contrasts(df, strata_cols, exposure, group_a, group_b, ...)` | `validate_binary`, `rng_for`, `bootstrap_diff_ci` | `df`, tầng, biến so sánh (nhãn nhóm phải có trong cột, nếu không báo lỗi) | `pd.DataFrame` cột: `[...strata_cols, "group_a", "group_b", "accepted_a", "accepted_b", "n_a", "n_b", "rate_a_pct", "rate_b_pct", "diff_pp", "ci_low_pp", "ci_high_pp", "small_n", "status"]`; `status` ∈ `ok` / `small_n` / `no_common_support`; tầng NaN là một tầng riêng |
| `standardized_contrast(strata_df, ...)` | `contrasts` (input), `rng_for` | Output của `contrasts` | `dict` khóa: `n_strata_total`, `n_strata_used`, `n_comparison_total`, `n_comparison_used`, `coverage`, `diff_pp`, `ci_low_pp`, `ci_high_pp`, `status`. Chỉ dùng tầng có `n ≥ min_n` ở cả 2 nhóm, trọng số `(n_a + n_b)/Σ`; kết quả là chênh lệch **trong các tầng common support** |
| `pivot_expiration(df, index_cols=("time",), target="Y")` | `TIME_ORDER`, `EXPIRATION_ORDER` | `df` raw (nhãn `time`/`expiration` lạ → báo lỗi) | `tuple(rates_pct, counts, long_df)`; `rates` có cột `diff_1d_minus_2h_pp` (pp); `long_df` cột `[*index_cols, "expiration", "rate_pct", "n"]` |
| `cluster_rates_ci(data, group_col, strata_cols=(), unit="respondent", ...)` | `_cluster_bootstrap` | `group_col` dạng `Categorical`, cột `respondent_id`; không được có NaN | `pd.DataFrame` index = categories của `group_col`, cột `["rate_pct", "ci_low_pct", "ci_high_pct"]` (làm tròn 2 chữ số) |
| `cluster_diff_ci(data, group_col, group_a, group_b, strata_cols=(), unit="respondent", ...)` | `_cluster_bootstrap` | `Categorical`, 2 nhãn; `unit="row"` để so sánh với bootstrap theo dòng | `dict` khóa: `rate_a_pct`, `rate_b_pct`, `diff_pp`, `ci_low_pp`, `ci_high_pp` (làm tròn 1 chữ số), `empty_strata_draws` (số lần rút có ô rỗng, bị loại) |

### `plotting.py` & `modeling.py` (Trực quan hóa & ML Q6)

| Hàm | Phụ thuộc nội bộ | Input chính | Output trả về (kiểu & cấu trúc chính xác) |
| --- | --- | --- | --- |
| `plotting.save_figure(fig, name, out_dir=FIGURES_DIR, dpi=160)` | `data.FIGURES_DIR` | `Figure, str` | `Path` tới `reports/figures/{name}.png` |
| `plotting.plot_heatmap(rate_matrix, count_matrix, ..., ax=None)` | `set_style`, `save_figure` | 2 ma trận `DataFrame` | `tuple(fig, ax, im)` (`im` là `AxesImage` để gắn colorbar chung) |
| `plotting.plot_bars_ci(summary_df, x_col, hue_col, ...)` | `stats.rate_table` (schema input), `set_style`, `save_figure` | `summary_df` | `matplotlib.figure.Figure` |
| `modeling.build_pipeline(estimator, cat_cols, bin_cols)` | `sklearn` (lazy import) | Estimator + cột | `sklearn.pipeline.Pipeline` (`ColumnTransformer` + `model`) |
| `modeling.cluster_bootstrap_metric(metric_fn, y_true, y_values, groups, ...)` | `np`, `pd` | Mảng + `groups` | `np.ndarray` gồm `n_boot` điểm bootstrap theo người |
| `modeling.error_breakdown(df, y_true, y_pred, group_col)` | — | Test predictions & nhóm | `pd.DataFrame` index = `group_col`, cột `["n", "true_rate", "acc", "FPR", "FNR"]` (`true_rate`, `acc` là tỷ lệ 0–1; `FPR`, `FNR` là %), sắp theo `true_rate` |
| `modeling.probability_bins(y_true, y_pred, y_proba, ...)` | — | Mảng `y`, xác suất | `pd.DataFrame` index = `p_bin`, cột `["n", "mean_p", "true_y", "acc"]` |
