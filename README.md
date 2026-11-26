<div align="center">

# In-Vehicle Coupon Acceptance

**Phân tích ý định chấp nhận coupon khi lái xe & mô hình dự đoán nhãn `Y`**

CSC17104 · Lập trình cho Khoa học Dữ liệu

[![Dataset](https://img.shields.io/badge/UCI-Dataset%20%23603-0A66C2?style=flat-square)](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation)
[![License](https://img.shields.io/badge/Data-CC%20BY%204.0-16A34A?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
![Tests](https://img.shields.io/badge/Tests-11%2F11-22C55E?style=flat-square)

</div>

---

## Tổng quan

Dự án phân tích các yếu tố **bối cảnh, thời hạn, thói quen, người đồng hành và nhân khẩu học** liên quan đến **ý định chấp nhận coupon khi lái xe**, đồng thời xây dựng mô hình Machine Learning dự đoán nhãn `Y`.

- **3 Phase notebook** · **19 biểu đồ** · **18 bảng** · [Slides](slides.pdf)
- **6 câu hỏi nghiên cứu** (Q1–Q5 phân tích thống kê, Q6 Machine Learning) — chi tiết tại [`docs/research_questions.md`](docs/research_questions.md)

> [!IMPORTANT]
> Dữ liệu là khảo sát tình huống giả định (`Y = 1` là **ý định**, không phải giao dịch thật). Mọi kết quả chỉ là **mối liên hệ quan sát**, không suy diễn nhân quả.

---

## Bộ dữ liệu

| | |
| :--- | :--- |
| **Nguồn** | [UCI ML Repository #603](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation) · DOI [`10.24432/C5GS4P`](https://doi.org/10.24432/C5GS4P) |
| **Giấy phép** | CC BY 4.0 |
| **Bài báo gốc** | Wang et al. (2017), *JMLR* 18(70), 1–37 |
| **Quy mô** | `12.684` dòng × `26` cột |
| **Nhãn `Y`** | `1` = chấp nhận coupon (**56,84%**), `0` = không |
| **Nội dung** | Khảo sát trên Amazon Mechanical Turk: người tham gia hình dung đang lái xe và quyết định có nhận coupon hay không |

Chi tiết cột & lưu ý chất lượng dữ liệu: [`docs/dataset_dictionary.md`](docs/dataset_dictionary.md)

---

## Thành viên

| Thành viên | MSSV | Phụ trách |
| :--- | :---: | :--- |
| **Trần Nhật Dương** | `23120243` | Collection, Related Work, Q1–Q2 (hành trình & thời hạn) |
| **Nguyễn Mạnh Hà** | `23120248` | EDA, Cleaning Plan, quy ước thống kê, Q3–Q4 (thói quen & người đi cùng) |
| **Hoàng Công Lý** | `24120378` | Q5 (tuổi & thu nhập), Q6 (ML Pipeline) |

---

## Cấu trúc repository

```text
├── notebooks/      # 01_collection_exploration → 02_analysis → 03_ml_question
├── src/            # coupon_project: data, features, stats, plotting, modeling
├── docs/           # research_questions, dataset_dictionary, related_work, CONTRIBUTING, workflow_and_api
├── scripts/        # download_data.py, check_project.py, run_all.py
├── tests/          # 11 unit tests (pytest)
├── data/           # raw/ (tải từ UCI, gitignored) & processed/
├── reports/        # figures/ (19 biểu đồ) & tables/ (18 bảng CSV, gitignored)
├── presentation/   # slides.html (nguồn xuất slides.pdf)
└── slides.pdf      # Slide thuyết trình cuối kỳ
```

---

## Hướng dẫn chạy

```bash
# 1. Clone repository
git clone https://github.com/TrNhDuong/in-vehicle-coupon-analysis.git
cd in-vehicle-coupon-analysis

# 2. Tạo môi trường
conda env create -f environment.yml
conda activate csc17104-coupon

# 3. Tải dữ liệu
python scripts/download_data.py

# 4. Chạy toàn bộ pipeline
python scripts/run_all.py
```

> [!TIP]
> Nếu không tải được tự động, đặt file CSV thủ công vào `data/raw/in-vehicle-coupon-recommendation.csv`.
> `run_all.py` sẽ chạy lần lượt: `check_project` → `pytest` → thực thi notebook `01`, `02`, `03`.

---

<div align="center">
<sub>AI/LLM chỉ dùng hỗ trợ học tập và kiểm chứng code · xem <a href="LLM_USAGE.md">LLM_USAGE.md</a></sub>
</div>