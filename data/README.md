# Data – UCI 603

## Đường dẫn dữ liệu

- File CSV gốc: `data/raw/in-vehicle-coupon-recommendation.csv`
- Dữ liệu đã xử lý: `data/processed/` (nhóm tạo sau khi quyết định quy tắc cleaning)

## Tải dữ liệu

Chạy từ thư mục gốc repo:

```bash
python scripts/download_data.py
```

Hoặc tải trực tiếp từ trang chính thức: <https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation> và giải nén/đổi tên đúng `in-vehicle-coupon-recommendation.csv`.

**Nguồn và giấy phép:** UCI Machine Learning Repository, In-Vehicle Coupon Recommendation (ID 603), <https://doi.org/10.24432/C5GS4P>; CC BY 4.0. Giữ attribution khi sử dụng/phân phối dữ liệu.

## Nguyên tắc xử lý

1. Không chỉnh sửa nội dung trong `raw/`.
2. Luôn mô tả missing, duplicate, encoding và bất kỳ row drop nào.
3. Sau từng bước làm thay đổi dữ liệu: ghi lại số dòng trước/sau và lý do.
4. Nếu lưu processed CSV, ghi rõ notebook/script và các bước tạo ra nó.
5. Dataset lớn không được commit trong repo này (`.gitignore` đã cấu hình).
