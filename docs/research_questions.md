# 🎯 Đề xuất 6 câu hỏi nghiên cứu – CSC17104

> Đây là **kế hoạch nghiên cứu**, không phải kết luận. Nhóm tự xác minh số lượng nhóm, làm sạch dữ liệu, triển khai code, đánh giá và viết câu trả lời từ số liệu thật. Tất cả các câu phải có motivation, ≥2 biểu đồ và hạn chế.

## Ma trận tiêu chí D1–D6

| Câu | Owner | D1 | D2 | D3 | D4 | D5 | D6 |
| --- | --- | :--: | :--: | :--: | :--: | :--: | :--: |
| Q1 | Dương |  |  | ✓ | ✓ | ✓ |  |
| Q2 | Dương |  | ✓ |  | ✓ | ✓ |  |
| Q3 | Hà |  |  | ✓ | ✓ | ✓ | ✓ |
| Q4 | Hà |  |  |  | ✓ | ✓ |  |
| Q5 | Lý |  |  |  | ✓ | ✓ | ✓ |
| **Q6** | **Lý** |  |  |  |  |  | **ML riêng** |

**Bao phủ D2, D3, D4, D5, D6**; đề yêu cầu ≥4/6. Phải kiểm chứng từng tiêu chí trong notebook. Một câu không thể đạt D5 chỉ bằng cách gắn nhãn mà không triển khai CI/test/effect size.

---

## Q1 · Dương – Sự thuận tiện di chuyển

**Câu hỏi:** Mối liên hệ giữa khoảng cách và hướng đi đến địa điểm sử dụng coupon với xác suất chấp nhận có giữ nguyên khi xét mục đích chuyến đi và loại coupon không?

- **Motivation:** Hiểu khi nào coupon phù hợp hành trình; hữu ích khi cân nhắc cách gửi ưu đãi theo ngữ cảnh.
- **Cột:** `toCoupon_GEQ15min`, `toCoupon_GEQ25min`, `direction_same`, `destination`, `coupon`, `Y` (kiểm tra thêm `toCoupon_GEQ5min`).
- **D3:** Tạo `travel_time_band` (ví dụ nhóm 0–<15, 15–<25, ≥25 phút **theo cờ giá trị thực tế**); ghi lại quy tắc và kiểm tra tính hợp lệ của các cờ.
- **D4:** So sánh trong từng `destination` và `coupon`; cân nhắc nhóm quá ít mẫu.
- **D5:** Khoảng tin cậy cho tỷ lệ/chênh lệch tỷ lệ, hoặc bootstrap đúng đơn vị quan sát; trình bày mẫu từng nhóm.
- **Chart 1:** Heatmap tỷ lệ `Y=1` theo `travel_time_band` × `direction_same`.
- **Chart 2:** Grouped bar theo `destination`/loại coupon, kèm CI khi phù hợp.
- **Hạn chế cần thảo luận:** Các biến thời gian là ngưỡng chứ không phải phút chính xác; dữ liệu quan sát khảo sát, thiếu participant ID.

## Q2 · Dương – Thời hạn coupon & thời điểm trong ngày

**Câu hỏi:** Mối liên hệ giữa hạn coupon `2h` và `1d` với tỷ lệ chấp nhận thay đổi thế nào theo thời điểm trong ngày và loại coupon?

- **Motivation:** Xem tính hấp dẫn của coupon ngắn hạn có khác khi người lái đang ở các thời điểm khác nhau không.
- **Cột:** `expiration`, `time`, `coupon`, `destination`, `Y`.
- **D2:** Dùng `pivot_table` thể hiện các tỷ lệ ở giao điểm `time` × `expiration`, và/hoặc `melt` để so sánh tình huống. Không gọi đây là xu hướng theo *ngày*.
- **D4:** Giữ loại coupon giống nhau khi so sánh; nếu đủ mẫu, xét thêm `destination`.
- **D5:** Bootstrap CI của chênh lệch `1d` – `2h`, tránh chỉ so sánh 2 tỷ lệ trần.
- **Chart 1:** Grouped bar theo giờ và expiration.
- **Chart 2:** Heatmap chênh lệch tỷ lệ theo time × coupon.
- **Hạn chế:** `time` là thời điểm trong ngày ở một kịch bản giả định, không có chuỗi ngày tháng để phân tích trend thực.

## Q3 · Hà – Thói quen tiêu dùng và coupon phù hợp

**Câu hỏi:** Trong cùng một loại coupon, người có thói quen thường xuyên đến địa điểm tương ứng có tỷ lệ chấp nhận cao hơn không?

- **Motivation:** Kiểm tra liệu sự phù hợp giữa ưu đãi và thói quen có đáng kể với ý định nhận coupon không.
- **Cột:** `coupon`, `Bar`, `CoffeeHouse`, `CarryAway`, `RestaurantLessThan20`, `Restaurant20To50`, `Y`.
- **D3:** Tạo `matched_visit_frequency` cho từng loại coupon; lập mapping bằng các **nhãn coupon trong CSV thực tế**.
- **D4:** So sánh trong từng loại coupon, không gộp các coupon có độ phổ biến khác nhau mà không kiểm soát.
- **D5:** CI/effect size cho mức thường xuyên và ít thường xuyên.
- **D6:** Kiểm tra độ bền với ngưỡng thường xuyên (≥1–3 lần, ≥4–8 lần/tháng) và cách xử lý NaN.
- **Chart 1:** Tỷ lệ chấp nhận theo cấp tần suất trong từng loại coupon.
- **Chart 2:** Heatmap các loại coupon × cấp tần suất, có thể bổ sung số mẫu.
- **Hạn chế:** Tần suất tự báo cáo, các nhóm nhỏ và biến thiếu.

## Q4 · Hà – Vai trò của người đi cùng

**Câu hỏi:** Người đi cùng liên quan đến việc chấp nhận coupon như thế nào, sau khi so sánh các tình huống có cùng mục đích và loại coupon?

- **Motivation:** Coupon có thể phù hợp khác nhau khi lái xe một mình, với bạn bè, người yêu/bạn đời hoặc trẻ em.
- **Cột:** `passanger`, `destination`, `coupon`, `has_children`, `Y`.
- **D4:** Phân tầng theo `destination` và `coupon`, thảo luận việc `has_children` có nên kiểm soát thêm không.
- **D5:** CI cho các tỷ lệ theo nhóm và effect size/chênh lệch khi so sánh các nhóm liên quan.
- **Chart 1:** Grouped bar tỷ lệ chấp nhận theo `passanger` × `coupon`.
- **Chart 2:** Heatmap `passanger` × `destination` trong các loại coupon đủ dữ liệu.
- **Hạn chế:** Có thể xuất hiện nhóm nhỏ, không suy ra ảnh hưởng nhân quả từ người đồng hành.

## Q5 · Lý – Thu nhập và nhóm tuổi

**Câu hỏi:** Liên hệ giữa tuổi, khoảng thu nhập và tỷ lệ chấp nhận theo loại coupon có còn tồn tại khi kiểm soát thói quen đến các địa điểm tương ứng?

- **Motivation:** Phân tích sự khác biệt nhóm khách hàng và tránh so sánh demographic mà bỏ qua sở thích sẵn có.
- **Cột:** `age`, `income`, `coupon`, 5 cột thói quen tương ứng, `Y`.
- **D4:** So sánh trong cùng loại coupon; nếu có thể, phân tầng theo thói quen phù hợp và cân nhắc nhóm mẫu rất nhỏ.
- **D5:** CI chênh lệch/hiệu ứng; tránh đọc heatmap khi không có số mẫu.
- **D6:** Kiểm tra kết quả khi đổi cách gộp nhóm tuổi/thu nhập.
- **Chart 1:** Heatmap thu nhập × coupon (có n cho từng ô).
- **Chart 2:** Grouped bar theo nhóm tuổi với CI và/hoặc các nhóm thói quen.
- **Hạn chế:** `age` chứa `below21`, `50plus`; `income` là **khoảng thu nhập**, không phải số liên tục.

## Q6 · Lý – Machine Learning dự đoán `Y`

**Câu hỏi:** Có thể dự đoán **ý định** chấp nhận coupon bằng những thông tin có sẵn tại thời điểm coupon được đưa ra không? Mô hình nào tốt hơn baseline trên tập dữ liệu giữ lại?

- **Motivation & đối tượng sử dụng:** Mô hình minh họa hỗ trợ xác định bối cảnh phù hợp để giới thiệu coupon. Không khẳng định khả năng triển khai thương mại chỉ từ dữ liệu khảo sát.
- **Target:** `Y` nhị phân; **tuyệt đối không đưa `Y` vào features**. Kiểm tra việc có dùng được từng feature tại *prediction time* hay không.
- **Split:** Tìm hiểu liệu có participant ID/group ID không. Nếu không có, mô tả rủi ro các dòng lặp cùng người có thể rơi vào cả train/test; có thể cân nhắc stratified random split và nhấn mạnh giới hạn.
- **Baseline & models:** `DummyClassifier` (trivial) + `LogisticRegression` + `RandomForestClassifier`.
- **Preprocess:** Thiết kế `ColumnTransformer` + `Pipeline`, impute và encode trong pipeline, fit chỉ trên train; `OneHotEncoder(handle_unknown='ignore')` cho cột category; lưu ý tuổi/thu nhập không phải số thuần.
- **CV & tuning:** Cross-validation training only; chỉ dùng tập test để đánh giá **một lần sau khi chốt model**.
- **Metric:** Chọn F1 / ROC-AUC / balanced accuracy hoặc phù hợp sau khi xem phân bố `Y`; giải thích vì sao.
- **Error analysis:** Confusion matrix, xem lỗi theo `coupon`, `passanger` và các nhóm có đủ quan sát.
- **Interpretability:** Permutation importance hoặc phân tích hệ số có cân nhắc tiền xử lý.
- **Biểu đồ tối thiểu:** Confusion matrix, chart so sánh hiệu suất các model. Nên bổ sung chart lỗi theo nhóm và permutation importance.

### Tự đánh giá trước khi chốt câu hỏi

- [ ] Bộ dữ liệu thực tế có đủ mẫu trong các giao điểm phân tầng.
- [ ] Đã kiểm tra dữ liệu thiếu ảnh hưởng thế nào đến từng câu.
- [ ] Với mọi câu: cách làm đủ sâu, có ít nhất 2 plot và câu trả lời bằng con số.
- [ ] Các câu không trùng lặp mục đích, chỉ ra giới hạn của khảo sát.
- [ ] Kiểm tra các dự án public để nêu sự khác biệt và attribution.
