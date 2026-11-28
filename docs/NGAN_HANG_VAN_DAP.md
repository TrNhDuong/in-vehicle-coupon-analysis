# Ngân hàng lý thuyết & câu hỏi vấn đáp

> Dùng để ôn trước buổi bảo vệ (~15 phút trình bày + Q&A). **Giảng viên quyết định ai trình bày phần nào**, nên mỗi người ôn **toàn bộ**, không chỉ phần mình.
> Mọi con số dưới đây lấy từ output notebook đã chạy với môi trường ghim (`python=3.11`, `scikit-learn 1.8.0`). Nếu chạy lại mà số đổi thì đọc số trong notebook, đừng học thuộc số cũ.
> Kiến thức đánh dấu **(mở rộng)** vượt ngoài phần cơ bản của môn (pandas, NumPy, Matplotlib, scikit-learn, thống kê mô tả): nhóm tự tìm hiểu để làm phân tích sâu (D4–D6). Hãy giải thích ở mức trực giác và nói rõ lý do dùng.

**Mục lục:** A. Lý thuyết nền · B. Câu hỏi vấn đáp (B1 tổng quan → B13 câu hỏi bẫy) · C. Kịch bản trình bày 15 phút & checklist

---

## A. Lý thuyết nền

### A1. Quy trình của đề
Thu thập dữ liệu (nguồn, giấy phép, cách thu thập) → Khám phá dữ liệu (thường xen với tiền xử lý) → Đặt câu hỏi có ý nghĩa (≥ số thành viên, nêu lợi ích, không quá dễ) → Tiền xử lý + phân tích để trả lời từng câu (mô tả bằng chữ + code rõ ràng) → Reflection (mỗi người: khó khăn, học được gì; cả nhóm: có thêm thời gian sẽ làm gì) → Tài liệu tham khảo. Ngoài ra: dùng Git/GitHub, chia việc cân bằng, mọi người hiểu phần của nhau.

### A2. pandas & NumPy dùng trong dự án
| Thao tác | Dùng để | Ví dụ trong dự án |
| --- | --- | --- |
| `pd.read_csv`, `df.shape`, `df.dtypes`, `df.head()` | Đọc và xem dữ liệu | Phase 1 mục 2.1–2.5 |
| `df.isna().sum()/mean()` | Đếm/tỷ lệ ô thiếu | `missing_table` |
| `df.duplicated()` / `keep=False` | Bản sao thừa / mọi dòng trong nhóm trùng | 74 bản sao, 148 dòng liên quan |
| `value_counts(normalize=True)` | Phân phối một cột | `top_values` ở 2.7 |
| `groupby(...).agg(...)` | Thống kê theo nhóm | `rate_table`, `contrasts` |
| `pivot_table` / `melt` | Đổi bảng dài ↔ rộng (D2) | `pivot_expiration` (Q2) |
| `pd.crosstab` | Đếm/tỷ lệ chéo 2 biến | `time × destination`, cơ cấu coupon lúc 10AM |
| `pd.Categorical(..., ordered=True)` | Biến phân loại có thứ tự | `TIME_ORDER`, `AGE_ORDER`, … |
| `map(dict)`, `isin`, `assign`, `np.where` | Tạo biến mới (D3) | `matched_frequency`, `frequent_user`, gộp tuổi/thu nhập |
| `concat`, `merge` | Ghép bảng | Gộp bảng contrasts, bảng biến thể D6 |
| `copy()` | Không sửa dữ liệu gốc | Mọi hàm trong `src` |
| `np.random.default_rng(seed)` | Sinh số ngẫu nhiên tái lập được | bootstrap |
| `np.percentile` | Phân vị (CI percentile) | mọi CI bootstrap |

### A3. Thống kê
- **Tỷ lệ chấp nhận** = trung bình của `Y` (0/1) × 100%. **Điểm phần trăm (pp)**: hiệu hai tỷ lệ (61,42% − 42,89% = 18,53 pp), khác với "% tăng tương đối".
- **Khoảng tin cậy 95% (CI)**: khoảng giá trị hợp lý của đại lượng thật với độ tin cậy 95% theo cách xây dựng; CI của **chênh lệch** chứa 0 nghĩa là chưa phân biệt được với "không khác nhau".
- **Wilson CI** (mở rộng): CI cho một tỷ lệ, luôn nằm trong [0; 100%] và đáng tin hơn công thức Wald `p ± 1,96·√(p(1−p)/n)` khi `n` nhỏ hoặc `p` gần 0/1.
- **Bootstrap percentile**: rút lại mẫu có hoàn lại nhiều lần, tính lại đại lượng, lấy phân vị 2,5% và 97,5%. Với biến 0/1, rút lại dòng tương đương rút `Binomial(n, p̂)`.
- **Bootstrap theo người / theo cụm** (mở rộng): khi một người có nhiều dòng (không độc lập), phải rút lại **người**; rút theo dòng cho CI hẹp giả tạo.
- **Biến nhiễu (confounder)**: biến liên quan đến cả nhóm so sánh lẫn kết quả, ví dụ `destination` liên quan đến `direction_same` và `Y`. **Phân tầng**: so sánh bên trong từng mức của biến nhiễu.
- **Nghịch lý Simpson**: chiều chênh lệch ở bảng gộp ngược với chiều trong từng tầng vì cơ cấu các nhóm khác nhau (Q2 lúc 10AM).
- **Chuẩn hóa trực tiếp** (mở rộng): tính lại tỷ lệ mỗi nhóm như thể nhóm đó có cùng cơ cấu tầng với toàn mẫu, rồi mới so sánh (Q5). **Trung bình có trọng số các tầng** (Q4): lấy trung bình các chênh lệch trong tầng theo trọng số số mẫu.
- **Common support**: chỉ so sánh trong vùng dữ liệu mà cả hai nhóm đều có đủ mẫu; tầng thiếu hẳn một nhóm thì không có thông tin so sánh.
- **Độ bền (robustness / sensitivity)**: đổi một lựa chọn hợp lý (ngưỡng, cách xử lý thiếu, cách gộp nhóm, bỏ dòng trùng, đơn vị bootstrap) xem kết luận có đổi không (D6).
- **Liên hệ ≠ nhân quả**: dữ liệu khảo sát quan sát được, không phải thí nghiệm ngẫu nhiên.
- **So sánh nhiều lần** (mở rộng): làm rất nhiều phép so sánh thì sẽ có vài kết quả "có ý nghĩa" do ngẫu nhiên; nhóm chưa hiệu chỉnh điều này (đã ghi ở hạn chế).

### A4. Machine Learning
- **Phân loại nhị phân có giám sát**: học `P(Y = 1 | X)` từ dữ liệu có nhãn.
- **Train/test split**: test chỉ dùng **một lần** để đánh giá mô hình đã chốt. **Cross-validation (CV)**: chia train thành k fold để chọn siêu tham số. `StratifiedKFold`: giữ tỷ lệ lớp mỗi fold; `GroupKFold`/`StratifiedGroupKFold`: một nhóm (người) chỉ nằm trong một fold.
- **Data leakage (rò rỉ dữ liệu)**: thông tin của dữ liệu đánh giá lọt vào lúc huấn luyện. Các dạng: dùng cột chỉ có sau thời điểm dự đoán; fit tiền xử lý trên toàn bộ dữ liệu; cùng một người ở cả train và test.
- **`Pipeline` / `ColumnTransformer`**: gói tiền xử lý + mô hình thành một đối tượng; khi `fit` chỉ học từ dữ liệu train của lần đó. `SimpleImputer` điền thiếu; `OneHotEncoder` mã hóa phân loại thành cột 0/1 (`handle_unknown="ignore"`: mức lạ thành toàn 0).
- **`GridSearchCV`**: thử mọi tổ hợp siêu tham số bằng CV, chọn tổ hợp tốt nhất theo metric `refit`, rồi fit lại trên toàn train. Tham số của bước trong Pipeline viết `tên_bước__tham_số` (`model__C`).
- **Baseline**: `DummyClassifier(strategy="most_frequent")` luôn đoán lớp phổ biến; mô hình thật phải vượt nó.
- **Logistic Regression**: mô hình tuyến tính, đầu ra qua hàm sigmoid thành xác suất; `C` là nghịch đảo độ mạnh điều chuẩn L2 (`C` nhỏ thì phạt mạnh, hệ số co về 0, chống overfit).
- **Random Forest**: nhiều cây quyết định, mỗi cây học trên một mẫu bootstrap của dòng và mỗi lần tách chỉ xét một phần đặc trưng (`max_features`); dự đoán là trung bình các cây. `max_depth` giới hạn độ sâu; `min_samples_leaf` là số mẫu tối thiểu ở lá. Học được quan hệ phi tuyến và tương tác.
- **Metric**: accuracy; precision = TP/(TP+FP); recall (TPR) = TP/(TP+FN); F1 = trung bình điều hòa của precision và recall; **balanced accuracy** = (TPR + TNR)/2; **ROC-AUC** = xác suất mô hình cho một dòng "nhận" điểm cao hơn một dòng "từ chối" chọn ngẫu nhiên (0,5 = đoán mò, 1 = hoàn hảo), không phụ thuộc ngưỡng.
- **Confusion matrix** `[[TN, FP], [FN, TP]]`; **FPR** = FP/(FP+TN); **FNR** = FN/(FN+TP); **ngưỡng** mặc định 0,5.
- **Permutation importance**: xáo trộn một cột rồi xem metric giảm bao nhiêu; đo mức mô hình *phụ thuộc* vào cột, không phải nhân quả.
- **Overfitting**: học thuộc nhiễu của train nên kém trên dữ liệu mới. Dấu hiệu: điểm train/CV cao hơn hẳn điểm test.

### A5. Trực quan hóa & tái lập
- Chọn biểu đồ theo câu hỏi: cột nhóm + thanh CI để so sánh tỷ lệ; heatmap kèm `n` cho bảng chéo hai chiều; forest plot (điểm + CI) cho chênh lệch. Luôn có tiêu đề, nhãn trục, đơn vị (`%`, `pp`) và `n`; đánh dấu ô ít mẫu.
- Tái lập: seed cố định, môi trường ghim phiên bản, chạy lại từ đầu bằng một lệnh (`run_all.py`), kiểm thử tự động, không sửa dữ liệu gốc (so SHA-256).

---

## B. Câu hỏi vấn đáp (kèm đáp án gợi ý)

### B1. Tổng quan & yêu cầu của đề
1. **Nhóm làm gì trong đồ án này?** — Phân tích dữ liệu khảo sát UCI #603 về ý định nhận coupon khi lái xe: 5 câu hỏi thống kê (Q1–Q5) và 1 câu Machine Learning (Q6), theo quy trình thu thập → khám phá → đặt câu hỏi → tiền xử lý/phân tích → reflection.
2. **Vì sao 6 câu hỏi?** — Đề yêu cầu ít nhất bằng số thành viên (3); nhóm đặt 2 câu/người, trong đó có 1 câu ML.
3. **Câu hỏi "có ý nghĩa và không quá dễ" thể hiện ở đâu?** — Mỗi câu có người hưởng lợi/quyết định cụ thể (bảng đầu notebook 02) và cần nhiều bước: tạo biến, phân tầng, chuẩn hóa, CI, kiểm tra độ bền; không trả lời được bằng một dòng `groupby`.
4. **D1–D6 là gì, nhóm dùng những tiêu chí nào?** — D1 ghép bảng; D2 pivot/melt/so sánh theo thời kỳ; D3 tạo biến mới có cơ sở; D4 kiểm soát biến nhiễu; D5 định lượng bất định; D6 kiểm tra độ bền. Nhóm dùng D2–D6 (5/6); mỗi câu non-ML có ≥ 2 tiêu chí.
5. **Kết luận quan trọng nhất của cả đồ án?** — Loại coupon và thói quen ghé quán liên hệ mạnh hơn nhiều so với nhân khẩu học; so sánh gộp thô dễ sai vì bối cảnh khảo sát dính chặt với nhau; mô hình ML hữu ích để xếp hạng (ROC-AUC 0,781 trên người mới).
6. **Phát hiện bất ngờ nhất?** — Nghịch lý Simpson lúc 10AM: bảng gộp cho `2h` hơn `1d` (−2,01 pp) nhưng trong từng loại coupon thì cả 5/5 đều có ước lượng `1d > 2h`; và thu nhập ≥100k vẫn nhận 57,8%, không thấp hơn trung bình.

### B2. Dữ liệu & thu thập
7. **Nguồn, giấy phép?** — UCI ML Repository #603, DOI 10.24432/C5GS4P, CC BY 4.0 (được dùng/sửa/chia sẻ, kể cả học thuật, nếu ghi nguồn).
8. **Tác giả thu thập thế nào?** — Khảo sát trên Amazon Mechanical Turk: mô tả tình huống lái xe giả định rồi hỏi người trả lời có nhận coupon nếu họ là tài xế không (bài báo Wang et al., 2017, JMLR).
9. **Một dòng là gì?** — Câu trả lời của một người cho một tình huống; không phải một người (567 người suy ra, phần lớn 22 dòng/người).
10. **`Y = 1` có phải đã dùng coupon không?** — Không, chỉ là ý định tự khai trong tình huống giả định.
11. **Hạn chế lớn nhất của dữ liệu?** — Không có mã người trả lời; dữ liệu là ý định giả định; người trả lời MTurk không đại diện mọi tài xế; tổ hợp bối cảnh do người thiết kế khảo sát chọn (ô rỗng).
12. **Vì sao chọn dữ liệu này?** — Thật, công khai, giấy phép rõ; 12.684 × 26 đủ lớn; có đủ loại biến để đặt câu hỏi thực tế và làm cả thống kê lẫn ML.
13. **Các phân tích công khai khác làm gì, nhóm khác ở đâu?** — Bài báo gốc đề xuất thuật toán rule-set; các repo công khai chủ yếu là EDA mô tả hoặc ML chia theo dòng. Nhóm thêm phân tầng/chuẩn hóa, CI, kiểm tra độ bền và chia dữ liệu theo người (`docs/related_work.md`).

### B3. Khám phá & tiền xử lý (Phase 1)
14. **Dữ liệu thiếu ở đâu, xử lý ra sao?** — `car` thiếu 99,15% → không dùng làm biến; 5 cột thói quen thiếu 0,84–1,71% → không `dropna` toàn bảng, không đổi thành `never`; mô tả thì gom vào "Unknown", so sánh thì dùng complete-case kèm phương án điền mode để kiểm tra độ nhạy; ML thì dùng `SimpleImputer` trong Pipeline.
15. **Vì sao không điền NaN thành `never`?** — Thiếu không có nghĩa là "không bao giờ"; điền bừa làm sai phân phối thói quen và kết luận Q3/Q5.
16. **Dòng trùng xử lý thế nào?** — 74 bản sao thừa (0,58%), mỗi nhóm trùng 2 dòng giống hệt. Không có mã người nên không biết là lỗi hay câu trả lời hợp lệ → giữ, và kiểm tra độ nhạy khi bỏ (Q1: +18,53 → +19,41 pp; Q3: đổi tối đa 0,29 pp).
17. **Cột nào có kiểu chưa phù hợp?** — `age`, `income`, `time`, `expiration` và 5 cột thói quen là phân loại có thứ tự nhưng lưu dạng chuỗi (sắp chuỗi sai: `"10AM"` < `"7AM"`) → dùng `pd.Categorical(ordered=True)`; không ép `age`/`income` sang số vì là mã nhóm; `temperature` chỉ có 3 mức nên coi như phân loại.
18. **Có giá trị bất thường không?** — Cột số đều hợp lệ (0 vi phạm logic); `toCoupon_GEQ5min` là hằng số; `direction_opp` trùng thông tin; `car` có giá trị lạ (`do not drive`, `Car that is too old to install Onstar :D`); UCI ghi "không thiếu dữ liệu" nhưng CSV thực tế có thiếu.
19. **Quan hệ sơ bộ nào ảnh hưởng mạnh đến phân tích sau?** — `7AM` ⇔ `Work`; `10AM`, `2PM` chỉ có `No Urgent Place`; `Friend(s)` chỉ đi `No Urgent Place`; `Rainy` luôn 55°F, `Snowy` luôn 30°F → phải phân tầng khi so sánh.
20. **`matched_frequency` là gì?** — Tần suất ghé đúng loại địa điểm của coupon trong dòng đó (coupon `Bar` lấy cột `Bar`, …); thiếu 164 dòng (1,29%).
21. **Wilson CI của tỷ lệ chung?** — 56,84% (7.210/12.684), CI [55,98%; 57,70%].

### B4. Q1 — Khoảng cách & hướng (Dương)
22. **`travel_time_band` tạo thế nào, vì sao là D3?** — Từ 2 cờ: `GEQ15 = 0` → `5-<15`, `GEQ15 = 1 & GEQ25 = 0` → `15-<25`, `GEQ25 = 1` → `>=25`. Là biến mới có cơ sở từ cột gốc, dễ đọc hơn 2 cờ rời.
23. **Kết quả chính?** — 61,42% → 56,07% → 42,89%; gần − xa +18,53 pp, CI [15,69; 21,38].
24. **Phân tầng làm thay đổi gì?** — Chiều giữ nguyên trong `Home` (+16,05) và `Work` (+20,16); khác nhau rất mạnh theo coupon: `Restaurant(<20)` giảm 42,74 pp, `Carry out` gần như không đổi (+2,05, CI chứa 0).
25. **Vì sao hướng đi gộp thô chỉ +1,76 pp mà trong `Home` lên +17,40 pp?** — `No Urgent Place` (tỷ lệ nhận cao) luôn có `direction_same = 0`, làm nhóm "ngược hướng" được kéo lên; cố định điểm đến thì hiệu ứng thật lộ ra. Đây là biến nhiễu che khuất.
26. **`no_common_support` nghĩa là gì?** — Tầng thiếu hẳn một nhóm (ví dụ `No Urgent Place` không có `>=25 min`), không thể so sánh nên không tính chênh lệch.
27. **Q1 có cần CI theo người không?** — Đã kiểm tra ở Phase 2.4: gần − xa có CI theo người [15,4; 21,5], gần như bằng CI theo dòng, vì mỗi người đều gặp cả tình huống gần và xa (so sánh bên trong người).
28. **Ứng dụng?** — Nhà hàng/cà phê nên gợi ý quán dưới 25 phút, cùng hướng; đồ mang đi có thể nới bán kính (cần A/B test).

### B5. Q2 — Thời hạn 2h vs 1d (Dương)
29. **D2 thể hiện ở đâu?** — `pivot_table` (hàng `time`, cột `expiration`, giá trị tỷ lệ và `n`) rồi `melt` sang bảng dài để vẽ (`pivot_expiration`). `time` chỉ là giờ trong ngày, không phải chuỗi thời gian.
30. **Kết quả chính?** — `1d` 62,56% vs `2h` 49,60%: +12,96 pp [11,27; 14,70]; lớn nhất lúc 10PM (+26,13) và 7AM (+20,78).
31. **Giải thích nghịch lý lúc 10AM?** — Gộp thô −2,01 pp, nhưng trong từng coupon cả 5/5 có ước lượng `1d > 2h` (4/5 có CI không chứa 0). Lý do: nhóm `1d` lúc 10AM có 36,1% coupon `Bar` (ít được nhận) so với 5,4% ở nhóm `2h`, nên bảng gộp bị kéo xuống.
32. **Có nên phát `2h` cho Bar buổi tối?** — Không có bằng chứng: lúc 10PM −8,87 pp nhưng CI [−18,37; 0,14] chứa 0, còn lúc 6PM lại ngược chiều (+12,82, CI [4,32; 21,28]). Với Bar, thời hạn hầu như không tạo khác biệt (+0,85 pp, CI chứa 0).
33. **Hạn chế?** — Bar không có `2h` lúc 7AM, 2PM; `time` dính với `destination`; CI theo dòng (Phase 2.4: CI theo người [10,8; 15,2], kết luận giữ nguyên).

### B6. Q3 — Thói quen (Hà)
34. **"Thường xuyên" định nghĩa thế nào?** — Chính: ≥ 1 lần/tháng (`1~3`, `4~8`, `gt8`); độ nhạy: ≥ 4 lần/tháng.
35. **Kết quả?** — Cả 5/5 coupon nhóm thường ghé cao hơn: Bar +39,58 [35,18; 43,97], Coffee House +31,41 [28,42; 34,38], Restaurant(20-50) +17,15, Carry out +5,80, Restaurant(<20) +5,39.
36. **D6 làm gì?** — 2 ngưỡng × 2 cách xử lý thiếu = 4 biến thể, cộng bỏ trùng: chiều dương giữ nguyên ở 4/4 biến thể, bỏ trùng đổi tối đa 0,29 pp; riêng Carry out với ngưỡng ≥4 thì CI [−0,72; 6,45] chứa 0.
37. **Vì sao kiểm tra lại bằng CI theo người lại làm thay đổi kết luận ở Q3?** — Thói quen là đặc điểm cố định của mỗi người, nên so sánh là *giữa các người*; các dòng của một người cùng nhóm thói quen nên bootstrap theo dòng đánh giá quá cao lượng thông tin. Theo người: Carry out [−0,9; 12,7] và Restaurant(<20) [−1,2; 11,7] chứa 0; ba loại còn lại vẫn rõ.
38. **Điểm bất ngờ?** — Ghé nhiều hơn chưa chắc nhận nhiều hơn: Bar mức `gt8` 73,47% (n=49) không cao hơn `4~8` 78,00% (n=150); CI chồng lấn nên chỉ nói "chững lại".
39. **Vì sao dùng Wilson cho hình nhưng bootstrap cho chênh lệch?** — Wilson cho một tỷ lệ là công thức đóng, nhanh và chính xác; chênh lệch hai tỷ lệ thì dùng bootstrap cho tiện và nhất quán.

### B7. Q4 — Người đồng hành (Hà)
40. **Kết quả thô và sau chuẩn hóa?** — Thô: Friend(s) − Alone +14,76 [12,81; 16,75], Partner − Alone +6,95. Chuẩn hóa `coupon × destination`: +1,33 [−1,70; 4,51] và +3,03 [−1,08; 7,07], cả hai CI chứa 0.
41. **Vì sao chênh lệch biến mất?** — Friend(s) chỉ xuất hiện ở `No Urgent Place` (tỷ lệ nhận cao), không có ở Home/Work. Chỉ 4/15 tầng (41,6% mẫu cặp) đủ common support. Riêng việc thu hẹp về các tầng này đã kéo +14,76 xuống +5,46; cân lại cơ cấu coupon giảm tiếp còn +1,33.
42. **Công thức chuẩn hóa ở Q4?** — Trung bình các chênh lệch trong tầng đủ mẫu, trọng số `w_s = (n_A,s + n_B,s)/Σ(n_A + n_B)`; CI bằng bootstrap trong từng tầng.
43. **"6/12 tầng đổi dấu" nghĩa là gì?** — Trong 12 tầng đủ mẫu của hai cặp, 6 tầng có chênh lệch ngược dấu với mức thô, nhưng chỉ 2 tầng trong số đó có CI không chứa 0, nên phần lớn chưa chắc chắn.
44. **`has_children` có nghĩa trẻ đang trên xe?** — Không, chỉ là người trả lời có con; người đi cùng là `Kid(s)` trong `passanger`.

### B8. Q5 — Tuổi & thu nhập (Lý)
45. **Vì sao gộp tuổi/thu nhập?** — Để mỗi ô coupon × thói quen × nhóm có đủ người; 4 nhóm tuổi (<26, 26–35, 36–50, 50+), 3 nhóm thu nhập (ranh giới 37,5k, 75k USD).
46. **`respondent_id` dựng thế nào, có chính xác không?** — Các dòng có cùng toàn bộ 13 cột hồ sơ + thói quen là một người → 567 ID (489 ID có đúng 22 dòng). Có thể gộp vài người có hồ sơ giống hệt (ID có 44/66/110 dòng); không thấy dấu hiệu tách một người thành hai.
47. **Chuẩn hóa trực tiếp làm gì?** — Tính lại tỷ lệ của mỗi nhóm tuổi như thể nhóm đó có cùng cơ cấu `coupon × thói quen` với toàn mẫu, nên chênh lệch còn lại không còn do khác cơ cấu.
48. **Kết quả?** — Tuổi `<26 − 50+`: thô +9,7 → chuẩn hóa coupon +9,8 → coupon × thói quen +7,5 [2,8; 12,4] (giảm khoảng 23%). Thu nhập `Thấp − Cao`: +4,4 [0,4; 8,4]; giữ cố định tuổi còn +3,8 [−0,6; 7,8], chứa 0.
49. **Vì sao kiểm soát thói quen làm chênh lệch tuổi nhỏ lại?** — Người trẻ ghé bar/cà phê nhiều hơn (đi bar ≥1 lần/tháng: 35,9% ở <26 so với 23,2% ở 50+), nên một phần chênh lệch "theo tuổi" thật ra là chênh lệch theo thói quen.
50. **Vì sao bootstrap theo người?** — Một người trả lời ~22 tình huống; bootstrap theo dòng cho CI hẹp hơn ~1,8 lần (rộng 5,4 so với 9,6 pp), tức tự tin quá mức.
51. **D6 ở Q5?** — Giữ cố định nhóm còn lại; ngưỡng thói quen ≥4 (+9,8; 45/2000 lần rút có ô rỗng); chia đôi tuổi (+3,2, CI chứa 0 → khác biệt nằm ở hai đầu tuổi); chia đôi thu nhập (+2,9, CI chứa 0); bootstrap theo dòng.
52. **`empty_strata_draws` là gì?** — Số lần bootstrap có ô (nhóm × tầng) rỗng nên không tính được tỷ lệ chuẩn hóa; các lần đó bị loại khi lấy phân vị.
53. **"Thu nhập cao ít cần coupon" có đúng không?** — Không, trong khảo sát: ≥100k nhận 57,8% (CI [53,6; 62,1]), không thấp hơn trung bình 56,84%; thấp nhất lại là 75–87,5k (48,3%).

### B9. Q6 — Machine Learning (Lý)
54. **Câu hỏi và lợi ích?** — Các đặc trưng biết trước lúc hiện coupon dự đoán `Y` tốt hơn baseline bao nhiêu khi tách theo người; để hệ thống gợi ý **xếp hạng** ai nên nhận coupon nào.
55. **Prediction time là gì, vì sao 22 cột?** — Chỉ dùng thông tin có trước khi hiện coupon: bối cảnh, coupon/thời hạn (do hệ thống chọn), hồ sơ, thói quen. Loại `Y`, `toCoupon_GEQ5min` (hằng), `direction_opp` (trùng), `car` (thiếu 99,15%).
56. **Thói quen có phải rò rỉ không?** — Không phải rò rỉ nhãn (là thông tin tự khai có trước), nhưng giả định hệ thống đã biết thói quen; người dùng mới (cold-start) sẽ không có.
57. **Vì sao không chia ngẫu nhiên theo dòng?** — Cùng một người sẽ nằm ở cả train và test, mô hình "nhớ" người đó, điểm bị thổi phồng. Kiểm chứng: chia fold CV theo dòng làm RF tăng giả tạo +0,043 (0,810 so với 0,767).
58. **Vì sao không chia theo `time`?** — `time` chỉ là giờ trong ngày của tình huống giả định, không có "tương lai" để mô phỏng.
59. **`GroupShuffleSplit` và `StratifiedGroupKFold` khác gì?** — Cái đầu chia một lần 80/20 theo nhóm (train 453 người, test 114 người); cái sau chia train thành 5 fold, mỗi người trọn trong một fold, tỷ lệ `Y` các fold gần nhau (55,9–56,3%).
60. **Vì sao tiền xử lý trong Pipeline?** — Để imputer/encoder chỉ học từ phần train của mỗi lần fit (từng fold, lần refit cuối) → không rò rỉ sang fold kiểm định hay test.
61. **Vì sao điền `"missing"` thay vì mode?** — Thiếu có thể mang thông tin, giữ thành một mức riêng; hằng số không học từ dữ liệu.
62. **`handle_unknown="ignore"` để làm gì?** — Gặp mức chưa thấy khi fit thì mã hóa toàn 0 thay vì báo lỗi.
63. **Vì sao không chuẩn hóa thang đo cho LR?** — Sau One-Hot mọi đầu vào đều là 0/1, cùng thang đo.
64. **Baseline Dummy cho F1 0,749 mà AUC 0,5?** — Luôn đoán "nhận" nên recall = 1, precision = tỷ lệ `Y=1` của test (0,599): F1 = 2p/(1+p) = 0,749; nhưng không xếp hạng được nên AUC 0,5. Vì vậy chọn ROC-AUC làm metric chính.
65. **Siêu tham số được chọn?** — LR: `C = 0,01`. RF: `max_depth = 20`, `max_features = 0,2`, `min_samples_leaf = 5` (300 cây).
66. **Kết quả CV và test?** — CV ROC-AUC: LR 0,722 ± 0,011; RF 0,767 ± 0,009. Test: RF 0,781 [0,755; 0,807], balanced accuracy 0,706, F1 0,775, accuracy 72,4%; LR 0,726; Dummy 0,500.
67. **Test có bị dùng để chọn mô hình không?** — Không. Chọn bằng CV (`idxmax`); cả 3 mô hình được chấm test một lần chỉ để lập bảng so sánh.
68. **CI của điểm test tính sao?** — Bootstrap theo người của tập test (1.000 lần, trọng số = số lần người được rút). Cùng seed cho mọi mô hình nên CI của hiệu RF − LR (0,055 [0,037; 0,074]) là ghép cặp.
69. **0,781 có phải do may mắn?** — Lặp lại với 50 cách chia theo người (giữ cấu hình): RF 0,774 ± 0,012 (0,752–0,801), luôn hơn LR (50/50). Vậy 0,781 là điển hình, hơi thuận lợi. Tập test bản chính có tỷ lệ `Y = 1` cao (59,9%) nhưng ROC-AUC không phụ thuộc tỷ lệ lớp.
70. **Vì sao RF tốt hơn LR?** — LR chỉ cộng tác động riêng của từng cột; RF học được tương tác, ví dụ "coupon Bar *và* người hay đi bar". Thêm cho LR một cột ghép `coupon × thói quen` nâng CV từ 0,722 lên 0,748, thu hẹp gần 60% khoảng cách tới RF (0,767).
71. **Lỗi tập trung ở đâu?** — 705 lỗi (391 FP, 314 FN). Coupon phổ biến bị đoán nhận quá tay (Carry out FPR 90,5%); coupon ít phổ biến bị bỏ sót (Bar FNR 51,9%). Mô hình tốt ở hai đầu xác suất (p > 0,7: 84,6% nhận; p ≤ 0,3: 19,0%), kém ở vùng 0,3–0,6 (đúng 52–59%).
72. **Ngưỡng 0,5 có hợp lý?** — Là mặc định; nên chọn ngưỡng theo chi phí FP (làm phiền) và FN (bỏ lỡ), trên dữ liệu train/CV, không chọn trên test. Mô hình phù hợp để xếp hạng hơn là cắt cứng.
73. **Permutation importance cho biết gì?** — `coupon` (0,1573), `CoffeeHouse` (0,0569), `expiration` (0,0495), `Bar` (0,0168), `destination` (0,0148); nhân khẩu học gần 0. Chỉ cho biết mô hình dựa vào cột nào, không phải nhân quả; tính trên test sau khi đã chốt mô hình nên không ảnh hưởng việc chọn.
74. **Vì sao permutation importance xáo cột gốc chứ không xáo cột One-Hot?** — Xáo trước Pipeline nên cả một biến phân loại được đánh giá như một đơn vị.
75. **Kết quả phụ thuộc phiên bản thư viện?** — Có, ở chữ số thứ 3: scikit-learn ≤ 1.7 chia fold `StratifiedGroupKFold(shuffle=True)` khác. Nhóm ghim 1.8.0 và chạy lại toàn bộ.
76. **Nếu có thêm thời gian?** — Chia test có phân tầng theo nhóm, nested CV, thêm tương tác cho LR hoặc gradient boosting, hiệu chỉnh xác suất, chọn ngưỡng theo chi phí, đánh giá kịch bản cold-start.

### B10. Code trong `src/` & notebook
77. **Vì sao gom logic vào `src/coupon_project`?** — Viết một lần, dùng cho mọi câu; kiểm thử được bằng pytest; notebook gọn và nhất quán.
78. **`rng_for(key)` để làm gì?** — Sinh seed riêng từ tên phép so sánh: chạy lại ra đúng số, thêm/bớt một phép so sánh không làm đổi CI của phép khác. `_plain` đổi số numpy sang số Python để seed giống nhau trên mọi phiên bản.
79. **`contrasts` trả về gì?** — Mỗi tầng một dòng: `n_a`, `n_b`, tỷ lệ, `diff_pp`, CI, `small_n`, `status`.
80. **Giải thích `_cluster_bootstrap` trong 4 câu.** — Gán dòng vào ô (nhóm, tầng); tỷ lệ mỗi ô tính có trọng số; tỷ lệ chuẩn hóa = trung bình tỷ lệ các ô theo tỷ trọng tầng của toàn mẫu; bootstrap rút lại người, người được rút k lần thì dòng của họ có trọng số k, lặp 2.000 lần rồi lấy phân vị.
81. **Vì sao `save_table` không được là dòng cuối cell?** — Hàm trả về đường dẫn; Jupyter sẽ in đường dẫn máy ra output (đã từng lộ đường dẫn thư mục tạm).
82. **`observed=False` trong `pivot_table` để làm gì?** — Giữ đủ mọi mức của biến Categorical (đủ 5 khung giờ) dù có ô không có dữ liệu.
83. **Vì sao `assert` trong notebook?** — Kiểm tra giả định ngay khi chạy (không trùng người giữa train/test, không vi phạm logic cờ, file gốc không bị sửa): sai là dừng ngay.
84. **`df.groupby(...).ngroup()` làm gì?** — Gán số thứ tự nhóm cho từng dòng; dùng để dựng `respondent_id`.
85. **`GridSearchCV(scoring=[...], refit="roc_auc")`?** — Tính 4 metric cho mỗi cấu hình nhưng chọn cấu hình và fit lại theo ROC-AUC.
86. **`gs.predict_proba(X_test)[:, 1]`?** — Xác suất lớp 1 (nhận) cho từng dòng; `predict` tương đương ngưỡng 0,5.
87. **`cm / cm.sum(axis=1, keepdims=True)`?** — Chuẩn hóa ma trận nhầm lẫn theo từng lớp thật (mỗi hàng cộng lại 100%).

### B11. Tái lập, Git, AI
88. **Làm sao chắc người khác chạy lại ra cùng số?** — Ghim phiên bản (`environment.yml`, `requirements.txt`), seed cố định, `run_all.py` chạy lại từ đầu, kiểm tra SHA-256 của CSV, 44 test tự động.
89. **Chia việc thế nào, Git ra sao?** — Mỗi người 2 câu và một phần module; mỗi người một nhánh, tích hợp rồi merge vào `main`; kế hoạch theo giai đoạn (link Google Sheets trong README).
90. **Dùng AI thế nào?** — Như gia sư/người rà soát: giải thích khái niệm, gợi ý cách kiểm tra, rà lỗi; mọi số liệu lấy từ output chạy thật; ghi đầy đủ trong `LLM_USAGE.md`; mỗi người tự giải thích được code và tự viết reflection.

### B12. Câu hỏi đọc code nhanh (giảng viên chỉ vào một dòng)
91. `q1_df = add_travel_time_band(df)` — tạo bản sao có cột `travel_time_band`, `df` gốc không đổi.
92. `contrasts(q1_df, ["coupon"], "travel_time_band", NEAR, FAR, key="q1_coupon")` — trong từng loại coupon, tính tỷ lệ gần − xa và CI.
93. `pd.crosstab(at_10am["coupon"], at_10am["expiration"], normalize="columns")` — trong mỗi nhóm thời hạn lúc 10AM, mỗi loại coupon chiếm bao nhiêu %.
94. `work["matched_frequency"].fillna(modes)` — điền ô thiếu bằng mức phổ biến nhất của cùng coupon (phương án độ nhạy).
95. `standardized_contrast(strata_table, n_boot=10000, seed=17104, key=...)` — trung bình có trọng số các chênh lệch tầng đủ mẫu, kèm CI.
96. `q5.dropna(subset=["matched_frequency"])` — bỏ 164 dòng thiếu thói quen chỉ cho phép so sánh có kiểm soát thói quen.
97. `cluster_diff_ci(q5_cc, "age_group", "<26", "50+", ("coupon", "frequent_user"))` — chênh tuổi đã chuẩn hóa theo coupon × thói quen, CI theo người.
98. `GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42).split(X, y, groups=respondent_id)` — chia 20% số người làm test.
99. `permutation_importance(selected_model, X_test, y_test, scoring="roc_auc", n_repeats=10)` — xáo mỗi cột 10 lần, đo ROC-AUC giảm.
100. `clone(searches[name].best_estimator_).fit(...)` — tạo mô hình mới cùng cấu hình (chưa huấn luyện) để fit lại trên cách chia khác.

### B13. Câu hỏi "bẫy"
101. **"Vậy đi gần thì làm người ta nhận coupon nhiều hơn?"** — Không nói được "làm cho": dữ liệu quan sát. Chỉ nói "trong khảo sát, tình huống gần đi kèm tỷ lệ nhận cao hơn".
102. **"CI 95% nghĩa là 95% khả năng giá trị thật nằm trong khoảng này?"** — Cách nói chính xác hơn: nếu lặp lại quy trình nhiều lần thì khoảng 95% các khoảng dựng được sẽ chứa giá trị thật.
103. **"Sao không dùng p-value?"** — CI cho cả độ lớn lẫn độ chắc chắn; CI của chênh lệch không chứa 0 tương ứng với kiểm định ở mức 5%.
104. **"Q1–Q4 dùng bootstrap theo dòng, vậy có sai không?"** — Đã kiểm tra lại bằng CI theo người ở Phase 2.4: Q1, Q2, Q4 giữ nguyên kết luận; Q3 thì Carry out và Restaurant(<20) không còn chắc chắn — đã ghi rõ.
105. **"Accuracy 72,4% có cao không?"** — Phải so với baseline 59,9%; metric chính là ROC-AUC 0,781 so với 0,5.
106. **"Test cao hơn CV, có phải overfit?"** — Overfit thì test thấp hơn; ở đây test cao hơn chút do ngẫu nhiên của 114 người; qua 50 cách chia trung bình 0,774.
107. **"Có thể dùng mô hình này ngay ngoài thực tế?"** — Chưa: dữ liệu là ý định giả định trên MTurk; cần thử nghiệm A/B với hành vi thật.
108. **"Ai làm phần này? Giải thích dòng này."** — Mỗi người phải trả lời được mọi phần (đọc mục B12 và `HUONG_DAN_HE_THONG.md`).

---

## C. Kịch bản trình bày ~15 phút (có thể trình bày trực tiếp trên notebook)
| Phút | Nội dung | Mở ở đâu |
| --- | --- | --- |
| 0–2 | Bài toán, dữ liệu (nguồn, license, cách thu thập), 3 điểm EDA quan trọng (thiếu dữ liệu, dòng trùng, cấu trúc `7AM ⇔ Work`, `Friend(s)` chỉ ở `No Urgent Place`) | `01` mục 1, 2.8, 2.10 |
| 2–4 | Danh sách 6 câu hỏi + lợi ích; quy ước %/pp/CI | `02` đầu notebook |
| 4–6 | Q1 + Q2 (kết quả chính, biến nhiễu `destination`, nghịch lý Simpson lúc 10AM) | `02` Phase 2.1 |
| 6–8 | Q3 + Q4 (thói quen; chênh lệch Friend(s) biến mất sau chuẩn hóa) | `02` Phase 2.2 |
| 8–10 | Q5 (chuẩn hóa trực tiếp, bootstrap theo người) + bảng kiểm tra CI theo người | `02` Phase 2.3, 2.4 |
| 10–13 | Q6 (prediction time, chia theo người, Pipeline, CV, test 1 lần, bảng kết quả, lỗi, importance, độ ổn định) | `03` |
| 13–15 | Kết luận chung, hạn chế, hướng phát triển, reflection | `02` Phase 2.4 |

Mẹo: nói ý tưởng, ít đọc code; mỗi kết luận nêu **một con số kèm CI** và **một câu hạn chế**.

### Checklist trước buổi bảo vệ
- [ ] Mỗi người đọc hết `HUONG_DAN_HE_THONG.md` và tự trả lời được mục B mà không nhìn đáp án.
- [ ] Chạy `python scripts/run_all.py` trên máy mình, mở 3 notebook đã chạy sẵn output.
- [ ] Reflection của từng người đã tự viết xong; `LLM_USAGE.md` đã cập nhật.
- [ ] Link Google Sheets/Trello kế hoạch đã có trong README; nhánh cuối đã merge vào `main`.
