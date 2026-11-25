# 📋 PHÂN CÔNG CHI TIẾT & HƯỚNG TRẢ LỜI 6 CÂU HỎI

> **Môn:** CSC17104 – Lập trình cho Khoa học dữ liệu  
> **Đồ án:** In-Vehicle Coupon Acceptance Analysis  
> **Nhóm:** Trần Nhật Dương · Nguyễn Mạnh Hà · Hoàng Công Lý  
> **Nguồn:** [UCI #603](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation) · [Đề chính thức](../README.md)

> [!IMPORTANT]
> Tài liệu này là **bảng giao việc và hướng dẫn học tập**, không phải báo cáo phân tích đã hoàn thành. Những nhận định có ghi **giả thuyết** phải được kiểm chứng; không được đổi chúng thành kết luận. Không điền phần trăm, p-value, CI hoặc điểm ML khi chưa chạy dữ liệu. Đề môn học chỉ cho phép dùng AI như gia sư; mỗi thành viên phải tự thực hiện, diễn giải và viết kết luận từ số liệu của mình, ghi nhận sử dụng AI đáng kể trong `LLM_USAGE.md`.

---

## A. Phân công tổng thể

| Hạng mục | Owner chính | Người hỗ trợ / review | Sản phẩm kiểm tra |
|---|---|---|---|
| Thu thập nguồn, license, metadata, related work, lý do chọn dữ liệu | **Dương** | Hà | Phần Collection trong `01_collection_exploration.ipynb`; nguồn trong README |
| EDA (overview, missingness, duplicates, phân phối, kiểm tra nhãn, cleaning plan) | **Hà** | Dương | Phần Exploration trong `01_collection_exploration.ipynb`; dữ liệu sạch có giải thích |
| Định nghĩa metric chung, CI, ngưỡng mẫu nhỏ, tiêu chuẩn biểu đồ | **Hà** | Cả nhóm | Tiêu chuẩn phân tích dùng nhất quán cho Q1–Q5 |
| **Q1 & Q2** – hành trình và thời hạn coupon | **Dương** | Hà review | `02A_duong_q1_q2.ipynb`, ≥4 biểu đồ, bảng kết quả + CI |
| **Q3 & Q4** – thói quen và người đi cùng | **Hà** | Dương review | `02B_ha_q3_q4.ipynb`, ≥4 biểu đồ, bảng kết quả + CI |
| **Q5** – phân khúc tuổi và thu nhập | **Lý** | Hà review | `02C_ly_q5.ipynb`, ≥2 biểu đồ, bảng kết quả + CI |
| **Q6** – dự đoán Y bằng ML | **Lý** | Dương + Hà kiểm tra leakage / đọc lỗi | `03_ml_question.ipynb`, baseline, 2 mô hình, CV, test một lần, phân tích lỗi |
| Tài liệu hóa cách chạy, kiểm thử, tích hợp repo | **Dương** | Lý | README, environment, kiểm tra clone & rerun từ đầu |
| Tạo bảng hình ảnh, số liệu, thống nhất kết luận | **Hà** | Cả nhóm | `reports/figures/`, `reports/tables/`, key findings có dẫn chứng |
| Slides, demo, rehearsal, reflection cá nhân | **Cả 3** | — | `slides.pdf`, mỗi người thuyết trình phần mình và hiểu phần còn lại |

### Ma trận yêu cầu độ sâu

| Câu | Người sở hữu | Tiêu chí cần thể hiện bằng thao tác thực |
|---|---|---|
| Q1 | Dương | D3 + D4 + D5 |
| Q2 | Dương | D2 + D4 + D5 |
| Q3 | Hà | D3 + D4 + D5 + D6 |
| Q4 | Hà | D4 + D5 |
| Q5 | Lý | D4 + D5 + D6 |
| Q6 | Lý | ML riêng: baseline + ≥2 models + split phù hợp + pipeline + CV + test once + errors + interpretation |

Phạm vi non-ML bao phủ **D2, D3, D4, D5, D6** (5/6). Không cần làm D1 khi các tiêu chí khác đã được chứng minh. D2 có thể là `pivot_table`/`melt` (không được tuyên bố dataset có chuỗi ngày tháng thật).

### Cách chia công việc chung tránh xung đột Git

- `01_collection_exploration.ipynb`: Dương viết phần nguồn; Hà viết phần EDA sau khi thống nhất cấu trúc với Dương; tránh cùng commit một file notebook đồng thời.
- Mỗi người sửa notebook mang tên mình. Không thay đổi tên cột hoặc dữ liệu trong `data/raw/`.
- Lý có thể mở issue yêu cầu Hà hỗ trợ chuẩn hóa dữ liệu, nhưng **tiền xử lý train/test** của ML phải nằm trong `Pipeline` và được fit trên train.
- Mỗi pull request: mô tả câu hỏi, thay đổi số dòng, file biểu đồ, kết quả kiểm tra và lý do kết luận. Mỗi thành viên cần review ít nhất một PR của người khác.
- Chốt quy ước `acceptance_rate = mean(Y)` trong từng nhóm (với `Y` là nhị phân 0/1), đồng thời báo `n` để tránh đọc sai nhóm ít quan sát.

---

## B. Những thông tin có thể trả lời ngay từ UCI (không cần suy đoán)

1. **Mục tiêu:** nghiên cứu **ý định** chấp nhận coupon trong kịch bản lái xe giả định (`Y=1` nhận; `Y=0` không nhận). Không được gọi `Y=1` là giao dịch đã đổi coupon thành công.
2. **Quy mô UCI công bố:** 12.684 quan sát; 25 features và 1 target (CSV có 26 cột khi bao gồm `Y`).
3. **Nguồn thu thập:** khảo sát qua Amazon Mechanical Turk; có dữ liệu thiếu.
4. **License:** CC BY 4.0, yêu cầu ghi nhận nguồn/tác giả phù hợp.
5. **Các trường trong CSV cần chú ý:** `passanger` (cố ý giữ chính tả cột gốc), `has_children`, `toCoupon_GEQ15min`, `toCoupon_GEQ25min`, `direction_same`, `direction_opp`, `Y`. Tên loại coupon cần lấy bằng `df['coupon'].unique()` trước khi viết mapping. `time` chỉ là thời điểm trong ngày (7AM, 10AM, 2PM, 6PM, 10PM), **không** phải chuỗi thời gian nhiều ngày.
6. **Chưa thể khẳng định** nhóm khách hàng nào có tỷ lệ nhận cao nhất, chiều tác động của biến nào, hay mô hình nào tốt nhất nếu chưa chạy dữ liệu và kiểm tra sai số.

### Quy tắc chung cho cả 6 câu

1. Viết **question → motivation → methods → results → limitations** ngay trong notebook.
2. Trước và sau mỗi bước làm thay đổi dữ liệu: ghi số dòng `n_before`, `n_after`, số dòng bị loại và lý do. **Không xóa toàn bộ NaN một cách máy móc.**
3. Kiểm tra số mẫu cho mọi nhóm so sánh. Nhóm nhỏ cần đánh dấu rõ hoặc gộp có giải thích.
4. Với tỷ lệ chấp nhận: tính `n`, số chấp nhận `sum(Y)`, `rate=mean(Y)`; so sánh **chênh lệch điểm phần trăm** và ước lượng bất định (ví dụ khoảng tin cậy bootstrap 95%).
5. Trực quan tối thiểu **2 hình / câu**; đủ title, tên trục, đơn vị %, chú giải, và n nếu phù hợp; lưu hình vào `reports/figures/`.
6. Kết luận phải nói **“có liên hệ / trong khảo sát”**, không nói **“gây ra / làm cho”** nếu chưa có thiết kế thực nghiệm về nhân quả.
7. Sau mỗi câu trả lời: nêu một điểm bất ngờ, khả năng lý giải, hạn chế và ứng dụng thực tế có điều kiện.

---

## C. DƯƠNG — Q1, Q2 (bối cảnh hành trình và tính linh hoạt của coupon)

**Notebook:** `notebooks/02A_duong_q1_q2.ipynb`  
**Việc chung:** metadata, cách khảo sát, nguồn, license, related works, README, hướng dẫn tái lập.

### Q1 — Khoảng cách & hướng di chuyển

**Câu hỏi:** *Khoảng cách và hướng di chuyển đến địa điểm dùng coupon có liên hệ như thế nào với việc chấp nhận coupon, sau khi so sánh trong cùng mục đích hành trình và loại coupon?*

**Vì sao quan trọng?** Giúp đánh giá thời điểm/vị trí gợi ý voucher sao cho không làm người lái đi vòng quá nhiều.

**Biến:** `Y`, `toCoupon_GEQ15min`, `toCoupon_GEQ25min`, `direction_same`, `destination`, `coupon`.

**Việc phải làm theo thứ tự**

- [ ] Xem phân phối cờ 15 và 25 phút; xác nhận tính nhất quán (ví dụ ≥25 không thể đồng thời <15).
- [ ] D3: tạo `travel_time_band` từ ngưỡng **không phải phút đo chính xác**: `<15`, `15–<25`, `≥25` (đặt nhãn phù hợp ngữ nghĩa dữ liệu).
- [ ] Lập bảng `n`, `accepted`, `rate` cho `travel_time_band × direction_same`.
- [ ] D4: phân tầng theo `destination`, sau đó theo `coupon`; giải thích trường hợp ít mẫu hoặc nhóm rỗng.
- [ ] D5: tạo 95% CI cho các chênh lệch chính, ví dụ `<15` so với `≥25` trong các nhóm coupon đủ lớn.
- [ ] Vẽ hình 1: heatmap `travel_time_band × direction_same`; hình 2: grouped bars theo `destination` hoặc `coupon`.
- [ ] Viết câu trả lời riêng cho **mối liên hệ thô** và **mối liên hệ sau phân tầng**: có cùng xu hướng không?

**Cần trả lời bằng số liệu thật**

1. Nhóm thời gian nào có tỷ lệ chấp nhận cao nhất? `rate (%)` và `n` bao nhiêu?
2. Chênh lệch giữa gần và xa bao nhiêu **điểm phần trăm**? 95% CI ra sao?
3. Khác biệt có còn theo cùng một chiều trong nhóm `Home`, `Work`, `No Urgent Place` và từng `coupon`?
4. Hướng đi cùng chiều/đối chiều có làm thay đổi *mối liên hệ quan sát được* không?

**Giả thuyết cần kiểm chứng:** Càng mất công đi vòng hoặc thời gian đến nơi nhận ưu đãi càng dài, một số nhóm có thể ít muốn nhận coupon hơn. Không khẳng định trước kết quả.

**Khung diễn giải để tự điền sau khi chạy:**

> Với [n] quan sát phù hợp, nhóm thời gian [A] có tỷ lệ chấp nhận [x]%, so với [y]% ở nhóm [B] (chênh [x-y] điểm %, 95% CI [L, U]). Khi so sánh trong cùng loại coupon và mục đích chuyến đi, mối liên hệ [giữ nguyên / yếu đi / đổi chiều]. Điều này gợi ý [ý nghĩa thực tế], nhưng không thể kết luận nhân quả do [hạn chế].

**Kết quả bàn giao:** 1 bảng chính + 1 bảng phân tầng + CI + ≥2 hình + 1 đoạn kết luận do Dương tự viết.

### Q2 — Thời hạn `2h` và `1d`

**Câu hỏi:** *Liệu mối liên hệ giữa thời hạn coupon và tỷ lệ chấp nhận có khác nhau theo thời điểm trong ngày và loại coupon không?*

**Vì sao quan trọng?** Hỗ trợ cân nhắc ưu đãi ngắn hạn hay có thời gian sử dụng linh hoạt.

**Biến:** `Y`, `expiration`, `time`, `coupon`, `destination`.

**Việc phải làm**

- [ ] Kiểm tra tần suất `1d`, `2h` và từng `time`; không tự giả định phân bố cân bằng.
- [ ] D2: `pivot_table` với index=`time`, columns=`expiration`, values=`Y`, aggfunc=`mean`; kèm pivot số lượng.
- [ ] D4: lặp phép so sánh trong cùng `coupon` (và `destination` nếu đủ n).
- [ ] D5: khoảng tin cậy cho tỷ lệ hoặc chênh lệch `1d – 2h` theo các nhóm chính.
- [ ] Vẽ hình 1: grouped bars theo 5 thời điểm; hình 2: heatmap chênh lệch `1d - 2h` theo `time × coupon`.
- [ ] Phân biệt hiệu ứng của **thời hạn** với những khác biệt do **loại coupon** gây ra.

**Cần trả lời**

1. Nhìn tổng thể, loại thời hạn nào có tỷ lệ chấp nhận cao hơn, bao nhiêu điểm %?
2. Xu hướng này có xảy ra ở cả 5 thời điểm trong ngày không?
3. Khi chỉ xét riêng từng coupon, kết luận còn giống nhau không?
4. Có nhóm nào không đủ dữ liệu để kết luận chắc chắn không?

**Giả thuyết cần kiểm chứng:** Coupon `1d` có thể hấp dẫn hơn vì linh hoạt; nhưng `2h` đôi khi phù hợp nhu cầu tức thời. **Không được biến giả thuyết thành phát hiện.**

**Khung diễn giải:**

> Trong toàn mẫu, coupon `1d` được trả lời chấp nhận với tỷ lệ [a]%, còn `2h` là [b]%. Chênh lệch [a-b] điểm %. Theo thời điểm [t] và coupon [c], mối liên hệ [mô tả từ bảng thực tế]; kết quả sau khi kiểm soát loại coupon [nhất quán / không nhất quán]. Không có dữ liệu nhiều ngày nên đây là phân tích theo **khung giờ trong ngày**, không phải xu hướng thời gian dài hạn.

**Kết quả bàn giao:** 2 pivot (rate/n) + bảng chênh lệch + CI + ≥2 hình + đoạn tự diễn giải.

---

## D. HÀ — Q3, Q4 (thói quen và người đồng hành)

**Notebook:** `notebooks/02B_ha_q3_q4.ipynb`  
**Việc chung:** EDA + cleaning plan, tiêu chuẩn chất lượng, chuẩn hóa định nghĩa và xuất bảng thống nhất.

### Q3 — Sự phù hợp giữa coupon và thói quen

**Câu hỏi:** *Trong cùng loại coupon, người thường ghé loại địa điểm tương ứng có xu hướng chấp nhận ưu đãi nhiều hơn không?*

**Biến:** `coupon`, `Bar`, `CoffeeHouse`, `CarryAway`, `RestaurantLessThan20`, `Restaurant20To50`, `Y`.

**Việc phải làm**

- [ ] Kiểm tra chính xác các tên coupon bằng `df['coupon'].unique()`.
- [ ] D3: ánh xạ coupon → cột thói quen tương ứng, tạo `matched_frequency` (vd `Coffee House` → `CoffeeHouse`).
- [ ] D3: nếu hợp lý, tạo `frequent_user` theo ngưỡng **được định nghĩa trước**, chẳng hạn `1~3`, `4~8`, `gt8` mỗi tháng vs `never`, `less1`.
- [ ] Kiểm tra missingness trong các cột thói quen; không chuyển `NaN` thành `never` khi chưa có lý do.
- [ ] D4: so sánh *bên trong từng loại coupon*, không gộp mọi coupon một cách không kiểm soát.
- [ ] D5: CI cho chênh lệch frequent vs infrequent; báo `n`.
- [ ] D6: thử ngưỡng khác (`4~8`/`gt8` vs còn lại) và thử 2 xử lý NaN hợp lý để xem kết luận có thay đổi.
- [ ] Vẽ hình 1: acceptance rate theo `matched_frequency` cho từng coupon; hình 2: heatmap `coupon × frequency` kèm `n`.

**Cần trả lời**

1. Trong từng coupon, nhóm thường đến địa điểm có tỷ lệ chấp nhận bao nhiêu? Nhóm ít đến là bao nhiêu?
2. Loại coupon nào có chênh lệch lớn nhất? CI ra sao?
3. Kết luận có ổn định khi đổi ngưỡng frequent và cách xử lý thiếu dữ liệu không?
4. Thói quen nào có thể hữu ích khi cá nhân hóa ưu đãi, nhưng bị giới hạn bởi cách khảo sát?

**Giả thuyết cần kiểm chứng:** Một ưu đãi trùng sở thích có thể được chấp nhận nhiều hơn, song độ mạnh sẽ khác theo loại coupon.

**Khung diễn giải:**

> Trong nhóm coupon [loại], người có `matched_frequency` thuộc [nhóm A] chấp nhận [a]% (n=[nA]), so với [b]% ở [nhóm B] (n=[nB]). Chênh [a-b] điểm % (95% CI [L,U]). Khi đổi định nghĩa “thường xuyên” từ [ngưỡng 1] sang [ngưỡng 2], kết luận [giữ nguyên / thay đổi], vì vậy [đánh giá độ bền].

**Kết quả bàn giao:** mapping rõ ràng + 2 phương án xử lý/ngưỡng + 1 bảng sensitivity + 2 hình + đoạn tự diễn giải.

### Q4 — Ai ngồi cùng trên xe?

**Câu hỏi:** *Việc lái xe một mình, với bạn bè, trẻ em hoặc bạn đời có liên hệ ra sao với việc chấp nhận coupon khi đã xét loại coupon và mục đích đi?*

**Biến:** `passanger` (**đúng chính tả CSV**), `destination`, `coupon`, `has_children`, `Y`.

**Việc phải làm**

- [ ] Thống kê `passanger` và số mẫu từng nhóm; kiểm tra mẫu rất nhỏ.
- [ ] D4: so sánh nhóm người đi cùng **bên trong** từng `coupon` và `destination`; dùng bảng chéo rõ `n`.
- [ ] Nếu đủ dữ liệu, phân tầng thêm theo `has_children` để tránh diễn giải sai về sự hiện diện của trẻ em.
- [ ] D5: chọn 1–2 so sánh có ý nghĩa (vd Friend(s) vs Alone), báo chênh lệch điểm %, 95% CI.
- [ ] Vẽ hình 1: bars theo `passanger × coupon`; hình 2: heatmap theo `passanger × destination` (có thể lọc 1–2 loại coupon có n đủ).
- [ ] Trình bày kết quả ngược chiều giữa các coupon (nếu có), **không suy luận nhân quả**.

**Cần trả lời**

1. Nhóm đi cùng ai có tỷ lệ chấp nhận cao/thấp nhất ở mỗi coupon?
2. Với cùng coupon và destination, các nhóm có khác biệt đáng kể về mức độ hoặc độ bất định không?
3. So sánh khi không kiểm soát và sau kiểm soát có đổi chiều không?
4. Tại sao không thể nói “đi cùng bạn bè làm tăng tỷ lệ chấp nhận” chỉ từ dữ liệu khảo sát?

**Giả thuyết cần kiểm chứng:** Bối cảnh đi cùng bạn bè có thể liên hệ với mức sẵn lòng nhận coupon khác khi đi cùng trẻ nhỏ hoặc một mình; tùy coupon, mẫu và bối cảnh.

**Khung diễn giải:**

> Đối với coupon [loại] và destination [loại], nhóm [A] có tỷ lệ [x]% (n=[nA]); nhóm [B] có tỷ lệ [y]% (n=[nB]), chênh [x-y] điểm %. Dữ liệu cho thấy **mối liên hệ** [mạnh/yếu] trong nhóm so sánh này, không cho phép xác định người đồng hành là nguyên nhân vì [các yếu tố chưa kiểm soát].

**Kết quả bàn giao:** bảng chéo trước/sau phân tầng + ≥2 biểu đồ + CI + câu trả lời tự viết.

---

## E. LÝ — Q5, Q6 (phân khúc và mô hình phân loại)

**Notebook:** `notebooks/02C_ly_q5.ipynb` + `notebooks/03_ml_question.ipynb`  
**Việc chung:** rà soát tiền xử lý ML, data leakage, CV, reproducibility. Dương + Hà hỗ trợ Q6 phần kiểm tra data và kết quả.

### Q5 — Độ tuổi và thu nhập

**Câu hỏi:** *Mối liên hệ giữa nhóm tuổi, khoảng thu nhập và tỷ lệ chấp nhận coupon có còn quan sát thấy sau khi xét loại coupon và thói quen đến địa điểm tương ứng không?*

**Biến:** `age`, `income`, `coupon`, các biến thói quen phù hợp theo `coupon`, `Y`.

**Việc phải làm**

- [ ] Thống kê giá trị thực tế của `age`, `income`; tuổi có `below21`, `50plus`, thu nhập là khoảng, không ép sang số trực tiếp.
- [ ] Định nghĩa các nhóm tuổi/thu nhập để đủ số mẫu, giải thích lý do gộp.
- [ ] D4: trước hết phân tầng theo `coupon`, sau đó xét `matched_frequency` mà Hà tạo; kiểm tra nhóm quá nhỏ.
- [ ] D5: tính CI cho tỷ lệ/chênh lệch các nhóm so sánh được chọn; báo n.
- [ ] D6: thử thay đổi cách gộp tuổi/thu nhập để xem thứ tự hoặc kết luận thay đổi không.
- [ ] Vẽ hình 1: heatmap `income × coupon` với số mẫu; hình 2: rate theo nhóm tuổi trong từng coupon (kèm CI khi phù hợp).
- [ ] Chú ý phân biệt khác biệt theo tuổi/thu nhập với hiệu ứng do coupon hay sở thích.

**Cần trả lời**

1. Trong **cùng loại coupon**, nhóm tuổi và thu nhập nào có tỷ lệ chấp nhận cao/thấp? n và CI?
2. Sau khi kiểm soát tần suất đến địa điểm, khác biệt còn lại thế nào?
3. Có ô nhóm nào quá ít mẫu dẫn đến CI rộng không?
4. Đổi cách gộp nhóm có làm đổi kết luận không?

**Giả thuyết cần kiểm chứng:** Không nhất thiết thu nhập càng cao thì người dùng càng ít chấp nhận; sở thích/thói quen và loại coupon có thể giải thích một phần khác biệt quan sát.

**Khung diễn giải:**

> Trong cùng nhóm coupon [c], nhóm tuổi [a] và thu nhập [b] có tỷ lệ chấp nhận [x]% (n=[n]). Khi xét thêm thói quen tương ứng, mối liên hệ [còn/giảm/đổi chiều]. Kết quả [ổn định/không] khi dùng cách gộp tuổi [cách 1] và [cách 2]; do vậy chưa thể suy rộng vượt ngoài phạm vi khảo sát.

**Kết quả bàn giao:** 2–3 bảng nhóm có n + ≥2 biểu đồ + sensitivity + đoạn tự diễn giải.

### Q6 — Machine Learning để dự đoán nhãn Y

**Câu hỏi:** *Các thuộc tính có sẵn trước thời điểm giới thiệu coupon có thể dự đoán ý định chấp nhận `Y` tốt hơn baseline ở mức nào?*

**Vai trò:** người thiết kế quy tắc gợi ý coupon theo bối cảnh, với giả định thông tin đầu vào sẵn có trước khi gợi ý. Đây là bài toán học thuật trên dữ liệu khảo sát, chưa chứng minh hiệu quả thương mại.

**Việc phải làm, không được bỏ**

- [ ] **Xác định prediction time:** liệt kê features hợp lệ tại thời điểm gợi ý; `Y` là nhãn, không bao giờ thuộc X. Nếu dữ liệu nào không sẵn có phải loại, liệt kê rõ.
- [ ] **Chia dữ liệu:** tìm participant/user ID. Dataset công bố không có ID rõ; ghi hạn chế tiềm tàng về việc các kịch bản của cùng người vào train/test. **Không** chia theo `time` như chuỗi ngày tháng.
- [ ] **Lập baseline:** `DummyClassifier(strategy='most_frequent')` (hoặc một baseline đơn giản hợp lý khác) trên train.
- [ ] **Chọn ít nhất 2 mô hình:** `LogisticRegression`, `RandomForestClassifier`.
- [ ] **Thiết kế Pipeline:** `ColumnTransformer` + `SimpleImputer` + `OneHotEncoder(handle_unknown='ignore')` cho category; imputation/encoding nằm trong `Pipeline` cùng model để CV không leakage.
- [ ] **Tuning:** `GridSearchCV`/`RandomizedSearchCV` trên *training only*, ghi tham số, random_state, metric CV, folds. Không dùng test để chọn mô hình.
- [ ] **Test once:** sau khi chọn mô hình, đánh giá một lần trên held-out test; in confusion matrix, F1, ROC-AUC hoặc balanced accuracy (chọn metric theo mức cân bằng lớp).
- [ ] **Error analysis:** false positive/false negative theo `coupon`, `passanger`, `destination`; báo nhóm có n đủ. Ví dụ sai đại diện, không cherry-pick.
- [ ] **Model interpretation:** permutation importance trên hold-out hoặc validation có phương pháp rõ, tránh diễn giải thành quan hệ nhân quả.
- [ ] **2 biểu đồ tối thiểu:** confusion matrix + so sánh hiệu suất baseline/model. Nên thêm error-by-group và permutation importance.

**Bảng kết quả cuối phải có**

| Mô hình | CV metric (mean ± std) | Test F1 | Test ROC-AUC | Test balanced accuracy |
|---|---:|---:|---:|---:|
| Dummy baseline | [điền] | [điền] | [điền] | [điền] |
| Logistic Regression | [điền] | [điền] | [điền] | [điền] |
| Random Forest | [điền] | [điền] | [điền] | [điền] |

**Cần trả lời**

1. Mô hình có vượt baseline trên **metric được chọn từ đầu** hay không? Chênh bao nhiêu?
2. Mô hình nào được chọn sau CV; hiệu năng test ra sao?
3. False positives / false negatives tập trung ở nhóm nào; chi phí nhầm lẫn có quan trọng không?
4. Biến nào giúp dự đoán; có phải là quan hệ nhân quả không (trả lời: không)?
5. Kết quả có đáng tin cậy nếu có nhiều kịch bản từ cùng người trả lời nhưng không có participant ID không?

**Điều có thể trả lời ngay:** Đây là bài toán **phân loại nhị phân** và có thể dùng `Y` làm target. **Chưa thể khẳng định mô hình nào tốt nhất, đạt bao nhiêu điểm, hoặc có vượt baseline không** nếu chưa train/validate/test theo thiết kế.

**Khung diễn giải:**

> Trên tập train, chúng tôi so sánh baseline [x] với [m1] và [m2] qua [k]-fold CV, tối ưu theo [metric vì...]. Mô hình được chọn là [m], đạt test [metric]=[v], cao hơn baseline [delta]. Phân tích lỗi thấy [nhóm] có [đặc điểm lỗi], và permutation importance gợi ý [biến] hữu ích cho dự đoán. Đây là kết quả trên khảo sát; khả năng áp dụng thực tế còn bị giới hạn bởi [bias, participant ID, external validity].

**Kết quả bàn giao:** pipeline có thể chạy lại + bảng CV/test + error analysis + ≥2 hình + kết luận tự viết.

---

## F. Checklist từng giai đoạn (bàn giao có thể kiểm tra)

### Giai đoạn 1 — Chuẩn bị & khám phá

- **Dương:** nguồn UCI, DOI, giấy phép, ai thu thập, cách thu thập, related works, lý do chọn dữ liệu; hướng dẫn tải trong README.
- **Hà:** schema, missingness, duplicate, tỷ lệ Y, thống kê categorical/numerical hợp lý, lý do xử lý từng cột, 3–5 quan sát EDA + cleaning plan.
- **Lý:** kiểm tra biến mục tiêu, tính hợp lệ của features tại prediction time và các loại leakage có thể xảy ra; cùng review cleaning plan.
- **Cả nhóm:** xác nhận 6 câu có đủ dữ liệu, dataset đã được giảng viên chấp thuận, quy tắc Github + Conda có thể tái lập.

### Giai đoạn 2 — Phân tích từng câu

- **Dương:** hoàn tất Q1, Q2 và review Q3/Q4.
- **Hà:** hoàn tất Q3, Q4; review Q1/Q2 và Q5; hỗ trợ mô tả số liệu trong báo cáo.
- **Lý:** hoàn tất Q5 và Q6; nhận review kiểm tra leakage/CV từ 2 thành viên còn lại.
- **Cả nhóm:** 6 đoạn trả lời bằng số liệu thật + ≥12 biểu đồ + kiểm tra D2–D6 đã *được làm* chứ không chỉ liệt kê.

### Giai đoạn 3 — Hoàn tất nộp bài & bảo vệ

- **Dương:** README, tổng hợp quy trình chạy sạch từ clone, cấu trúc repo, references, slide phần mở đầu/Q1/Q2.
- **Hà:** thống nhất bảng/hình, slide phần EDA/Q3/Q4 và key findings.
- **Lý:** slide Q5/Q6, metric lựa chọn, cách chia dữ liệu, error analysis, mô hình hạn chế ở đâu.
- **Cả nhóm:** 3–5 key findings, limitations, future work, reflection **cá nhân tự viết**, LLM_USAGE.md, thuyết trình 15 phút + Q&A 10 phút. Mỗi thành viên phải giải thích được bất kỳ code nào.

### Checklist cuối cho TỪNG câu hỏi

- [ ] Câu hỏi cụ thể + motivation + người dùng thực tế + quyết định được hỗ trợ.
- [ ] Ghi rõ cột dùng, biến tạo mới và dữ liệu bị loại (nếu có).
- [ ] Có phương pháp, lý do chọn, số dòng trước/sau các bước tác động dữ liệu.
- [ ] Có **ít nhất hai** biểu đồ hoàn chỉnh.
- [ ] Có các tỷ lệ/con số thực tế + `n` + CI/test/effect size khi cần.
- [ ] Non-ML chứng minh **ít nhất hai** tiêu chí D1–D6 qua thao tác thật.
- [ ] ML chứng minh mọi yêu cầu riêng về split, baseline, models, pipeline, tuning, error, interpretation.
- [ ] Có kết luận trả lời trực tiếp, ý nghĩa thực tế, bất ngờ và hạn chế.
- [ ] Nội dung được chính người phụ trách hiểu, tự viết và có nguồn khi mượn ý/tài liệu.

---

## G. Bộ câu hỏi giảng viên có thể hỏi và định hướng trả lời

| Câu giảng viên hỏi | Ý chính nhóm nên giải thích bằng kiến thức của mình |
|---|---|
| “Một dòng trong dataset là gì?” | Một quan sát về câu trả lời chấp nhận coupon trong **một kịch bản lái xe giả định**; chưa chứng minh mỗi dòng là một người riêng biệt. |
| “Dữ liệu có thật hay synthetic?” | Khảo sát thực tế trên Mechanical Turk về các tình huống giả định, không phải dữ liệu giao dịch thực tế. |
| “Vì sao không chỉ dùng groupby?” | Đề cần phân tích sâu: biến phát sinh, kiểm soát confounder, uncertainty, robustness; các phép tổng hợp đơn giản chưa đủ. |
| “Vì sao dùng khoảng tin cậy?” | Để phản ánh mức bất định của ước lượng/chênh lệch, không chỉ dựa vào một tỷ lệ điểm. |
| “D4 là gì?” | Phân tầng/điều chỉnh theo biến khác (như loại coupon và destination) để kiểm tra xu hướng có còn không. |
| “D6 là gì?” | Thay đổi một lựa chọn phân tích hợp lý (ngưỡng frequeny/nhóm tuổi/xử lý NaN) và so sánh kết luận. |
| “Vì sao không nói A gây ra B?” | Dữ liệu quan sát qua khảo sát, không được thiết kế để suy luận tác động nhân quả. |
| “Vì sao không chia theo time cho ML?” | `time` là mốc giờ trong ngày, không phải ngày ghi nhận tuần tự. |
| “Tại sao phải pipeline?” | Đảm bảo impute/encode/tuning được fit trong từng train fold, giảm leakage vào validation/test. |
| “Vì sao so sánh baseline?” | Để chứng minh ML có giá trị cao hơn phương án dự đoán ngây thơ. |
| “Sử dụng AI như thế nào?” | Dùng để giải thích khái niệm hoặc debugging; tự chạy, hiểu, diễn giải, viết kết quả; ghi `LLM_USAGE.md`. |

---

## H. Thông tin nguồn cần trích dẫn

- UCI Machine Learning Repository, Dataset #603, DOI: <https://doi.org/10.24432/C5GS4P>.
- Dataset website: <https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation>.
- License: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Bài báo được UCI dẫn: Wang, T., Rudin, C., Doshi-Velez, F., Liu, Y., Klampfl, E., & MacNeille, P. (2017). *A Bayesian framework for learning rule sets for interpretable classification*. *Journal of Machine Learning Research*, 18(1), 2357–2393.
- Ghi nhận và đối chiếu các bài phân tích/notebook công khai trong `docs/related_work.md` trước khi nộp.
