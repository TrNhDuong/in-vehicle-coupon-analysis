# In-Vehicle Coupon Acceptance (CSC17104)

Phân tích các yếu tố bối cảnh, thời hạn, thói quen, người đồng hành và nhân khẩu học liên quan đến **ý định chấp nhận coupon khi lái xe**, cùng mô hình Machine Learning dự đoán nhãn `Y` (`12.684` dòng × `26` cột, [UCI Dataset #603](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation)).

> Dữ liệu khảo sát tình huống giả định trên Amazon Mechanical Turk (`Y = 1` là ý định, không phải giao dịch thật); mọi kết quả mang tính **mối liên hệ quan sát**, không suy diễn nhân quả. Toàn bộ 3 Phase notebook, **19** biểu đồ, **18** bảng, **11/11** unit tests và [slides.pdf](slides.pdf) đã hoàn tất; các thành viên cần tự điền phần *Individual reflections* trong [02_analysis.ipynb](notebooks/02_analysis.ipynb) trước khi nộp.

---

## 1. Thành viên & Phân công

| Thành viên | MSSV | Phụ trách chính | Vị trí trong 3 Phase notebooks |
| --- | --- | --- | --- |
| **Trần Nhật Dương** | `23120243` | Collection, Related Work, **Q1–Q2** (hành trình & thời hạn) | `01` (Phase 1.1) · `02` (Phase 2.1) |
| **Nguyễn Mạnh Hà** | `23120248` | EDA, Cleaning Plan, quy ước thống kê, **Q3–Q4** (thói quen & người đi cùng) | `01` (Phase 1.2–1.3) · `02` (Phase 2.2) |
| **Hoàng Công Lý** | `24120378` | **Q5** (tuổi & thu nhập theo người) · **Q6** (ML Pipeline) | `02` (Phase 2.3) · `03` (Phase 3) |

---

## 2. Bộ dữ liệu & Lưu ý chính

- **Nguồn:** UCI ML Repository #603 · DOI: [`10.24432/C5GS4P`](https://doi.org/10.24432/C5GS4P) · Giấy phép **CC BY 4.0** · Bài báo gốc: Wang et al. (2017), *JMLR* 18(70), 1–37.
- **Nhãn & chất lượng:** `Y = 1` chiếm **56,84%** (`7.210/12.684`). `car` thiếu **99,15%**, 5 cột thói quen thiếu `0,84%–1,71%` (`matched_frequency` thiếu **1,29%**); giữ nguyên `74` dòng trùng ở bản chính và kiểm tra độ nhạy riêng.
- **Đặc điểm cột gốc:** Giữ tên gốc `passanger`; `time` là **5 khung giờ trong ngày** (`7AM–10PM`), không phải chuỗi ngày tháng; `age`/`income` là nhóm phân loại có thứ tự; `toCoupon_GEQ5min` là cột hằng (`= 1`). Xem chi tiết tại [docs/dataset_dictionary.md](docs/dataset_dictionary.md).

---

## 3. Tóm tắt kết quả Q1–Q6 (`D2–D6` = 5/6 tiêu chí)

| Câu | Người | Tiêu chí | Phát hiện chính từ dữ liệu thật |
| --- | --- | --- | --- |
| **Q1** | Dương | `D3, D4, D5` | Gần (`5–<15 min`: **61,42%**) > xa (`≥25 min`: **42,89%**, **+18,53 pp**). `Restaurant(<20)` sụt **42,74 pp** khi xa, còn `Carry out` giữ **73,21%**. Phân tầng `Home` lộ rõ hiệu ứng cùng hướng (**+17,40 pp** vs thô `+1,76 pp`). |
| **Q2** | Dương | `D2, D4, D5` | `1d` (**62,56%**) > `2h` (**49,60%**, **+12,96 pp**). Lúc `10AM`, mức gộp thô âm (`-2,01 pp`) nhưng **5/5 coupon** đều `1d > 2h` (nghịch lý Simpson). `Bar` lúc `10PM` nghiêng nhẹ về `2h` (`-8,87 pp`). |
| **Q3** | Hà | `D3, D4, D5, D6` | Người ghé thường xuyên (`≥1`/tháng) chấp nhận cao hơn ở cả 5 coupon: mạnh nhất ở `Bar` (**+39,58 pp**) và `Coffee House` (**+31,41 pp**); chiều dương bền qua 4 biến thể ngưỡng/NaN và bỏ dòng trùng (`±0,29 pp`). |
| **Q4** | Hà | `D4, D5` | Gộp thô `Friend(s) − Alone` là **+14,76 pp**, thu hẹp còn **+1,33 pp** (CI `[-1,70; +4,51]`, chỉ `4/15` tầng / `41,6%` mẫu đủ `n≥30`) sau chuẩn hóa `coupon × destination` do `Friend(s)` chỉ có ở `No Urgent Place`. |
| **Q5** | Lý | `D4, D5, D6` | Cluster-bootstrap theo `567` hồ sơ người: `<26 − 50+` giảm từ `+9,7` xuống **+7,5 pp** (CI `[2,8; 12,4]`) sau chuẩn hóa thói quen; thu nhập `Thấp − Cao` mất ý nghĩa (**+3,8 pp**, CI `[-0,6; 7,8]`) khi cố định tuổi. |
| **Q6** | Lý | **ML** | Giữ `22` features trước lúc gợi ý, chia `80/20` theo người (`453` train / `114` test), tuning `Pipeline` qua 5-fold `StratifiedGroupKFold`. **Random Forest** đạt test **ROC-AUC = 0,781** (CI `[0,755; 0,807]`), **Bal. Acc. = 0,706**, **Acc. = 72,4%** (vs `Dummy` `0,500`, `LogReg` `0,726`); `coupon` và `CoffeeHouse` dẫn đầu permutation importance. |

---

## 4. Cấu trúc repository & Cách chạy

```text
├── notebooks/      # 3 Phase notebooks: 01_collection_exploration → 02_analysis → 03_ml_question
├── src/            # coupon_project: data, features, stats, plotting, modeling
├── docs/           # research_questions.md, dataset_dictionary.md, related_work.md, CONTRIBUTING.md, workflow_and_api.md
├── scripts/        # download_data.py, check_project.py, run_all.py
├── tests/          # 11 unit tests (pytest)
├── data/           # raw/ (tải từ UCI, gitignored) & processed/
├── reports/        # 19 biểu đồ (figures/) & 18 bảng CSV (tables/, gitignored)
├── presentation/   # slides.html (nguồn HTML xuất slides.pdf)
└── slides.pdf      # Slide thuyết trình cuối kỳ ở thư mục gốc
```

```bash
git clone https://github.com/TrNhDuong/in-vehicle-coupon-analysis.git
cd in-vehicle-coupon-analysis
conda env create -f environment.yml
conda activate csc17104-coupon
python scripts/download_data.py      # hoặc đặt CSV thủ công vào data/raw/in-vehicle-coupon-recommendation.csv
python scripts/run_all.py            # chạy check_project -> pytest -> thực thi 01, 02, 03
```

---

## 5. Tài liệu tham khảo & Liêm chính học thuật

- Chi tiết câu hỏi & tiêu chí: [docs/research_questions.md](docs/research_questions.md) · Quy ước phối hợp & workflow/API: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md), [docs/workflow_and_api.md](docs/workflow_and_api.md).
- Đối chiếu nghiên cứu công khai & trích dẫn nguồn: [docs/related_work.md](docs/related_work.md).
- AI/LLM chỉ dùng hỗ trợ học tập và kiểm chứng code; nhật ký sử dụng ghi tại [LLM_USAGE.md](LLM_USAGE.md).
