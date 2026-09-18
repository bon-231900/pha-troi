# NOVEL OS — PHÁ TRỜI (PHA_TROI)

> **Hệ điều hành sáng tác & Quản trị thực thể chuyên biệt cho tiểu thuyết trường thiên 3.000+ chương: “Phá Trời”.**

[![Deploy Reader to GitHub Pages](https://github.com/bon-231900/pha-troi/actions/workflows/deploy.yml/badge.svg)](https://github.com/bon-231900/pha-troi/actions/workflows/deploy.yml)
[![Live Reader](https://img.shields.io/badge/Live_Reader-phatroi.com-brightgreen)](https://phatroi.com/)
[![Novel License: All Rights Reserved](https://img.shields.io/badge/Novel_Content-All_Rights_Reserved-red.svg)](LICENSE.md)
[![Code License: MIT](https://img.shields.io/badge/Novel_OS_Code-MIT-blue.svg)](LICENSE-CODE.md)

---

## 📖 Ứng Dụng Đọc Truyện Mobile 24/7 (PWA)
- **Đọc Online / Offline mọi lúc mọi nơi (Tắt máy vẫn đọc tốt)**: [https://phatroi.com/](https://phatroi.com/) *(hoặc dự phòng [GitHub Pages](https://bon-231900.github.io/pha-troi/))*
- **Tiến độ phát hành**: Tác phẩm đang được sáng tác và đồng bộ chương mới trực tiếp lên Web Reader theo thời gian thực.
- **Tính năng nổi bật**:
  - Hỗ trợ **PWA** (Thêm vào Màn hình chính trên iOS/Android dùng như app riêng).
  - Chế độ **OLED Pure Black** chống mỏi mắt ban đêm, tiết kiệm pin.
  - Tùy chỉnh cỡ chữ, phông chữ (Bookerly / Sans), chế độ đọc chống phân tâm.
  - Nút **Tải toàn bộ offline** để đọc không cần kết nối mạng.

---

## 🌌 Về Tác Phẩm: "Phá Trời"
* **Bối cảnh**: TP. Hồ Chí Minh năm 2026 — Đô thị hiện đại với những guồng quay mưu sinh cơm áo gạo tiền ngấm ngầm bị xáo trộn bởi những mạch ngầm dị biến của thiên địa.
* **Nhân vật chính**: **Nguyễn Minh An** — Một người bình thường 100%, không chuyển sinh, không hệ thống, không bàn tay vàng vô lý. Bước chân vào con đường tu đạo từ con số không, từng bước tôi luyện bản lĩnh qua bi thương và biến cố đời thực.
* **Tông giọng & Quy mô**: Trầm tĩnh, khắc kỷ, bi tráng, slow-burn chân thực, hướng tới cấu trúc thế giới trường thiên 3.000+ chương với trần quy mô được kiểm soát chặt chẽ.

---

## 1. Giới thiệu Novel OS
Novel OS được thiết kế theo tư duy *Novels as Codebases*, giải quyết triệt để các vấn đề kinh điển của tiểu thuyết trường thiên quy mô hàng nghìn chương:
- Rò rỉ thông tin trước thời hạn (Premature Knowledge Leaks & Epistemic Separation)
- Thất lạc và đứt gãy tuyến truyện (Story Thread Amnesia & Dormancy Audits)
- Sai lệch dòng thời gian & khoảng cách địa lý (Impossible Travel & Timeline Contradictions)
- Lạm phát sức mạnh & phá vỡ trần quy mô (Power Creep & Multi-Axis Escalation Budgets)
- Lãng quên phục bút (Forgotten Foreshadowing & Chekhov's Guns)
- Bão hòa công thức tự sự & sáo ngữ kết chương (Narrative Fatigue & Formulaic Cliffhanger Repetition)
- Mất tính cách nhân vật (Character Voice & Behavior Drift)
- Mất dấu bí mật của tác giả (Author Secret Isolation)

## 2. Cấu trúc cốt lõi
- **Author Authority**: Quyền tuyệt đối thuộc về Tác giả. Mọi thay đổi canon lớn đều phải qua Proposal Engine (Xem chi tiết tại [NOVEL_LOCK.md](NOVEL_LOCK.md)).
- **21 Core Engines**: Quản trị tự động từ nhận thức nhân vật, đồ thị vũ trụ, dòng thời gian đến phòng thủ bão hòa tự sự (Xem chi tiết tại [ARCHITECTURE.md](ARCHITECTURE.md)).
- **Source of Truth**: Markdown cho bản thảo (`manuscript/`) & Story Bible (`canon/`); SQLite (`database/novel_os.db`) cho đồ thị quan hệ, sự kiện và nhật ký kiểm tra.
- **Quy trình Xuất bản Tiêu chuẩn**: Viết bằng Markdown, tự động biên dịch sang DOCX, EPUB tiêu chuẩn cho Apple Books / Google Play Books.
- **Đồng bộ tự động**: Biên dịch và đẩy bản thảo mới lên GitHub Pages chỉ với 1 câu lệnh.

## 3. Lệnh CLI chính
```bash
# Đồng bộ chương mới lên Web Reader 24/7 trên điện thoại:
python scripts/sync_to_github.py

# Xuất trọn bộ ra file EPUB cho ứng dụng Apple Books / Google Play Books:
python system/reader_app/export_epub.py

# Chạy Web Studio quản trị cục bộ:
python -m system.cli studio

# Kiểm tra tính toàn vẹn (Continuity & Canon):
python -m system.cli kiem-tra
```

---

## 4. ⚖️ Bản Quyền & Giấy Phép (License & Copyright)

Dự án áp dụng cơ chế phân định bản quyền kép (**Dual-Licensing**) rõ ràng giữa nội dung sáng tác văn học và phần mềm quản trị:

> [!IMPORTANT]
> **Repository được mở Công khai (Public) để độc giả đọc truyện và tham khảo kiến trúc Novel OS. Trạng thái Public TUYỆT ĐỐI KHÔNG đồng nghĩa với việc mở mã nguồn (Open Source) nội dung tiểu thuyết.**

* **Nội dung Tiểu thuyết ("Phá Trời") — [ALL RIGHTS RESERVED](LICENSE.md)**:
  * Thuộc bản quyền sở hữu trí tuệ duy nhất của **bon-231900 / An Bình**.
  * Bao gồm: Toàn bộ bản thảo (`manuscript/`), hồ sơ thế giới & nhân vật (`canon/`), cơ sở dữ liệu cốt truyện (`database/novel_os.db`), cốt truyện, tên gọi và lore.
  * **Nghiêm cấm mọi hành vi**: Sao chép, đăng tải lại (reup), phân phối lại, sửa đổi, dịch thuật, phóng tác phái sinh, thương mại hóa, hoặc thu thập làm dữ liệu huấn luyện/tinh chỉnh AI (LLM dataset training/fine-tuning) khi chưa có sự đồng ý bằng văn bản từ tác giả.

* **Phần mềm & Tiện ích (Novel OS Engine) — [MIT LICENSE](LICENSE-CODE.md)**:
  * Áp dụng riêng cho mã nguồn phần mềm, CLI, engine quản trị, reader app và scripts (`system/`, `scripts/`, `tests/`).
  * Mã nguồn này hoàn toàn tách biệt và không bao gồm nội dung truyện.

