# ✅ Checklist theo đề CSC17104

## A. Dataset & Collection
- [ ] Dataset UCI 603 đã được giảng viên duyệt.
- [ ] Có nguồn, DOI, tổ chức/tác giả, phương pháp thu thập, đối tượng, giới hạn, giấy phép CC BY 4.0.
- [ ] Dataset đúng định dạng, tối thiểu khoảng 3.000 dòng / 10 cột.
- [ ] Liệt kê các phân tích public liên quan và điểm khác biệt.

## B. Exploration
- [ ] Thống kê số dòng/cột và ý nghĩa mỗi dòng; data types và mô tả cột.
- [ ] Kiểm tra duplicate, missing count + %, nhóm giá trị/nhãn không nhất quán.
- [ ] Kiểm tra phân phối, outlier, giá trị bất hợp lý (nếu có).
- [ ] Tìm mối liên hệ các biến phù hợp câu hỏi.
- [ ] Tóm tắt 3–5 nhận xét ban đầu và kế hoạch tiền xử lý.

## C. Phân tích – nhóm 3 người
- [ ] 6 câu hỏi, 2 câu/người; mỗi câu có motivation và người hưởng lợi.
- [ ] Mỗi câu non-ML dùng ≥2 tiêu chí D1–D6 (thể hiện bằng phân tích thực tế).
- [ ] Toàn bộ câu non-ML bao phủ ≥4 trong 6 tiêu chí.
- [ ] Mỗi câu có ≥2 biểu đồ và kết luận định lượng.
- [ ] Mỗi thay đổi rows (filter/merge/drop) có ghi số dòng và giải thích.
- [ ] Phân tích hạn chế và cách kiểm chứng độ ổn định kết luận.

## D. Machine Learning Q6
- [ ] Câu hỏi nêu người dùng mô hình, dữ liệu được biết lúc dự đoán và cột gây leakage bị loại.
- [ ] Train/test split hợp lý và thảo luận rủi ro cùng một người xuất hiện nhiều dòng.
- [ ] Trivial baseline + ít nhất 2 mô hình.
- [ ] Preprocessing nằm trong scikit-learn Pipeline.
- [ ] Tuning bằng CV trên training only; test chỉ dùng để đánh giá một lần.
- [ ] Chọn và giải thích metric; có phân tích lỗi theo nhóm/vùng dữ liệu.
- [ ] Diễn giải mô hình và trả lời câu hỏi thực tế.

## E. Nộp bài & thuyết trình
- [ ] README có tên/MSSV, phân công, nguồn, license, các câu hỏi, kết luận, hướng dẫn chạy.
- [ ] `environment.yml`, `LLM_USAGE.md`, `src/`, `notebooks/`, `data/`.
- [ ] Có `slides.pdf` tại **repo root** khi hoàn thành.
- [ ] Thuyết trình nhóm 15 phút + 10 phút Q&A; ai cũng hiểu toàn bộ code.
- [ ] Reflection riêng của Dương, Hà, Lý; AI usage log đầy đủ.
- [ ] Project được chạy lại từ môi trường mới, không lệ thuộc máy cá nhân.
