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

Dự án phân tích các yếu tố **bối cảnh hành trình, thời hạn, thói quen tiêu dùng, người đồng hành và nhân khẩu học** liên quan đến **ý định chấp nhận coupon khi lái xe**, đồng thời xây dựng mô hình Machine Learning dự đoán nhãn `Y` từ các đặc trưng biết trước thời điểm gợi ý.

- **3 Phase notebook** · **19 biểu đồ** · **22 bảng CSV** · [Slide thuyết trình (`slides.pdf`)](slides.pdf)
- Bao phủ **5/6 tiêu chí độ sâu (`D2, D3, D4, D5, D6`)** cho câu hỏi thống kê và đầy đủ quy trình chống rò rỉ dữ liệu cho câu hỏi Machine Learning.

> [!IMPORTANT]
> Dữ liệu là khảo sát tình huống giả định trên Amazon Mechanical Turk (`Y = 1` là **ý định chấp nhận**, không phải giao dịch đổi coupon thật). Mọi kết quả chỉ phản ánh **mối liên hệ quan sát**, không suy diễn nhân quả.

---

## Thành viên & Phân công

| Thành viên | MSSV | Câu hỏi sở hữu | Phân công công việc chính |
| :--- | :---: | :---: | :--- |
| **Trần Nhật Dương** | `23120243` | **Q1 – Q2** | Data Collection, Related Work, phân tích hành trình & thời hạn (`Phase 2.1`), `plotting.py`, `stats.py` (CI), `scripts/`, tích hợp repo |
| **Nguyễn Mạnh Hà** | `23120248` | **Q3 – Q4** | EDA, Cleaning Plan, quy ước thống kê (`Phase 1.2–1.3`), thói quen & người đồng hành (`Phase 2.2`), `data.py`, `features.py` |
| **Hoàng Công Lý** | `24120378` | **Q5 – Q6 (ML)** | Phân khúc tuổi & thu nhập theo cụm người (`Phase 2.3`), mô hình ML chống rò rỉ (`Phase 3`), `stats.py` (cluster CI), `modeling.py` |

*(Chi tiết ranh giới module và quy tắc phối hợp xem tại [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) và [`docs/workflow_and_api.md`](docs/workflow_and_api.md).)*

---

## Bộ dữ liệu & Các phân tích công khai liên quan

| Thuộc tính | Thông tin |
| :--- | :--- |
| **Nguồn** | [UCI ML Repository #603 – In-Vehicle Coupon Recommendation](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation) · DOI [`10.24432/C5GS4P`](https://doi.org/10.24432/C5GS4P) |
| **Giấy phép** | Creative Commons Attribution 4.0 (**CC BY 4.0**) |
| **Tác giả & Bài báo gốc** | Wang, T., Rudin, C., Doshi-Velez, F., Liu, Y., Klampfl, E., & MacNeille, P. (2017), *JMLR* 18(70), 1–37 |
| **Quy mô & Nhãn** | `12.684` dòng × `26` cột (`25` đặc trưng + nhãn nhị phân `Y`: **56,84%** `Y = 1`, không thiếu nhãn) |
| **Phương pháp thu thập** | Khảo sát kịch bản lái xe giả định trên Amazon Mechanical Turk (`567` hồ sơ cá nhân phân biệt, phần lớn trả lời `22` kịch bản/người) |

Chi tiết ý nghĩa 26 cột & kiểm tra chất lượng dữ liệu: [`docs/dataset_dictionary.md`](docs/dataset_dictionary.md).

### Đối chiếu với các phân tích / notebook công khai (Related Work)

- **Wang et al. (2017)** ([JMLR](https://www.jmlr.org/papers/v18/16-003.html)): đề xuất thuật toán học tập luật diễn giải được (*Bayesian Rule Sets*) trên bộ dữ liệu gốc. Nhóm không phát triển thuật toán rule-set mới mà đi sâu phân tích thống kê có kiểm soát biến nhiễu (`D4`), định lượng bất định (`D5`) và kiểm tra độ bền (`D6`).
- **seetharamanr86 / customer_coupon_acceptance** ([GitHub](https://github.com/seetharamanr86/customer_coupon_acceptance)): thống kê mô tả tỷ lệ nhận coupon theo loại ưu đãi, thói quen và người đi cùng. Nhóm khác biệt ở việc phân tầng có hệ thống để bóc tách nghịch lý Simpson (`10AM` ở Q2), hiệu ứng che khuất bởi điểm đến (`direction_same` ở Q1) và giới hạn *common support* (`Friend(s)` vắng mặt hoàn toàn ở `Home`/`Work` trong Q4).
- **arnavkundu / MLEngineerNanoDegree-Capstone** ([GitHub](https://github.com/arnavkundu/MLEngineerNanoDegree-Capstone)): huấn luyện bộ phân loại dự đoán `Y` theo dòng. Nhóm thiết kế kiểm kê đặc trưng tại *prediction time*, tách `train`/`test` và `StratifiedGroupKFold` theo người trả lời suy ra (`respondent_id`) để chặn độ thổi phồng `+0,043` ROC-AUC do lặp người giữa hai tập.

Bảng đối chiếu đầy đủ và nguyên tắc trích dẫn: [`docs/related_work.md`](docs/related_work.md).

---

## 6 Câu hỏi nghiên cứu

| Mã | Owner | Câu hỏi nghiên cứu | Tiêu chí / Phương pháp | Vị trí |
| :--- | :---: | :--- | :--- | :--- |
| **Q1** | Dương | Khoảng cách và hướng di chuyển đến điểm dùng coupon liên hệ thế nào với tỷ lệ chấp nhận sau khi phân tầng theo mục đích chuyến đi và loại coupon? | `D3, D4, D5` | `02_analysis.ipynb` (Phase 2.1) |
| **Q2** | Dương | Chênh lệch chấp nhận giữa hạn `1d` và `2h` thay đổi ra sao theo khung giờ trong ngày và loại coupon? | `D2, D4, D5` | `02_analysis.ipynb` (Phase 2.1) |
| **Q3** | Hà | Trong cùng loại coupon, người có thói quen ghé địa điểm tương ứng thường xuyên hơn có tỷ lệ chấp nhận cao hơn không? | `D3, D4, D5, D6` | `02_analysis.ipynb` (Phase 2.2) |
| **Q4** | Hà | Người đồng hành (`passanger`) liên hệ ra sao với tỷ lệ chấp nhận sau khi kiểm soát loại coupon và mục đích hành trình (`destination`)? | `D4, D5` | `02_analysis.ipynb` (Phase 2.2) |
| **Q5** | Lý | Khác biệt tỷ lệ chấp nhận theo nhóm tuổi và khoảng thu nhập còn giữ lại bao nhiêu sau khi chuẩn hóa theo loại coupon và thói quen tương ứng? | `D4, D5, D6` | `02_analysis.ipynb` (Phase 2.3) |
| **Q6** | Lý | Các đặc trưng biết trước thời điểm hiển thị coupon dự đoán ý định `Y` vượt baseline ở mức nào khi tách dữ liệu theo người trả lời? | **ML** (`Dummy`, `LogReg`, `RF` trong `Pipeline`) | `03_ml_question.ipynb` (Phase 3) |

Chi tiết thiết kế biến và biểu đồ từng câu: [`docs/research_questions.md`](docs/research_questions.md).

---

## Các phát hiện chính (Key Findings)

1. **Loại coupon và sự khớp thói quen áp đảo nhân khẩu học:** Người ghé quán thường xuyên (`≥1` lần/tháng) chấp nhận cao hơn ở cả 5/5 loại coupon — mạnh nhất tại `Bar` (**+39,58 pp**, CI `[35,09; 44,11]`) và `Coffee House` (**+31,41 pp**, CI `[28,15; 34,58]`). Ngược lại, chênh lệch tuổi `<26 − 50+` sau chuẩn hóa thói quen còn **+7,5 pp** (CI `[2,8; 12,4]`), còn chênh lệch thu nhập `Thấp − Cao` mất ý nghĩa thống kê khi cố định tuổi (**+3,8 pp**, CI `[−0,6; 7,8]`).
2. **Phát hiện bất ngờ nhất — Nghịch lý Simpson & mất cân bằng cấu trúc khi gộp thô:** Lúc `10AM` (Q2), gộp thô cho cảm giác `2h` cao hơn `1d` (`−2,01 pp`), nhưng tách riêng từng coupon thì **cả 5/5 loại đều `1d > 2h`** (`+2,41` đến `+23,02 pp`). Tương tự, chênh lệch thô `Friend(s) − Alone` (**+14,76 pp**) thu hẹp còn **+1,33 pp** (CI `[−1,70; +4,51]`) sau chuẩn hóa `coupon × destination` vì `Friend(s)` chỉ xuất hiện ở `No Urgent Place` (`0` dòng ở `Home`/`Work`); ở Q5, nhóm thu nhập `≥100k USD` vẫn nhận **57,8%** (cao hơn trung bình mẫu `56,84%`).
3. **Độ nhạy khoảng cách và thời hạn phụ thuộc đặc thù dịch vụ:** Toàn mẫu, gần `5–<15 min` (**61,42%**) vượt xa `≥25 min` (**42,89%**, **+18,53 pp**) và hạn `1d` (**62,56%**) vượt `2h` (**49,60%**, **+12,96 pp**). Tuy nhiên `Restaurant(<20)` sụt **42,74 pp** khi xa `≥25 min` trong khi `Carry out & Take away` giữ phẳng trên **72%**; riêng `Bar` lúc `10PM` nghiêng về `2h` (`−8,87 pp`).
4. **Mô hình ML có giá trị xếp hạng ưu tiên và đòi hỏi chia theo cụm người:** Trên tập test giữ riêng (`2.552` dòng, `114` người chưa từng gặp), **Random Forest** đạt **ROC-AUC = 0,782** (CI `[0,756; 0,808]`), **Balanced Accuracy = 0,705**, vượt rõ `Logistic Regression` (`0,726`) và `Dummy` (`0,500`), dẫn dắt bởi `coupon` (`0,157`), `CoffeeHouse` (`0,058`), `expiration` (`0,049`) và `Bar` (`0,017`). Nếu chia ngẫu nhiên theo dòng thay vì theo `respondent_id`, CV ROC-AUC của Random Forest bị thổi phồng giả tạo thêm **+0,043** (`0,810` vs `0,767`).

---

## Cấu trúc repository

```text
├── README.md                              # Tổng quan, phân công, câu hỏi, kết quả chính & cách chạy
├── environment.yml                        # Môi trường Conda tái lập (Python 3.11)
├── pyproject.toml                         # Cấu hình gói nội bộ coupon_project
├── LLM_USAGE.md                           # Nhật ký sử dụng công cụ AI/LLM của từng thành viên
├── slides.pdf                             # Slide thuyết trình cuối kỳ (10 trang)
├── data/
│   ├── raw/                               # CSV gốc tải từ UCI #603 (gitignored)
│   └── processed/                         # Dữ liệu sau bước kiểm tra Phase 1 (gitignored)
├── src/coupon_project/                    # Module tái sử dụng: data, features, stats, plotting, modeling
├── notebooks/
│   ├── 01_collection_exploration.ipynb    # Phase 1: Collection, EDA, kiểm tra logic & cleaning plan
│   ├── 02_analysis.ipynb                  # Phase 2: Phân tích Q1–Q5, tổng hợp, hạn chế, hướng mở rộng & reflections
│   └── 03_ml_question.ipynb               # Phase 3: Q6 Machine Learning, error analysis & permutation importance
├── scripts/                               # download_data.py, check_project.py, run_all.py
├── tests/                                 # 11 unit tests kiểm thử các hàm cốt lõi (pytest)
├── docs/                                  # Từ điển dữ liệu, câu hỏi, related work, quy ước & hợp đồng API
├── reports/                               # figures/ (19 biểu đồ PNG) & tables/ (22 bảng CSV, gitignored)
└── presentation/                          # slides.html (nguồn xuất slides.pdf)
```

---

## Hướng dẫn cài đặt & chạy lại dự án

```bash
# 1. Clone repository
git clone https://github.com/TrNhDuong/in-vehicle-coupon-analysis.git
cd in-vehicle-coupon-analysis

# 2. Tạo và kích hoạt môi trường Conda
conda env create -f environment.yml
conda activate csc17104-coupon
pip install -e . --no-deps

# 3. Tải dữ liệu CSV gốc từ UCI #603 (vào data/raw/)
python scripts/download_data.py

# 4. Chạy kiểm tra & thực thi tuần tự toàn bộ notebook (01 -> 02 -> 03)
python scripts/run_all.py
```

Hoặc mở `jupyter lab` và chạy lần lượt theo đúng thứ tự:
1. `notebooks/01_collection_exploration.ipynb`
2. `notebooks/02_analysis.ipynb`
3. `notebooks/03_ml_question.ipynb`

> [!TIP]
> Nếu kết nối đến UCI gặp sự cố, tải thủ công file `in-vehicle-coupon-recommendation.csv` từ [trang UCI #603](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation) và đặt vào `data/raw/`, sau đó chạy `python scripts/check_project.py` và `python -m pytest -q`.

---

<div align="center">
<sub>AI/LLM chỉ dùng hỗ trợ học tập và kiểm chứng code · xem <a href="LLM_USAGE.md">LLM_USAGE.md</a></sub>
</div>
