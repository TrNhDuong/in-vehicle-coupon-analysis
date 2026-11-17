# 🔎 Related work & attribution

Đề yêu cầu **liệt kê các notebook/phân tích công khai về cùng dataset** và giải thích sự khác biệt của câu hỏi nhóm. Bảng dưới đây tổng hợp các nguồn đã rà soát để đối chiếu phạm vi, phương pháp và ghi nhận bản quyền đầy đủ.

| Nguồn tham khảo | URL | Ghi nhận bản quyền / xuất xứ |
| --- | --- | --- |
| UCI Dataset #603 (*In-Vehicle Coupon Recommendation*) | <https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation> | Tong Wang & Cynthia Rudin; DOI `10.24432/C5GS4P`; giấy phép **CC BY 4.0** |
| Bài báo nghiên cứu gốc (Wang et al., 2017) | <https://www.jmlr.org/papers/v18/16-003.html> | Wang, T., Rudin, C., Doshi-Velez, F., Liu, Y., Klampfl, E., & MacNeille, P. (2017), *JMLR* 18(70), 1–37 (2357–2393) |
| Ví dụ phân tích public (GitHub) | <https://github.com/seetharamanr86/customer_coupon_acceptance> | Repo phân tích EDA công khai trên UCI #603 |
| Ví dụ notebook ML public (GitHub) | <https://github.com/arnavkundu/MLEngineerNanoDegree-Capstone> | Repo capstone ML công khai trên bài toán dự đoán chấp nhận coupon |

## Bảng đối chiếu chi tiết

| Nguồn | Họ đã hỏi / làm gì? | Nhóm khác ở đâu? | Có dùng code/ý tưởng không? Đã trích dẫn thế nào? |
| --- | --- | --- | --- |
| **Wang et al. (2017)** *(JMLR)* | Đề xuất thuật toán học tập quy tắc diễn giải được (Bayesian Rule Sets — BRS) và thu thập bộ dữ liệu khảo sát kịch bản lái xe trên Amazon Mechanical Turk để làm benchmark phân loại nhị phân. | Nhóm không đề xuất thuật toán rule-set mới mà tập trung phân tích thống kê bối cảnh hành trình/thói quen (Q1–Q5) kèm đánh giá bất định và so sánh pipeline ML chuẩn mực (Q6). | Chỉ dùng dữ liệu công khai và bối cảnh thu thập; trích dẫn bài báo gốc và DOI UCI #603 trong README và `01_collection_exploration.ipynb`. |
| **seetharamanr86 / customer_coupon_acceptance** | Tập trung EDA tỷ lệ chấp nhận theo loại coupon (như Bar, Coffee House), nhân khẩu học, thói quen và người đi cùng bằng thống kê mô tả trực quan. | Nhóm bổ sung thiết kế kiểm soát biến nhiễu có hệ thống (**D4**: phân tầng theo `destination` và `coupon`), ước lượng khoảng tin cậy bootstrap 95% (**D5**), kiểm tra độ bền ngưỡng (**D6**), và làm rõ các ô rỗng cấu trúc / nghịch lý Simpson (ví dụ `10AM` ở Q2, `direction_same` ở Q1). | Không sao chép code hay biểu đồ. Tham khảo danh mục vấn đề thường gặp để đối chiếu tránh trùng lặp Q3/Q5 của nhóm và ghi nguồn tại đây. |
| **arnavkundu / MLEngineerNanoDegree-Capstone** | Xây dựng các mô hình phân loại dự đoán biến mục tiêu `Y` cho bài toán chấp nhận coupon (so sánh mô hình ML trên bộ đặc trưng khảo sát). | Nhóm thiết kế riêng Q6 với `DummyClassifier` baseline, kiểm tra leakage theo thời điểm dự đoán (*prediction time*), đặt toàn bộ tiền xử lý vào `ColumnTransformer` + `Pipeline` chỉ fit trên tập train, phân tích lỗi theo phân khúc và thảo luận giới hạn thiếu `participant_id`. | Không dùng lại code; tự triển khai pipeline theo quy chuẩn môn CSC17104 và đối chiếu phạm vi ML. |

> **Nguyên tắc học thuật:** Mọi nhận định trong nhóm đều chạy trực tiếp từ `data/raw/in-vehicle-coupon-recommendation.csv`, luôn nhấn mạnh đây là **ý định khảo sát trong kịch bản giả định**, chỉ kết luận mối liên hệ quan sát được (không suy diễn nhân quả), và không sao chép kết luận từ nguồn ngoài.
