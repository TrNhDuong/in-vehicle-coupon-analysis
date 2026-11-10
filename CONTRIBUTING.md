# 🤝 Hướng dẫn cộng tác – Dương / Hà / Lý

## Quy ước Git

- Dùng `main` cho bản chạy được; mỗi người phát triển trên nhánh riêng: `duong/q1-q2`, `ha/q3-q4`, `ly/q5-ml`.
- Commit nhỏ, có thông điệp rõ ràng, ví dụ: `docs: define Q2 methods` hoặc `eda: check missing values`.
- Không push lên GitHub CSV lớn, khóa truy cập hay file môi trường cục bộ.
- Khi mở Pull Request, điền `.github/PULL_REQUEST_TEMPLATE.md`. Người khác kiểm tra notebook chạy được, logic và giải thích.
- **Không thay đổi dữ liệu gốc** trong `data/raw/`. Nếu cần xử lý, ghi các bước vào notebook và tạo bản mới trong `data/processed/`.
- Trước khi merge, kiểm tra `git status`, `python -m pytest -q` và notebook đã restart/run all từ đầu.

## Phân công

| Nhánh | Người sở hữu | Notebook |
| --- | --- | --- |
| `duong/q1-q2` | Trần Nhật Dương | `02A_duong_q1_q2.ipynb` |
| `ha/q3-q4` | Nguyễn Mạnh Hà | `02B_ha_q3_q4.ipynb` |
| `ly/q5-ml` | Hoàng Công Lý | `02C_ly_q5.ipynb`, `03_ml_question.ipynb` |
| `main` | Cả nhóm | `01_collection_exploration.ipynb`, `02_analysis.ipynb`, README, slides |

Người sở hữu câu hỏi có trách nhiệm trình bày phần của mình; tất cả thành viên cần hiểu cả project.

## Tránh xung đột notebook

- Chỉ một người edit một notebook tại một thời điểm, đặc biệt notebook chung.
- Trước commit, xóa output thừa và traceback mang tính cá nhân.
- Đặt hình xuất từ notebook vào `reports/figures/` nếu cần đưa vào slide/README.
- Không xóa dòng dữ liệu trong im lặng: ghi **row count trước/sau**, lý do và lưu quyết định.

## Definition of Done cho mỗi câu hỏi

- [ ] Motivation: vì sao câu hỏi đáng trả lời và ai cần câu trả lời.
- [ ] Liệt kê cột và kiểm tra chất lượng dữ liệu liên quan.
- [ ] Giải thích trước các quyết định tiền xử lý; log số dòng trước/sau từng bước thay đổi.
- [ ] Mô tả phương pháp phù hợp với D1–D6 (non-ML), hoặc đủ các yêu cầu ML.
- [ ] Có **ít nhất 2 biểu đồ** với title, axes, unit, legend khi cần.
- [ ] Trả lời **bằng số liệu thật**, nêu ý nghĩa, bất ngờ, giới hạn.
- [ ] Notebook chạy được từ kernel mới; người khác đã review.
