# QUY TRÌNH VẬN HÀNH NOVEL OS

## 1. Chu Trình 'Viết tiếp' (Autonomous Continuation)
Khi Author ra lệnh: **"Viết tiếp."**
Hệ thống kích hoạt pipeline khép kín gồm 10 bước:
1. **Đọc Trạng Thái Hiện Tại**: Xác định Volume, Arc, Chapter hiện tại; đọc trạng thái địa lý, thể chất, cảm xúc của các nhân vật tham gia.
2. **Lọc Ma Trận Nhận Thức**: Đọc ma trận nhận thức của POV hiện tại và các nhân vật trong cảnh (Ai biết gì, ai KHÔNG biết gì).
3. **Đóng Gói Ngữ Cảnh**: Context Builder tạo `Context Pack` tinh gọn, cách ly tuyệt đối `author_secret`.
4. **Quyết Định Hướng Đi Tự Sự**: Xác định bước chuyển biến tiếp theo (tiến triển xung đột, khám phá bí ẩn, hay khoảnh khắc đời thường).
5. **Soạn Thảo (Co-Author)**: Viết bản thảo theo đúng POV, phong cách Cinematic + Literary + Dark Fantasy.
6. **Tự Phản Biện Đa Chiều**: Self-Critique Engine quét 11 chiều kích tìm mâu thuẫn narrative.
7. **Tự Động Chuẩn Hóa**: Sửa chữa các hạt sạn nhỏ, cảnh báo nếu có lỗi lớn.
8. **Cập Nhật Trạng Thái & Bộ Nhớ**: Cập nhật vị trí, thương tích, ma trận nhận thức, quan hệ, timeline.
9. **Lưu Trữ Bền Vững**: Lưu Markdown vào `manuscript/markdown/`, biên dịch sang `manuscript/word/`.
10. **Quản Lý Git**: Tự động tạo git commit cho các thay đổi nhỏ.

## 2. Chu Trình 'Viết lại' (Targeted Revision)
Khi Author ra lệnh: **"Viết lại."**
1. Xác định phạm vi cần sửa (câu, cảnh, hay toàn bộ chương).
2. Tái tạo Context Pack tại thời điểm trước khi chương được viết.
3. Soạn lại bản thảo, sửa đổi các điểm nghẽn logic.
4. Cập nhật lại state tương ứng.
