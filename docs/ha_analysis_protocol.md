# Quy ước EDA và Q3–Q4 của Hà

Đây là **bản nháp thực nghiệm có AI hỗ trợ**, không phải xác nhận Hà đã tự làm,
review hoặc đủ điều kiện nộp. Repo yêu cầu LLM chỉ đóng vai trò gia sư; xem
`LLM_USAGE.md`. Hà cần tự thực hiện và diễn giải theo quy định môn học.

## Phạm vi và cách chạy

- EDA trong `notebooks/01_collection_exploration.ipynb`; giữ phần Collection của Dương.
- Q3/Q4 trong `notebooks/02B_ha_q3_q4.ipynb`.
- Tiện ích thống kê: `src/coupon_project/analysis.py`.
- Chạy tại repo root: `python scripts/download_data.py`, sau đó
  `python scripts/run_ha_notebooks.py`. Hoặc mở Jupyter, restart/run all hai notebook.
- Mọi bảng/hình có tiền tố `ha_`; CSV kết quả và processed bị `.gitignore` loại
  theo quy ước repo, được tái tạo khi chạy notebook. Không force-add dữ liệu.
- Hai notebook đọc raw độc lập; Q3/Q4 không phụ thuộc trạng thái kernel của EDA.
- Chưa làm Q1/Q2/Q5/Q6, chưa xác nhận review PR, giảng viên duyệt dataset,
  reflection cá nhân, hoặc slide cuối của nhóm.

## Chốt lựa chọn trước khi tính Q3/Q4

1. Đơn vị là **dòng kịch bản khảo sát**. `Y=1` là ý định chấp nhận.
   Giữ dòng trùng hoàn toàn ở phân tích chính vì không có participant ID để
   phân biệt bản ghi lỗi với câu trả lời giống nhau; chạy thêm Q3 không trùng
   như sensitivity, không tuyên bố đã loại được phụ thuộc theo người.
2. Tỷ lệ = `sum(Y)/n = mean(Y)`; bảng gồm `n`, `accepted`, `rate`, CI 95%.
   Tỷ lệ lưu ở [0,1]; biểu đồ dùng %, chênh lệch dùng **điểm phần trăm**.
3. CI tỷ lệ dùng Wilson 95% không continuity correction. CI chênh lệch dùng
   percentile bootstrap 10.000 lượt, seed gốc 17104 và khóa ổn định SHA-256.
   Với Y nhị phân, lấy mẫu lại tổng thành công bằng Binomial(n, mean(Y))
   tương đương bootstrap các dòng trong từng nhóm, tiết kiệm bộ nhớ.
4. Cả hai CI giả định dòng độc lập. Không có ID nên chưa bootstrap theo người;
   CI có thể quá hẹp. CI bootstrap có thể suy biến ở nhóm toàn 0/toàn 1.
   CI này có tính khám phá, chưa hiệu chỉnh nhiều so sánh; không dùng để tuyên bố
   quan hệ nhân quả hay "ý nghĩa" dựa riêng vào CI không chứa 0.
5. Chốt `MIN_N=30` trước kết quả: đánh dấu `*` cho nhóm nhỏ; không xếp hạng
   hay diễn giải mạnh những nhóm này. Đây là quy ước trình bày, không bảo đảm
   power/đại diện/độc lập. Nhóm trống là `No data`, không phải 0%.
6. Q3: ánh xạ **nhãn CSV thực** sang đúng cột thói quen, tạo `matched_frequency`.
   `frequent_user`: 1 nếu `1~3/4~8/gt8`, 0 nếu `never/less1`, thiếu vẫn thiếu.
   Ngưỡng thay thế: `4~8/gt8` so với `never/less1/1~3`.
   Hai cách xử lý thiếu: loại riêng dòng thiếu **thói quen phù hợp** khỏi
   contrast, và điền mode trong cùng coupon không dùng Y (chỉ sensitivity).
   Bảng mô tả vẫn giữ nhóm Unknown. Điền mode giả định người thiếu giống
   nhóm phổ biến, không chứng minh missing-at-random và không dùng cho ML.
7. Q4: chọn trước hai contrast `Friend(s) - Alone`, `Partner - Alone`.
   So sánh thô, cùng coupon, cùng coupon × destination; bổ sung has_children.
   `has_children` là có con, không đồng nhất với `passanger=Kid(s)`.
8. Q4 chuẩn hóa: chỉ giữ tầng có **cả hai nhóm n≥30**. Dùng cùng trọng số
   `w_s=(n_As+n_Bs)/sum_s(n_As+n_Bs)` cho hai nhóm; lấy tổng `w_s*(p_As-p_Bs)`.
   Bootstrap giữ cố định trọng số và n từng tầng. Báo số tầng, dòng giữ lại và
   coverage trên đúng hai nhóm so sánh. Kết quả chỉ áp dụng cho common support;
   khác quần thể so với crude nên không gọi là hiệu ứng nhân quả đã điều chỉnh.
9. Log trước/sau mọi lọc dùng để phân tích, kể cả thiếu, sensitivity và common
   support. Groupby chỉ tổng hợp; `n` ở từng hàng cho biết số dòng tham gia.
10. Hình dùng cùng thang 0–100%, title/trục/chú giải/n, CI nếu có; tên file
    ổn định, xuất PNG 160 dpi vào `reports/figures/`, CSV vào `reports/tables/`.

## Bàn giao cho Dương/Lý

- `data/processed/ha_analysis_ready.csv`: giữ thứ tự và mọi cột raw, thêm
  `matched_frequency` và `frequent_user`; không impute, không drop dòng/cột.
  Đây là bản phục vụ mô tả, không phải dữ liệu đã fit preprocessing cho ML.
- `ha_q3_sensitivity.csv` có đầy đủ ngưỡng × xử lý thiếu × coupon.
- `ha_q4_*` có bảng tỷ lệ, contrasts, common-support coverage và row audit.
- `reports/ha_findings.md` là bản nháp số liệu tự sinh có nguồn bảng/hình;
  `presentation/ha_speaker_notes.md` là ghi chú để Hà tự chuẩn bị phần nói.
- Notebook Q1/Q2/Q5/Q6 hiện là TODO: chưa thể review kết quả/leakage thực nghiệm.
  Khi có PR thật, Hà kiểm tra row counts, CI, n nhỏ, mapping và split/Pipeline
  của ML; không đánh dấu hoàn thành trước khi có bằng chứng.

## Nguồn

- [UCI Dataset 603](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation),
  DOI [10.24432/C5GS4P](https://doi.org/10.24432/C5GS4P), CC BY 4.0.
- [SciPy: proportion_ci](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html):
  tài liệu Wilson và các tài liệu gốc được dẫn trong trang. Công thức Wilson
  được hiện thực độc lập trong `analysis.py`; không sao chép public notebook.
