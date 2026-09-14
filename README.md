# NOVEL OS — PHÁ TRỜI (PHA_TROI)

> **Hệ điều hành sáng tác & Quản trị thực thể chuyên biệt cho tiểu thuyết trường thiên 3.000+ chương: “Phá Trời”.**

[![Deploy Reader to GitHub Pages](https://github.com/bon-231900/pha-troi/actions/workflows/deploy.yml/badge.svg)](https://github.com/bon-231900/pha-troi/actions/workflows/deploy.yml)
[![Live Reader](https://img.shields.io/badge/Live_Reader-24%2F7-brightgreen)](https://bon-231900.github.io/pha-troi/)

---

## 📖 Ứng Dụng Đọc Truyện Mobile 24/7 (PWA)
- **Đọc Online / Offline mọi lúc mọi nơi (Tắt laptop vẫn đọc tốt)**: [https://bon-231900.github.io/pha-troi/](https://bon-231900.github.io/pha-troi/)
- **Tiến độ**: Quyển 1 (46/46 chương — 118,637 từ) đã sẵn sàng.
- **Tính năng nổi bật**:
  - Hỗ trợ **PWA** (Thêm vào Màn hình chính trên iOS/Android thành app riêng).
  - Chế độ **OLED Pure Black** chống mỏi mắt ban đêm, tiết kiệm pin.
  - Tùy chỉnh cỡ chữ, phông chữ (Bookerly / Sans), chế độ đọc chống phân tâm.
  - Nút **Tải toàn bộ offline** để đọc không cần kết nối mạng.

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
- **Author Authority**: Quyền tuyệt đối thuộc về Tác giả. Mọi thay đổi canon lớn đều phải có sự phê duyệt qua Proposal Engine.
- **Source of Truth**: Markdown cho bản thảo (Manuscript) & Story Bible; SQLite (`database/novel_os.db`) cho đồ thị, trạng thái, dòng thời gian, nhật ký kiểm tra.
- **Quy trình Word / Markdown / EPUB**: Viết bản thảo bằng Markdown chuẩn, tự động xuất DOCX và EPUB tiêu chuẩn.
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
