# NOVEL OS — PHÁ TRỜI (PHA_TROI)

> **Hệ điều hành sáng tác & Quản trị thực thể chuyên biệt cho tiểu thuyết trường thiên 3.000+ chương: “Phá Trời”.**

## 1. Giới thiệu
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
- **Quy trình Word / Markdown**: Viết bản thảo bằng Markdown chuẩn, tự động biên dịch và đồng bộ hóa sang file Word (.docx) chuyên nghiệp.
- **Web Studio & CLI**: Giao diện điều khiển trực quan tại `http://127.0.0.1:8765` cùng bộ lệnh CLI tiếng Việt trực tiếp.

## 3. Khởi động Web Studio
Chạy file `Chay_Studio.bat` hoặc gõ:
```bash
python -m system.cli studio
```

## 4. Lệnh CLI chính (Hỗ trợ 100% tiếng Việt)
```bash
# Sáng tác tiếp chương mới tự động
python -m system.cli viet-tiep --chuong 2

# Kiểm tra tính toàn vẹn (Continuity & Canon)
python -m system.cli kiem-tra

# Xuất bản thảo ra Word (.docx)
python -m system.cli xuat-word --chuong 1

# Tra cứu dữ liệu
python -m system.cli canon
python -m system.cli nhan-vat
python -m system.cli thoi-gian
python -m system.cli the-gioi
python -m system.cli phuc-but
python -m system.cli de-xuat
```
