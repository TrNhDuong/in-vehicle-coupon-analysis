# Ghi chú chuẩn bị phần trình bày của Hà

Nguồn slide: `ha_slides.md`, 5 trang nội dung để ghép vào deck nhóm. Đây là
bản nháp AI hỗ trợ, chưa phải lời kể cá nhân hay xác nhận Hà đã làm bài.
Môi trường thiếu `load_workspace_dependencies`/runtime Artifact Tool do skill
Presentations yêu cầu, nên chưa xuất và kiểm tra PPTX/PDF. Không có `slides.pdf`
cuối kỳ. Nguồn Markdown có thể render bằng Marp trong môi trường nhóm tự chọn.

## Thời lượng gợi ý

- EDA 45–60 giây, đặt ở phần dataset chung của nhóm.
- Q3 khoảng 90 giây: mapping, kết quả chính, một sensitivity quan trọng.
- Q4 khoảng 90 giây: sự khác biệt giữa crude và common support, giới hạn quần thể.
- Giới hạn có thể ghép vào trang kết luận chung, tránh lặp lại.

## Những điều cần tự giải thích được

1. Tại sao chỉ dùng cột thói quen tương ứng coupon, thay vì gộp cả năm cột?
2. Tại sao NaN không phải `never`, và tại sao điền mode chỉ là sensitivity?
3. `rate=mean(Y)` khác chênh lệch điểm phần trăm như thế nào?
4. Bootstrap nhị phân bằng Binomial(n,p) tương đương lấy mẫu lại dòng ở đâu?
5. Thiếu participant ID ảnh hưởng giả định CI thế nào?
6. Vì sao không nói bạn bè làm tăng chấp nhận chỉ dựa trên chênh lệch 14,76?
7. Chuẩn hóa dùng những tầng nào, cùng trọng số cho hai nhóm ra sao?
8. Vì sao 1,33 điểm % không phải ước lượng cho mọi chuyến đi của toàn mẫu?
9. `has_children=1` khác đang chở trẻ em như thế nào?
10. Review nào đang chờ PR thực tế, kiểm tra nào do AI chạy và kiểm tra nào Hà tự làm?

## Hình nguồn để cân nhắc khi ghép

| Nội dung | Hình | Mục đích |
|---|---|---|
| EDA | `../reports/figures/ha_eda_missing.png` | Phân biệt thiếu car và thiếu thói quen |
| Q3 | `../reports/figures/ha_q3_frequency_heatmap.png` | Các mức tần suất, tỷ lệ và n |
| Q3 bổ sung | `../reports/figures/ha_q3_frequency_bars.png` | Bất định của từng tỷ lệ |
| Q4 | `../reports/figures/ha_q4_destination_heatmaps.png` | Ô không có dữ liệu và sự khác biệt theo bối cảnh |
| Q4 bổ sung | `../reports/figures/ha_q4_passanger_bars.png` | Mô tả trước phân tầng destination |

Các hình dùng tiếng Anh cho nhãn phân tích, nội dung notebook dùng tiếng Việt.
Khi ghép vào slide, giữ nguyên tỷ lệ hình, không cắt n/CI hoặc chữ No data.
Tránh thu nhỏ cả hình đa panel khiến không đọc được nhãn.

## Nguồn và kiểm tra số liệu

Tất cả số liệu là snapshot của CSV UCI SHA-256
`d47897367f5a12a31dece0f4e42d7bd9da76d7016b568da511b50335d08dcb43`.
Nguồn chính thức: <https://archive.ics.uci.edu/dataset/603/in+vehicle+coupon+recommendation>,
DOI <https://doi.org/10.24432/C5GS4P>, CC BY 4.0.
Chi tiết mapping, CI và common support trong `../docs/ha_analysis_protocol.md`.
Nếu thay đổi dữ liệu/phương pháp, cập nhật số trên slide từ bảng kết quả mới.
Hà tự viết reflection về trải nghiệm thực của mình.
