# Kế hoạch & theo dõi công việc theo giai đoạn

> Đề yêu cầu: *trước mỗi giai đoạn, nhóm họp và ghi rõ kế hoạch (việc cần làm, thời lượng, ai làm) trên Google Sheets/Trello… và ghi link đó vào `README.md`*.
> Bảng dưới đây dựng lại từ lịch sử commit thực tế để nhóm **sao chép sang Google Sheets** (mỗi dòng một việc), rồi dán link vào mục "Kế hoạch & theo dõi công việc" của `README.md`. Cột "Ngày" lấy từ ngày commit; nhóm bổ sung ngày họp và thời lượng thực tế nếu có ghi chép.

## Giai đoạn đã hoàn thành

| Giai đoạn | Việc | Người làm | Ngày (theo commit) | Sản phẩm kiểm tra được | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 0. Khởi tạo | Tạo repo, khung thư mục, khung notebook cho cả nhóm | Dương | 10/11 | commit `repo initialized` | Xong |
| 1. Thu thập dữ liệu | Nguồn UCI #603, giấy phép CC BY 4.0, cách thu thập, related work | Dương | 17/11 | `01` mục 1, `docs/related_work.md` | Xong |
| 1. Khám phá dữ liệu | EDA, missing, duplicate, kiểm tra logic, kế hoạch tiền xử lý | Hà | 16–17/11 | `01` mục 2, `docs/dataset_dictionary.md` | Xong |
| 2. Câu hỏi & phân tích | Q1, Q2 (hành trình, thời hạn) | Dương | 17/11 | `02` Phase 2.1, hình `q1_*`, `q2_*` | Xong |
| 2. Câu hỏi & phân tích | Q3, Q4 (thói quen, người đồng hành) | Hà | 16–17/11 | `02` Phase 2.2, hình `q3_*`, `q4_*` | Xong |
| 2. Câu hỏi & phân tích | Q5 (tuổi, thu nhập, bootstrap theo người) | Lý | 17/11 | `02` Phase 2.3, hình `q5_*` | Xong |
| 3. Machine Learning | Q6 (Pipeline, CV theo người, test 1 lần, lỗi, importance) | Lý | 17/11 | `03`, hình `q6_*` | Xong |
| 4. Tích hợp | Gộp 3 nhánh, tổ chức `src/`, `run_all.py`, README, slide | Dương | 25–26/11 | nhánh `final_1` | Xong |
| 4. Hoàn thiện | Việt hóa docstring, rút gọn code, đồng bộ số Q6, Future work | Lý | 26/11 | nhánh `ly/final-fixes` | Xong |
| 5. Rà soát toàn diện | Ghim môi trường, sửa lỗi, EDA theo đề, cấu trúc câu hỏi, kiểm chứng số liệu, tài liệu hệ thống, ngân hàng vấn đáp | Lý (+ góp ý cho Dương, Hà) | 28/11 | nhánh `ly/full-audit`, `docs/BAO_CAO_KIEM_TRA.md` | Xong |

## Việc còn lại trước khi nộp (giao người, đặt hạn)

| Việc | Người làm | Hạn đề xuất | Ghi chú |
| --- | --- | --- | --- |
| Review các commit gắn nhãn phần mình trên `ly/full-audit` (đọc diff, chạy lại, hiểu từng dòng) | Dương, Hà, Lý | trước x−2 | Xem `docs/BAO_CAO_KIEM_TRA.md` mục 3 |
| Tự viết *Reflection* (khó khăn đã gặp, điều học được) trong `02_analysis.ipynb` | Mỗi người tự viết phần của mình | trước x−2 | AI không được viết hộ |
| Tạo Google Sheets/Trello kế hoạch (copy bảng này) và dán link vào README | Dương | trước x−2 | Yêu cầu của đề |
| Cập nhật mục riêng trong `LLM_USAGE.md` | Mỗi người | trước x−2 | Ghi cả lần rà soát ngày 28/11 |
| Merge nhánh hoàn chỉnh vào `main` và push | Dương (tích hợp) | trước 9:00 ngày x−2 | Đề: mọi nhánh phải được merge vào `main` |
| Mở GitHub issue báo hoàn thành, mời nhóm khác review | Dương | 9:00 ngày x−2 | Mốc của đề |
| Mỗi thành viên review project của một nhóm khác bằng GitHub issue | Dương, Hà, Lý | sau 9:00 ngày x−2 | Mốc của đề |
| Sửa theo góp ý, nộp bản cuối lên GitHub và Moodle | Cả nhóm | ngày x−1 | Mốc của đề |
| Tập thuyết trình 15 phút (+ ~5 phút Q&A); mỗi người tập trình bày **mọi** phần | Cả nhóm | trước ngày x | Giảng viên chọn người trình bày phần nào |
