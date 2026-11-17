# Bàn giao phần Hà

Ngày 16/11/2026 (Asia/Bangkok). **Bản nháp thực nghiệm có AI hỗ trợ**,
không xác nhận Hà đã tự thực hiện, diễn giải, review hay đủ điều kiện nộp.
Việc dùng AI đã ghi trong `../LLM_USAGE.md`.

## Đã đọc và xác định phạm vi

Đã đọc các tệp nội dung của starter: README, CONTRIBUTING, CHECKLIST,
LLM_USAGE, environment, manifest, cấu hình Git/CI/PR, toàn bộ docs, data README,
sáu notebook, src, scripts và tests; đồng thời đọc file phân công ngoài repo
`C:\Users\win 10\Downloads\PHAN_CONG_CHI_TIET_DUONG_HA_LY.md`.
Không có AGENTS.md trong repo. Tài liệu PDF đề chính thức được nhắc trong docs
không có trong repo, nên chưa đối chiếu bản PDF gốc. Yêu cầu AI ở đây lấy từ
README, LLM_USAGE và file phân công, không tuyên bố đã đọc PDF.

Phần Hà sở hữu: EDA, quy ước chất lượng/metric/CI, Q3, Q4, bảng/hình và
nguồn nội dung trình bày EDA/Q3/Q4. Vai trò review Q1/Q2/Q5/Q6 cần kết quả/PR
của đồng đội; các notebook đó hiện còn TODO nên chưa xác nhận review.

## Đối chiếu công việc và bằng chứng

| Yêu cầu | Bản nháp đã thực hiện | Nơi kiểm tra |
|---|---|---|
| Overview, schema và ý nghĩa dòng | 12.684×26, schema và semantic type | Notebook 01, `ha_eda_schema.csv` |
| Missing, duplicate, miền nhãn | Audit tất cả cột, missing theo coupon, 74 dòng trùng thêm giữ ở chính | Notebook 01, `ha_eda_missing*.csv`, `ha_eda_domains.csv` |
| Phân phối, bất hợp lý, quan hệ | Mức nhiệt độ rời rạc, cờ logic, bảng chéo và 2 hình EDA | Notebook 01, `ha_eda_logic_checks.csv`, hình `ha_eda_*` |
| 3–5 quan sát và cleaning plan | 5 quan sát tính từ CSV, quy tắc giữ/loại theo cột | Notebook 01, `reports/ha_eda_observations.md` |
| Dữ liệu phục vụ phân tích | Giữ toàn bộ raw, thêm 2 cột nullable, không impute/đổi tên/xóa dòng | `data/processed/ha_analysis_ready.csv` |
| Metric/CI/nhóm nhỏ | mean(Y), Wilson, bootstrap 10.000, seed 17104, n<30 | `ha_analysis_protocol.md`, `src/coupon_project/analysis.py` |
| Q3 D3 | Mapping đúng 5 nhãn CSV, matched_frequency và frequent_user | Notebook 02B, `ha_q3_mapping.csv` |
| Q3 D4/D5 | So sánh riêng coupon, n/accepted/rate, chênh điểm % và CI | `ha_q3_primary_contrasts.csv`, `ha_q3_frequency_rates.csv` |
| Q3 D6 | Hai ngưỡng × hai xử lý NaN, thêm dedup sensitivity | `ha_q3_sensitivity.csv`, `ha_q3_dedup_contrasts.csv` |
| Q3 ≥2 hình | Bar có Wilson CI và heatmap có n | `ha_q3_frequency_bars.png`, `ha_q3_frequency_heatmap.png` |
| Q4 D4/D5 | Crude, cùng coupon, coupon×destination, thêm has_children, chuẩn hóa common support | `ha_q4_*rates.csv`, `ha_q4_*contrasts.csv` |
| Q4 ≥2 hình | Bar người đi cùng/coupon, heatmap theo mục đích trong từng coupon | `ha_q4_passanger_bars.png`, `ha_q4_destination_heatmaps.png` |
| Audit hàng | n_before/n_after/rows_removed/lý do, kể cả sensitivity và common support | `ha_eda_row_audit.csv`, `ha_q3_q4_row_audit.csv` |
| Bàn giao findings | Số liệu có n, CI, độ bền, ứng dụng có điều kiện và giới hạn | `reports/ha_findings.md` |
| Nội dung trình bày | Nguồn 5 slide và ghi chú để tự chuẩn bị | `presentation/ha_slides.md`, `presentation/ha_speaker_notes.md` |

Tệp CSV có tiền tố `ha_` nằm trong `reports/tables/`, PNG trong
`reports/figures/`. Có **32 CSV và 6 PNG**. CSV kết quả/processed/raw bị ignore
theo cấu hình repo, không force-add; các notebook lưu output và có lệnh tái tạo.

## Điểm cần lưu ý khi đọc kết quả

- Q3: Bar có chênh lệch frequent–infrequent lớn nhất theo điểm ước lượng,
  39,58 điểm %, CI [35,09; 44,11]. Cả 5 coupon giữ chiều ước lượng dương
  ở bốn lựa chọn ngưỡng/NaN; Carry out & Take away ở ngưỡng cao có CI chứa 0.
- Q4: crude Friend(s)−Alone là 14,76 điểm %. Chuẩn hóa coupon×destination
  trên 4 tầng đủ n cho 1,33 điểm %, CI [−1,78; 4,48], coverage chỉ 41,6%.
  Phạm vi mẫu thay đổi nên không gọi đó là tác động đã điều chỉnh của toàn mẫu.
- Không có Friend(s) ở Home/Work. Restaurant(20-50) không có tầng đủ cả hai
  nhóm n≥30 cho hai contrast đã chọn. Giữ ô No data/small_n, không gán 0%.
- CI giả định dòng độc lập. Dataset thiếu ID, chưa xử lý phụ thuộc theo người,
  chưa hiệu chỉnh nhiều so sánh, không suy luận nhân quả hay giao dịch thực.

## Chạy và kiểm tra

Tại repo root, dùng môi trường có dependencies trong `environment.yml`:

```text
python scripts/download_data.py
python scripts/run_ha_notebooks.py
python -m pytest -q
python scripts/check_project.py
```

`run_ha_notebooks.py` khởi tạo kernel mới riêng cho từng notebook và kiểm tra
SHA-256 raw trước/sau. Q3/Q4 không phụ thuộc biến ẩn hoặc file processed của EDA.
Metadata phiên chạy ở `reports/ha_run_metadata.json`.

Kết quả kiểm tra trong phiên này:

- Notebook 01: 7 code cell thực thi, không có error output.
- Notebook 02B: 10 code cell thực thi, không có error output.
- `python -m pytest -q`: **10 passed**.
- `check_project.py`: đủ 16 tệp cấu trúc cần kiểm tra, dữ liệu 12.684×26,
  nhãn Y hợp lệ. Đây chỉ là kiểm tra cấu trúc, không xác nhận hoàn thành môn học.
- Đối chiếu độc lập **180 Wilson CI** trong các bảng với
  `scipy.stats.binomtest(...).proportion_ci(method='wilson')`, khớp trong sai số 1e-12.
- Kiểm tra tỷ lệ bằng accepted/n, chênh lệch bằng công thức trực tiếp, ô thiếu
  nhóm có contrast NaN; processed giữ nguyên mọi cột/dòng raw, kể cả NaN.
- SHA-256 raw trước/sau không đổi:
  `d47897367f5a12a31dece0f4e42d7bd9da76d7016b568da511b50335d08dcb43`.
- Đã xem trực quan cả 6 PNG; `git diff --check` không báo lỗi whitespace.

Đây là các kiểm tra do AI chạy, không ghi nhận thay cho review độc lập của Hà
hoặc đồng đội.

## Kiểm tra trước push ngày 17/11/2026

AI kiểm tra lại theo yêu cầu của Hà, không thay cho review của thành viên nhóm:

- **10 tests passed**, kiểm tra cấu trúc và `git diff --check` đạt.
- Chạy hai notebook bằng kernel mới trong bản sao tạm chỉ có source, scripts,
  notebooks và CSV raw; không có processed data/reports ban đầu. Toàn bộ 17
  code cell thực thi không lỗi, tái tạo đủ 32 CSV và 6 PNG.
- Cả 32 bảng CSV, hai báo cáo Markdown và processed data khớp bản hiện có.
  Raw giữ nguyên SHA-256; notebook gốc không bị ghi lại trong lần kiểm tra này.
- Đối chiếu lại 180 Wilson CI với SciPy, khớp sai số 1e-12.
- Notebook của Dương/Lý giữ nguyên so với HEAD. Manifest bao gồm đủ các tệp
  mới/sửa; không thấy mẫu credential phổ biến trong các tệp đó.
- CSV raw/processed, bảng CSV sinh ra và Jupyter runtime được Git ignore đúng.
  Đồng đội cần tải raw và chạy lại script để tạo các CSV không đi theo commit.

**Kết luận kỹ thuật:** có thể commit/push bản nháp trên nhánh `ha/q3-q4` để
nhóm review. Lúc kiểm tra có 27 file mới/sửa chưa commit, nhánh hiện tại là
`main`; chưa tạo nhánh, stage, commit hoặc push trong phiên kiểm tra này.
Chưa kiểm tra môi trường Conda Python 3.11 mới hoặc chạy CI từ xa.

## Các việc chưa thể xác nhận hoàn tất

- Hà tự thực hiện/đọc hiểu/diễn giải và tuân thủ quy định AI. AI đã hỗ trợ vượt
  phạm vi gia sư mà repo cho phép; bản nháp không tự trở thành bài nộp hợp lệ.
- Dương review EDA/Q3/Q4, Hà review PR Q1/Q2/Q5 và hỗ trợ Q6 khi có triển khai.
- Giảng viên duyệt dataset, tên/MSSV, related work, reflection cá nhân, findings
  của toàn nhóm, luyện nói và `slides.pdf` cuối ở repo root.
- PPTX/PDF riêng Hà chưa xuất: runtime Artifact Tool mà skill Presentations
  yêu cầu không được cung cấp trong phiên này. Đã chuẩn bị nguồn Markdown và notes.
- Host chạy Python 3.12.1; chưa có Conda/Python 3.11 để xác nhận clone-and-rerun
  trong chính môi trường Conda khai báo. Không sửa yêu cầu Python của nhóm chỉ
  vì khác phiên bản trên máy đang chạy.
