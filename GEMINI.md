# DỰ ÁN WEBGAME "PHÁ TRỜI" (PHATROI.COM)

Tài liệu này là quy tắc tối cao cho không gian làm việc `d:\tieu-thuyet`. Dự án đã được chuyển đổi hoàn toàn thành **Webgame Phá Trời** phát hành tại [phatroi.com](https://phatroi.com).

---

## 1. ĐỊNH HƯỚNG DỰ ÁN & BỐI CẢNH MỚI
- **Tên dự án**: Webgame Phá Trời (`phatroi.com`).
- **Thể loại**: Idle / Incremental / Mini Web Action Game.
- **Tôn chỉ nội dung**: 
  - Toàn bộ nội dung tiểu thuyết cũ (nhân vật phàm nhân, Thể Đạo, Lâm Tịch, Nguyễn Minh An, v.v.) đã chính thức hủy bỏ (deprecated/removed).
  - Game tập trung vào trải nghiệm gameplay hiện đại, đồ họa dark mode cao cấp, âm thanh sinh động, tính chiến thuật, chiều sâu nâng cấp và mở khóa thế giới game độc bản.

---

## 2. QUY CHUẨN CÔNG NGHỆ & HẠ TẦNG
- **Hosting & Tên miền**:
  - Tên miền: `phatroi.com` (Quản lý tại Cloudflare Registrar & DNS).
  - Hosting: GitHub Pages miễn phí tại repo `bon-231900/pha-troi` (nhánh `gh-pages`).
- **Mã nguồn game**:
  - Toàn bộ source code nằm trong thư mục `webgame/` (HTML5, CSS, JavaScript, Web Audio API).
  - Không dùng thư viện cồng kềnh, ưu tiên tốc độ tải < 1 giây, hoạt động offline tốt, tương thích 100% Mobile & PC.
- **Quy trình xuất bản (Deployment)**:
  - Chạy lệnh: `py scripts/deploy_webgame.py` để tự động đóng gói và cập nhật trực tiếp lên `phatroi.com`.

---

## 3. NGUYÊN TẮC THIẾT KẾ GAME (GAME DESIGN PILLARS)
1. **Meaningful Progression (Thăng tiến có ý nghĩa)**:
   - Tránh việc chỉ tăng số clicker vô nghĩa (numbers-go-up vô hồn).
   - Mọi nâng cấp phải có sự thay đổi thị giác (visual change), âm thanh (audio feedback) hoặc mở khóa cơ chế mới (new mechanics/features).
2. **Build Variety (Đa dạng chiến thuật)**:
   - Người chơi có nhiều phong cách chơi để lựa chọn (Bấm tay bạo kích, Treo máy nhàn rỗi, hoặc Chiến thuật chiêu thức).
3. **Juicy Feedback**:
   - Hiệu ứng nổ sát thương, rung chấn, âm thanh Web Audio chân thực, chuyển động mượt mà.
