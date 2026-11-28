<div align="center">

# In-Vehicle Coupon Acceptance

**Phân tích ý định chấp nhận coupon khi lái xe & mô hình dự đoán nhãn `Y`**

CSC17104 · Lập trình cho Khoa học Dữ liệu

[![Dataset](https://img.shields.io/badge/UCI-Dataset%20%23603-0A66C2?style=flat-square)](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation)
[![License](https://img.shields.io/badge/Data-CC%20BY%204.0-16A34A?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
![Tests](https://img.shields.io/badge/Tests-44%2F44-22C55E?style=flat-square)

</div>

---

## Tổng quan

Dự án phân tích các yếu tố **bối cảnh hành trình, thời hạn, thói quen tiêu dùng, người đồng hành và nhân khẩu học** liên quan đến **ý định chấp nhận coupon khi lái xe**, đồng thời xây dựng mô hình Machine Learning dự đoán nhãn `Y` từ các đặc trưng biết trước thời điểm gợi ý.

- **3 Phase notebook** · **19 biểu đồ** · **27 bảng CSV** · [Slide thuyết trình (`slides.pdf`)](slides.pdf)
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

*(Chi tiết phân công, quy tắc phối hợp và hợp đồng module xem tại [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) và [`docs/workflow_and_api.md`](docs/workflow_and_api.md).)*

---

## Bộ dữ liệu & Các phân tích công khai liên quan

| Thuộc tính | Thông tin |
| :--- | :--- |
| **Nguồn** | [UCI ML Repository #603 – In-Vehicle Coupon Recommendation](https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation) · DOI [`10.24432/C5GS4P`](https://doi.org/10.24432/C5GS4P) |
| **Giấy phép** | Creative Commons Attribution 4.0 (**CC BY 4.0**) |
| **Tác giả & Bài báo gốc** | Wang, T., Rudin, C., Doshi-Velez, F., Liu, Y., Klampfl, E., & MacNeille, P. (2017), *JMLR* 18(70), 1–37 |
| **Quy mô & Nhãn** | `12.684` dòng × `26` cột (`25` đặc trưng + nhãn nhị phân `Y`: **56,84%** `Y = 1`, không thiếu nhãn) |
| **Phương pháp thu thập** | Khảo sát kịch bản lái xe giả định trên Amazon Mechanical Turk (`567` hồ sơ cá nhân phân biệt, phần lớn trả lời `22` kịch bản/người) |

Chi tiết ý nghĩa 26 cột & kiểm tra chất lượng dữ liệu xem tại [`notebooks/01_collection_exploration.ipynb`](notebooks/01_collection_exploration.ipynb).

### Đối chiếu với các phân tích / notebook công khai (Related Work)

- **Wang et al. (2017)** ([JMLR](https://www.jmlr.org/papers/v18/16-003.html)): đề xuất thuật toán học tập luật diễn giải được (*Bayesian Rule Sets*) trên bộ dữ liệu gốc. Nhóm không phát triển thuật toán rule-set mới mà đi sâu phân tích thống kê có kiểm soát biến nhiễu (`D4`), định lượng bất định (`D5`) và kiểm tra độ bền (`D6`).
- **seetharamanr86 / customer_coupon_acceptance** ([GitHub](https://github.com/seetharamanr86/customer_coupon_acceptance)): thống kê mô tả tỷ lệ nhận coupon theo loại ưu đãi, thói quen và người đi cùng. Nhóm khác biệt ở việc phân tầng có hệ thống để bóc tách nghịch lý Simpson (`10AM` ở Q2), hiệu ứng che khuất bởi điểm đến (`direction_same` ở Q1) và giới hạn *common support* (`Friend(s)` vắng mặt hoàn toàn ở `Home`/`Work` trong Q4).
- **arnavkundu / MLEngineerNanoDegree-Capstone** ([GitHub](https://github.com/arnavkundu/MLEngineerNanoDegree-Capstone)): huấn luyện bộ phân loại dự đoán `Y` theo dòng. Nhóm thiết kế kiểm kê đặc trưng tại *prediction time*, tách `train`/`test` và `StratifiedGroupKFold` theo người trả lời suy ra (`respondent_id`) để chặn độ thổi phồng `+0,043` ROC-AUC xảy ra khi cùng một người nằm ở cả fold huấn luyện lẫn fold kiểm định.

---

## 6 Câu hỏi nghiên cứu

| Mã | Owner | Câu hỏi nghiên cứu | Tiêu chí / Phương pháp | Vị trí |
| :--- | :---: | :--- | :--- | :--- |
| **Q1** | Dương | Khoảng cách và hướng di chuyển liên hệ ra sao với tỷ lệ chấp nhận phiếu ưu đãi theo từng mục đích đi và loại dịch vụ? | `D3, D4, D5` | `02_analysis.ipynb` (Phase 2.1) |
| **Q2** | Dương | Tỷ lệ chấp nhận giữa phiếu ưu đãi có hạn `2h` và `1d` thay đổi thế nào theo khung giờ trong ngày và loại dịch vụ? | `D2, D4, D5` | `02_analysis.ipynb` (Phase 2.1) |
| **Q3** | Hà | Trong cùng loại dịch vụ, người có thói quen ghé địa điểm thường xuyên có tỷ lệ chấp nhận phiếu ưu đãi cao hơn không? | `D3, D4, D5, D6` | `02_analysis.ipynb` (Phase 2.2) |
| **Q4** | Hà | Người đồng hành (`passanger`) liên hệ thế nào với việc chấp nhận phiếu ưu đãi khi xét cùng loại dịch vụ và mục đích chuyến đi? | `D4, D5` | `02_analysis.ipynb` (Phase 2.2) |
| **Q5** | Lý | Khác biệt tỷ lệ chấp nhận phiếu ưu đãi theo tuổi và thu nhập có còn tồn tại sau khi kiểm soát loại dịch vụ và thói quen tiêu dùng? | `D4, D5, D6` | `02_analysis.ipynb` (Phase 2.3) |
| **Q6** | Lý | Thông tin sẵn có trước lúc hiển thị phiếu ưu đãi dự đoán ý định `Y` vượt baseline ở mức nào khi tách dữ liệu theo người trả lời? | **ML** (`Dummy`, `LogReg`, `RF` trong `Pipeline`) | `03_ml_question.ipynb` (Phase 3) |

Chi tiết thiết kế biến và biểu đồ từng câu: [`docs/research_questions.md`](docs/research_questions.md).

---

## Các phát hiện chính (Key Findings)

1. **Loại coupon và sự khớp thói quen áp đảo nhân khẩu học:** Người ghé quán thường xuyên (`≥1` lần/tháng) có tỷ lệ chấp nhận cao hơn ở cả 5/5 loại coupon (ước lượng điểm) — mạnh nhất tại `Bar` (**+39,58 pp**, CI `[35,18; 43,97]`) và `Coffee House` (**+31,41 pp**, CI `[28,42; 34,38]`); khi tính CI theo người, `Bar`, `Coffee House`, `Restaurant(20-50)` vẫn rõ ràng còn `Carry out` và `Restaurant(<20)` chưa phân biệt được với 0. Ngược lại, chênh lệch tuổi `<26 − 50+` sau chuẩn hóa thói quen còn **+7,5 pp** (CI `[2,8; 12,4]`), còn chênh lệch thu nhập `Thấp − Cao` mất ý nghĩa thống kê khi cố định tuổi (**+3,8 pp**, CI `[−0,6; 7,8]`).
2. **Phát hiện bất ngờ nhất — Nghịch lý Simpson & mất cân bằng cấu trúc khi gộp thô:** Lúc `10AM` (Q2), gộp thô cho cảm giác `2h` cao hơn `1d` (`−2,01 pp`), nhưng tách riêng từng coupon thì **cả 5/5 loại đều có ước lượng `1d > 2h`** (`+2,41` đến `+23,02 pp`). Tương tự, chênh lệch thô `Friend(s) − Alone` (**+14,76 pp**) thu hẹp còn **+1,33 pp** (CI `[−1,70; +4,51]`) sau chuẩn hóa `coupon × destination` vì `Friend(s)` chỉ xuất hiện ở `No Urgent Place` (`0` dòng ở `Home`/`Work`); ở Q5, nhóm thu nhập `≥100k USD` vẫn nhận **57,8%** — không thấp hơn trung bình mẫu `56,84%`.
3. **Độ nhạy khoảng cách và thời hạn phụ thuộc đặc thù dịch vụ:** Toàn mẫu, gần `5–<15 min` (**61,42%**) vượt xa `≥25 min` (**42,89%**, **+18,53 pp**) và hạn `1d` (**62,56%**) vượt `2h` (**49,60%**, **+12,96 pp**). Tuy nhiên `Restaurant(<20)` giảm **42,74 pp** khi xa `≥25 min` trong khi `Carry out & Take away` giữ phẳng trên **72%**; riêng `Bar` gần như không phụ thuộc thời hạn (`+0,85 pp`, CI chứa 0).
4. **Mô hình ML có giá trị xếp hạng ưu tiên và đòi hỏi chia theo cụm người:** Trên tập test giữ riêng (`2.552` dòng, `114` người chưa từng gặp), **Random Forest** đạt **ROC-AUC = 0,781** (CI `[0,755; 0,807]`), **Balanced Accuracy = 0,706**, vượt rõ `Logistic Regression` (`0,726`) và `Dummy` (`0,500`); lặp lại với 50 cách chia theo người, RF đạt `0,774 ± 0,012` và luôn hơn LR. Mô hình dựa chủ yếu vào `coupon` (`0,1573`), `CoffeeHouse` (`0,0569`), `expiration` (`0,0495`) và `Bar` (`0,0168`). Nếu chia fold CV ngẫu nhiên theo dòng thay vì theo `respondent_id`, CV ROC-AUC của Random Forest bị thổi phồng giả tạo thêm **+0,043** (`0,810` vs `0,767`).

---

## Cấu trúc repository

```text
├── README.md                              # Tổng quan, phân công, câu hỏi, kết quả chính & cách chạy
├── environment.yml                        # Môi trường Conda tái lập (Python 3.11, thư viện đã ghim phiên bản)
├── requirements.txt                       # Cùng bộ phiên bản cho người cài bằng pip
├── pyproject.toml                         # Cấu hình gói nội bộ coupon_project
├── LLM_USAGE.md                           # Nhật ký sử dụng công cụ AI/LLM của từng thành viên
├── slides.pdf                             # Slide thuyết trình cuối kỳ (16 trang, khổ 16:9)
├── data/
│   ├── raw/                               # CSV gốc tải từ UCI #603 (gitignored)
│   └── processed/                         # Dữ liệu sau bước kiểm tra Phase 1 (gitignored)
├── src/coupon_project/                    # Module tái sử dụng: data, features, stats, plotting, modeling
├── notebooks/
│   ├── 01_collection_exploration.ipynb    # Phase 1: Collection, EDA, kiểm tra logic & cleaning plan
│   ├── 02_analysis.ipynb                  # Phase 2: Phân tích Q1–Q5, tổng hợp, hạn chế, hướng mở rộng & reflections
│   └── 03_ml_question.ipynb               # Phase 3: Q6 Machine Learning, error analysis & permutation importance
├── scripts/                               # download_data.py, check_project.py, run_all.py
├── tests/                                 # 44 unit tests kiểm thử các hàm cốt lõi (pytest)
├── docs/                                  # CONTRIBUTING.md, research_questions.md, workflow_and_api.md
├── reports/                               # figures/ (19 biểu đồ PNG) & tables/ (27 bảng CSV, gitignored)
└── presentation/beamer/                   # Mã nguồn LaTeX Beamer & script dựng biểu đồ xuất slides.pdf
```

---

## Hướng dẫn cài đặt & chạy lại dự án

```bash
# 1. Clone repository
git clone https://github.com/TrNhDuong/in-vehicle-coupon-analysis.git
cd in-vehicle-coupon-analysis

# 2. Tạo và kích hoạt môi trường Conda (phiên bản thư viện đã ghim để ra đúng số liệu)
conda env create -f environment.yml
conda activate csc17104-coupon
python -m pip install -e . --no-deps
#    (không dùng Conda: tạo venv Python 3.11 rồi `python -m pip install -r requirements.txt`
#     và `python -m pip install -e . --no-deps`)

# 3. Tải dữ liệu CSV gốc từ UCI #603 (vào data/raw/; script tự kiểm tra SHA-256)
python scripts/download_data.py

# 4. Chạy kiểm tra & thực thi tuần tự toàn bộ notebook (01 -> 02 -> 03), khoảng 3 phút
python scripts/run_all.py
```

> [!NOTE]
> Số liệu Q6 phụ thuộc phiên bản `scikit-learn` (đã ghim `1.8.0`; bản ≤ 1.7 chia fold `StratifiedGroupKFold` khác). Trên Windows, luôn gọi công cụ qua `python -m ...` (ví dụ `python -m pytest`) — `run_all.py` đã làm như vậy để chạy được cả khi bật Smart App Control.

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
