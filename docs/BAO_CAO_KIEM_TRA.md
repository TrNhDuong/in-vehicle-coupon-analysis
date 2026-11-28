# Báo cáo rà soát toàn diện trước khi nộp (nhánh `ly/full-audit`)

**Thực hiện:** Hoàng Công Lý (`24120378`), có dùng Claude Code (AI) để rà soát và sửa (ghi nhận trong `LLM_USAGE.md`) · **Ngày:** 2026-11-28 · **Gốc:** `ly/final-fixes` (`934d226`)
**Cần review:** Trần Nhật Dương, Nguyễn Mạnh Hà — mỗi commit có nhãn `[owner: ...]` để chủ phần đó đọc diff, chạy lại và hiểu trước khi merge.

> **Tóm tắt:** Dự án chạy lại được từ đầu bằng một lệnh và cho đúng số liệu, sau khi ghim phiên bản thư viện. Đã đối chiếu với **đề gốc** (`Final Project.pdf` – FIT@HCMUS) và tóm tắt đề 2026 của nhóm (D1–D6, yêu cầu ML). Đã sửa toàn bộ lỗi phát hiện được (19 commit). Một số việc **chỉ thành viên tự làm được**, liệt kê ở mục 4.

## 1. Đã kiểm tra những gì, bằng cách nào
| Hạng mục | Cách kiểm tra | Kết quả cuối |
| --- | --- | --- |
| Tái lập | Cài môi trường sạch (Python 3.11.9), tải CSV từ UCI (so SHA-256), chạy `scripts/run_all.py` | Đạt: 44/44 test, 3 notebook không lỗi, 19 hình, 27 bảng, CSV gốc không đổi |
| Q1–Q5 | Chạy lại với pandas 3.1.1/numpy 2.4.6, so từng dòng output với bản đã commit | Trùng khớp 100% |
| Q6 | Chạy với scikit-learn 1.5.2 / 1.6.1 / 1.7.2 / 1.8.0 | Số phụ thuộc phiên bản → ghim 1.8.0 |
| Mọi con số trong README, markdown, slide, docs (89 khẳng định) | Tính lại độc lập bằng pandas + hàm của dự án với đúng `key`/`seed` | Đã sửa các chỗ sai, thiếu output hoặc diễn giải quá mức (mục 2) |
| Toán/thống kê trong `src/` | So `wilson_ci` với `scipy`; so bootstrap theo người với một cài đặt brute-force độc lập; tính tay trọng số chuẩn hóa | Đúng (sai lệch ~1e-14) |
| Phương pháp ML (Q6) | Kiểm tra rò rỉ, fold không trùng người, CI ghép cặp, lặp nhiều cách chia, thí nghiệm tương tác | Đúng chuẩn; bổ sung bằng chứng vào notebook |
| Hình & slide | Xem từng hình/slide, đối chiếu số | Đã xuất lại `slides.pdf` |
| Yêu cầu của đề | Đối chiếu từng mục: thu thập, khám phá, câu hỏi, tiền xử lý/phân tích, reflection, references, teamwork, mốc thời gian | Đã bổ sung phần thiếu; còn mục 4 |

## 2. Lỗi tìm thấy và cách đã sửa
| # | Mức | Vấn đề | Đã sửa (commit) | Owner |
| --- | --- | --- | --- | --- |
| 1 | Nghiêm trọng | Output notebook 02 in `PosixPath('/private/tmp/claude-501/...scratchpad/...')` — lộ đường dẫn máy và dấu vết chạy bằng AI | `save_table` không còn là dòng cuối cell; chạy lại toàn bộ (`41f3871`, `d2c24f2`, `19620df`) | Hà, Lý |
| 2 | Nghiêm trọng | 3 notebook chạy bằng 3 Python khác nhau (3.13.9 / 3.12.1 / 3.11.16), `environment.yml` không ghim phiên bản; số Q6 đổi theo phiên bản scikit-learn | Ghim phiên bản + `requirements.txt`; chạy lại cả 3 notebook trên một môi trường (`e005e96`, `19620df`) | chung |
| 3 | Nghiêm trọng | Phase 1 chưa trả lời đủ các câu hỏi khám phá của đề (ý nghĩa từng cột trong notebook, kiểu dữ liệu chưa phù hợp, cột số min/max, cột phân loại số giá trị và giá trị lạ, lý do chọn dữ liệu) | Viết lại notebook 01 theo đúng từng câu của đề (`225c7fd`, `de4d701`) | Dương, Hà |
| 4 | Cao | Q1–Q4 chưa có dòng "Câu hỏi", "Lợi ích", tách "Tiền xử lý / Phân tích"; Q6 chưa nêu câu hỏi và lợi ích | Cấu trúc lại notebook 02/03 theo khung của đề (`700c3a7`, `ab84a53`, `41f3871`, `d2c24f2`, `227794c`) | cả nhóm |
| 5 | Cao | README: CI của Q3 `[35,09; 44,11]`, `[28,15; 34,58]` không khớp output (`[35,18; 43,97]`, `[28,42; 34,38]`) | `26ed115` | Dương |
| 6 | Cao | Nhiều số trong markdown không có output nào chứng minh (Wilson CI của Y, 164 dòng thiếu, 7AM = 100% Work, Bar 10PM, 6/12 tầng đổi dấu, Carry out ngưỡng ≥4, …) | Thêm cell in ra đúng các số đó | cả nhóm |
| 7 | Cao | Khuyến nghị "2h cho Bar buổi tối" không có cơ sở (10PM: CI `[−18,37; 0,14]` chứa 0; 6PM ngược chiều +12,82 pp) | Sửa notebook, README, slide | Dương, chung |
| 8 | Trung bình | Q3 "cả 5/5 coupon": khi tính CI theo người, Carry out và Restaurant(<20) chứa 0 | Thêm bảng kiểm tra CI theo người cho Q1–Q4 ở Phase 2.4 và sửa kết luận (`ee61f56`) | Hà, chung |
| 9 | Trung bình | Q4: `+1,33 pp` chỉ là chênh lệch trong 4 tầng No Urgent Place, chưa nói rõ | Thêm bảng tách nguồn gốc (+14,76 → +5,46 → +1,33) (`3a63057`) | Hà |
| 10 | Trung bình | Slide/markdown diễn giải vượt CI: "≥100k bác bỏ…", "RF học tương tác" chưa có bằng chứng, "567 người" cho 12.520 dòng (đúng là 560), "giảm ~1/4" (đúng ≈ 23%) | Thêm bằng chứng (thí nghiệm tương tác chỉ dùng CV; % người đi bar theo tuổi) và sửa câu chữ | Lý, chung |
| 11 | Trung bình | Không có mục Tài liệu tham khảo trong notebook; reflection chưa theo 2 câu hỏi của đề; chưa có link kế hoạch trong README | Thêm References, khung reflection, chỗ dán link + `docs/KE_HOACH_CONG_VIEC.md` | chung |
| 12 | Trung bình | `scripts/*.py` crash (`UnicodeEncodeError`) khi chuyển hướng output trên Windows; `run_all.py` hỏng khi bật Smart App Control | Ép UTF-8, gọi `python -m nbconvert` (`e005e96`) | Dương |
| 13 | Thấp | Hàm thống kê sai âm thầm khi nhập sai (nhãn gõ sai, NaN trong id/tầng, `unit` sai, `wilson_ci(5, 3)`); seed khác nhau giữa pandas 2 + numpy 2 | Fail-fast + `_plain` (không đổi số đã công bố) (`f2d9f68`, `ed34551`) | Dương, Lý |
| 14 | Thấp | ~140 dòng code dài hơn 100 ký tự (đề: "đừng để dòng quá dài") | Ngắt dòng toàn bộ `src/`, `scripts/`, notebook | cả nhóm |
| 15 | Thấp | `docs/dataset_dictionary.md` nhắc module đã xóa; `BAO_CAO_SUA_DOI.md` ghi sai nguyên nhân số Q6 đổi | Sửa tài liệu | Hà, Lý |
| 16 | Thấp | Thiếu kiểm thử cho phần thống kê quan trọng | Thêm 33 test (`39e7361`) | chung |

## 3. Số liệu thay đổi (để mọi người cập nhật khi trình bày)
- **Q1–Q5: không đổi.** Thêm các số mới có output: CI theo người (Phase 2.4), `+5,46 pp` (Q4), % người đi bar theo tuổi (Q5).
- **Q6** (chạy lại với scikit-learn 1.8.0 — trùng số của nhánh `final_1`):

| Chỉ số | Cũ | Mới |
| --- | --- | --- |
| RF test ROC-AUC (CI) | 0,782 [0,756; 0,808] | **0,781 [0,755; 0,807]** |
| RF balanced accuracy | 0,705 | **0,706** |
| RF accuracy | 72,3% | **72,4%** |
| RF − LR | 0,056 [0,038; 0,074] | **0,055 [0,037; 0,074]** |
| Lỗi | 708 = 396 FP + 312 FN | **705 = 391 FP + 314 FN** |
| Bar FNR | 53,0% | **51,9%** |
| `CoffeeHouse` importance | 0,058 | **0,057** |
| Thổi phồng khi chia fold theo dòng | 0,0425 (in 4 chữ số) | **+0,043** |

Không đổi: số của LR, Dummy, F1, CV RF 0,767 ± 0,009. Mới thêm: 50 cách chia khác → RF `0,774 ± 0,012`, luôn hơn LR; LR + cột `coupon × thói quen` 0,722 → 0,748.

## 4. Việc thành viên PHẢI tự làm trước khi nộp
1. **Mỗi người tự viết Reflection** (khó khăn đã gặp; điều học được) trong `02_analysis.ipynb` — AI không được viết hộ.
2. **Review commit phần mình** trên nhánh này (đọc diff, chạy `python scripts/run_all.py`, đảm bảo giải thích được từng dòng).
3. **Tạo Google Sheets/Trello kế hoạch** (copy `docs/KE_HOACH_CONG_VIEC.md`) và **dán link vào README**.
4. **Cập nhật `LLM_USAGE.md`** (mỗi người mục của mình). Gợi ý cho mục của Lý: | `2026-11-28` | `Claude Code` | Rà soát toàn diện trước khi nộp: đối chiếu đề, kiểm chứng lại mọi số liệu, ghim môi trường, sửa lỗi script/hàm thống kê, cấu trúc lại notebook theo khung đề, viết tài liệu hệ thống và ngân hàng vấn đáp | Tự chạy lại `run_all.py` (44/44 test, 3 notebook không lỗi), đọc và kiểm tra từng commit |
5. **Merge vào `main`** trước 9:00 ngày x−2, mở **GitHub issue** báo hoàn thành; mỗi người review project của một nhóm khác; sửa và nộp bản cuối (GitHub + Moodle) ngày x−1.
6. **Cân bằng lịch sử commit** (đề yêu cầu): hiện Lý có nhiều commit hơn hẳn. Nên để Dương/Hà tự commit phần việc còn lại của mình (reflection, link kế hoạch, LLM_USAGE, chỉnh sửa sau review) từ tài khoản của họ.
7. **Ôn vấn đáp**: [`HUONG_DAN_HE_THONG.md`](HUONG_DAN_HE_THONG.md) + [`NGAN_HANG_VAN_DAP.md`](NGAN_HANG_VAN_DAP.md); tập trình bày mọi phần.

## 5. Khuyến nghị chưa áp dụng (cần nhóm quyết định)
- **CI GitHub Actions:** bước `pip install -e . --no-deps --no-build-isolation` có thể lỗi với setuptools đi kèm Python 3.11 (thiếu `bdist_wheel`). Gợi ý: thêm `python -m pip install --upgrade setuptools` và cài các phiên bản đã ghim (cần kiểm tra trên tab Actions sau khi push).
- **`pyproject.toml`:** thêm `matplotlib` vào `dependencies` (module `plotting` import ở đầu file).
- **Q6:** có thể dùng một fold của `StratifiedGroupKFold` làm tập test để tỷ lệ `Y` của test sát tỷ lệ chung (hiện 59,9% so với ~56,8%); đổi sẽ làm thay đổi toàn bộ số Q6 nên chỉ nên làm nếu còn thời gian.
- **`standardized_contrast`:** bootstrap đang dùng tỷ lệ đã làm tròn 2 chữ số (ảnh hưởng ≤ 0,11 pp lên CI, không đổi kết luận) — đã ghi trong docstring.

## 6. Cách tự kiểm tra lại
```bash
git checkout ly/full-audit
conda env create -f environment.yml && conda activate csc17104-coupon   # hoặc pip install -r requirements.txt
python -m pip install -e . --no-deps
python scripts/download_data.py
python scripts/run_all.py      # 44 passed, 3 notebook OK, 19 hình, 27 bảng
```
