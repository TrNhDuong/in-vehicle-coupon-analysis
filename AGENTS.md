# AGENTS.md – Quy tắc bắt buộc cho AI / Coding Agent

1. **Xác nhận người dùng trước khi sửa:** Nếu người dùng chưa nói rõ mình là **Trần Nhật Dương (`23120243`)**, **Nguyễn Mạnh Hà (`23120248`)** hay **Hoàng Công Lý (`24120378`)**, phải hỏi lại trước khi chỉnh sửa file.
2. **Chỉ sửa đúng phạm vi sở hữu:** Đọc [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) (Mục 1) để biết ranh giới file/notebook của từng người. Tuyệt đối **không** sửa code, notebook hoặc mục nhật ký trong [LLM_USAGE.md](LLM_USAGE.md) thuộc về thành viên khác (chỉ sửa phần tích hợp chung khi được yêu cầu rõ).
3. **Giữ ổn định hợp đồng API & dữ liệu gốc:** Trước khi đụng `src/coupon_project/`, đọc [docs/workflow_and_api.md](docs/workflow_and_api.md); không tự ý đổi tên tham số, kiểu trả về hoặc đơn vị (`%`, `pp`). Không sửa `data/raw/` và thao tác trên `df.copy()`.
4. **Trung thực học thuật:** Mọi con số đưa vào Markdown/slide phải lấy từ output chạy thật; không tự bịa số liệu và không viết hộ *Individual reflections* trong `notebooks/02_analysis.ipynb`.
5. **Kiểm chứng sau khi sửa:** Chạy `python scripts/check_project.py` và `python -m pytest -q` (hoặc `python scripts/run_all.py` nếu sửa logic phân tích/notebook) trước khi báo hoàn thành, đồng thời nhắc sinh viên cập nhật mục riêng trong [LLM_USAGE.md](LLM_USAGE.md).
