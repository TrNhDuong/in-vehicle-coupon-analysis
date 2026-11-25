# Data – UCI #603

## Đường dẫn & Cách tải

- CSV gốc: `data/raw/in-vehicle-coupon-recommendation.csv` (**không chỉnh sửa trực tiếp**, bị `.gitignore` loại).
- Dữ liệu dẫn xuất cho mô tả: `data/processed/analysis_ready.csv` (giữ nguyên `12.684` dòng × `26` cột raw, chỉ thêm `matched_frequency` và `frequent_user`; **không** dùng cho ML).

```bash
python scripts/download_data.py
```

Hoặc tải từ [UCI Dataset #603](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation) (`DOI: 10.24432/C5GS4P`, **CC BY 4.0**). Chi tiết 26 cột và quy ước xử lý xem tại [docs/dataset_dictionary.md](../docs/dataset_dictionary.md).
