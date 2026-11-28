# Slide Beamer

- `slides.tex`: mã Beamer, gồm 14 trang nội dung và 1 trang cảm ơn, khổ 16:9.
- `questions.tex`: nguyên văn 6 câu hỏi trong notebook 02 của bản `origin/final-ver2`, commit `4c3e9db`.
- `figures/`: biểu đồ PDF dạng vector dùng khi biên dịch, kèm bản PNG.
- `slides.pdf`: bản đã biên dịch bằng XeLaTeX.
- `reference_visuals.py`: dựng 16 biểu đồ gọn cho bố cục hai cột.
- `build.py`: dựng hình từ output notebook đã lưu và biên dịch lại trong repo.

## Biên dịch từ bộ mã nguồn đã đóng gói

Cài XeLaTeX cùng các gói Beamer và fontspec (MiKTeX hoặc TeX Live).
Giữ `questions.tex` và thư mục `figures/` cạnh `slides.tex`.
Chạy hai lần tại thư mục đó:

```powershell
xelatex '-interaction=nonstopmode' '-halt-on-error' 'slides.tex'
xelatex '-interaction=nonstopmode' '-halt-on-error' 'slides.tex'
```

Font chính là Segoe UI; nếu không có, dùng TeX Gyre Heros.

## Dựng lại hình từ notebook trong repo

Từ thư mục gốc repo, trong môi trường Python của dự án:

```powershell
python presentation/beamer/build.py --compile
```

Lệnh này chỉ đọc notebook và dữ liệu gốc; không sửa câu hỏi trong notebook hoặc mô hình.
Câu chữ trên slide được lưu tại `SLIDE_QUESTIONS` trong `build.py`.
Lần đồng bộ `4c3e9db` chỉ thay câu hỏi: code và toàn bộ output notebook không đổi, nên giữ nguyên kết quả, phần giải thích và các hình. Nhánh làm việc đang ở `e9ea20a`; không checkout hoặc ghi đè notebook để đồng bộ slide.
Số ML giữ theo output đã lưu với scikit-learn 1.8.0, không lấy kết quả chạy bằng phiên bản khác.
Đơn vị tỷ lệ là %, chênh lệch là điểm phần trăm (pp).

## Nội dung 15 trang

1. Mở đầu
2–3. Chủ đề, quy mô và các cột của dataset
4. Quá trình EDA
5. Quy trình phân tích thống kê
6–10. Câu 1–5: câu hỏi, cách phân tích, kết quả và giải thích
11–13. Câu 6: cách làm ML, kết quả, lỗi và giải thích
14. Tổng kết, giới hạn và hướng phát triển
15. Cảm ơn

Các lý giải về hành vi là khả năng có thể xảy ra, không phải kết luận nhân quả.
Bìa và trang cảm ơn dùng nền xanh nhạt; các trang nội dung giữ bố cục hai cột.
