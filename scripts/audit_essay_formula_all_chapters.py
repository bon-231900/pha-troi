import os
import re
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_DIR = r"manuscript/markdown"
chapters = sorted(glob.glob(f"{CHAPTER_DIR}/**/ch_*.md", recursive=True))

OPENING_ESSAY_PATTERNS = [
    (r"(nắng|ánh nắng|bình minh|hoàng hôn|ánh sáng|vệt nắng|vạt nắng)", "Tả ánh nắng/hoàng hôn/bình minh"),
    (r"(gió|cơn gió|ngọn gió|làn gió|gió sớm|gió đêm|gió biển)", "Tả gió"),
    (r"(mưa|cơn mưa|tiếng mưa|mưa rào|mưa giông)", "Tả mưa"),
    (r"(màn đêm|bóng đêm|đêm đã|đêm khuya|trời vừa|bầu trời|sập tối)", "Tả màn đêm/bầu trời"),
    (r"(sáng sớm|sáng hôm sau|buổi sáng|chiều muộn|chập tối|nửa đêm|tan ca|tan sở|hết giờ)", "Mốc thời gian hành chính/sinh hoạt"),
    (r"(tôi mở mắt|thức dậy|sau giấc ngủ|không tài nào chợp mắt|sau một tuần|sau khi)", "Thói quen bắt đầu ngày mới/tỉnh giấc"),
    (r"(tôi ngồi|tôi đứng|tôi nhấp|tôi uống|tôi nhìn|tôi tựa|tôi hít)", "Cử chỉ tĩnh trầm ngâm"),
]

ENDING_ESSAY_PATTERNS = [
    (r"(bánh xe số phận|số phận)", "Văn mẫu 'Bánh xe số phận'"),
    (r"(con đường phía trước|chặng đường phía trước|hành trình phía trước|phía trước mặt)", "Văn mẫu 'Con đường phía trước'"),
    (r"(một ngày mới|ngày làm việc mới|một đêm dài|chuyến hành trình|hành trình mới|chặng đường mới)\s+.*(bắt đầu|tiếp diễn|mở ra|đón chờ|chờ đợi)", "Văn mẫu 'Một hành trình/ngày mới bắt đầu'"),
    (r"(tôi biết|tôi hiểu|trong lòng tôi|trong tâm khảm|trong tâm trí)\s+.*(không bao giờ|vĩnh viễn|kiên định|sẵn sàng)", "Đúc kết tâm niệm/triết lý luận điểm"),
    (r"(ngọn lửa|huyết quản|dòng máu|thể đạo|phàm nhân)\s+.*(bùng cháy|cuộn chảy|rực cháy|kiên định|bền bỉ)", "Hô hào khí phách/thể đạo đúc kết"),
    (r"(sóng gió|bão táp|phong ba|thử thách|biến cố)\s+.*(phía trước|chờ đợi|sắp tới|đối mặt)", "Báo trước sóng gió/thử thách tương lai"),
    (r"(hẹn ước|lời thề|nghìn năm|non sông)", "Đúc kết non sông/hẹn ước"),
]

def clean_content(raw):
    # Remove YAML frontmatter if exists
    clean = raw
    if clean.startswith("---"):
        parts = clean.split("---", 2)
        if len(parts) >= 3:
            clean = parts[2]
    # Remove Markdown headers
    lines = clean.split("\n")
    filtered_lines = [l for l in lines if not l.strip().startswith("#")]
    text = "\n".join(filtered_lines).strip()
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paras

results = []

for ch_path in chapters:
    m = re.search(r"ch_(\d+)\.md", ch_path)
    if not m:
        continue
    num = int(m.group(1))
    
    with open(ch_path, "r", encoding="utf-8") as f:
        raw = f.read()
        
    paras = clean_content(raw)
    if len(paras) < 3:
        continue
        
    first_para = paras[0]
    second_para = paras[1] if len(paras) > 1 else ""
    last_para = paras[-1]
    second_last = paras[-2] if len(paras) > 1 else ""
    
    open_text = (first_para + " " + second_para).lower()
    end_text = (second_last + " " + last_para).lower()
    
    op_flags = []
    for pat, desc in OPENING_ESSAY_PATTERNS:
        if re.search(pat, open_text):
            op_flags.append(desc)
            
    end_flags = []
    for pat, desc in ENDING_ESSAY_PATTERNS:
        if re.search(pat, end_text):
            end_flags.append(desc)
            
    has_formula = (len(op_flags) >= 1 and len(end_flags) >= 1)
    severity = len(op_flags) + len(end_flags)
    
    results.append({
        "num": num,
        "first_para": first_para,
        "last_para": last_para,
        "op_flags": op_flags,
        "end_flags": end_flags,
        "has_formula": has_formula,
        "severity": severity
    })

formula_count = sum(1 for r in results if r["has_formula"])

os.makedirs("reports", exist_ok=True)
report_path = "reports/essay_formula_audit_deep.md"

with open(report_path, "w", encoding="utf-8") as out:
    out.write(f"# BÁO CÁO TOÀN DIỆN: SẠN KHUÔN MẪU 'MỞ BÀI - THÂN BÀI - KẾT BÀI' (CHƯƠNG 1 - 96)\n\n")
    out.write(f"- Tổng số chương khảo sát: **{len(results)} chương**\n")
    out.write(f"- Số chương bị dính khuôn mẫu luận điểm/tập làm văn: **{formula_count} / {len(results)} chương** ({formula_count/len(results)*100:.1f}%)\n\n")
    
    out.write("## 1. THỐNG KÊ CÁC DẤU HIỆU CÔNG THỨC NẶNG NHẤT\n\n")
    out.write("| Mức Độ | Số Chương | Đặc Điểm Nhận Diện |\n")
    out.write("| :--- | :--- | :--- |\n")
    out.write(f"| Nặng (Score >= 4) | {sum(1 for r in results if r['severity'] >= 4)} chương | Mở bài tả đủ mây gió thời tiết, kết bài hô hào đúc kết triết lý kiên định/bánh xe số phận |\n")
    out.write(f"| Trung bình (Score 2-3) | {sum(1 for r in results if 2 <= r['severity'] < 4)} chương | Mở bài hoặc kết bài dính 1 trong các văn mẫu quen thuộc |\n")
    out.write(f"| Sạch / Liền mạch (Score <= 1) | {sum(1 for r in results if r['severity'] <= 1)} chương | Vào thẳng hiện trường (Cold Open) hoặc kết thúc bằng hình ảnh cụ thể/cắt rụp |\n\n")
    
    out.write("## 2. BẢNG CHI TIẾT TỪNG CHƯƠNG BỊ DÍNH CÔNG THỨC\n\n")
    for r in results:
        status_tag = "🔴 DÍNH NẶNG" if r["severity"] >= 4 else ("🟡 CÓ SẠN" if r["has_formula"] or r["severity"] >= 2 else "🟢 ĐẠT CHUẨN")
        out.write(f"### [Chương {r['num']:03d}] — {status_tag} (Điểm: {r['severity']})\n")
        out.write(f"- **Mở bài** ({', '.join(r['op_flags']) if r['op_flags'] else 'Không dính mẫu'}):\n")
        out.write(f"> {r['first_para']}\n\n")
        out.write(f"- **Kết bài** ({', '.join(r['end_flags']) if r['end_flags'] else 'Không dính mẫu'}):\n")
        out.write(f"> {r['last_para']}\n\n")
        out.write("---\n\n")

print(f"Báo cáo hoàn tất tại: {report_path}")
print(f"Tổng số chương: {len(results)}")
print(f"Số chương dính công thức: {formula_count} / {len(results)} ({formula_count/len(results)*100:.1f}%)")
print(f"Số chương dính nặng (severity >= 4): {sum(1 for r in results if r['severity'] >= 4)}")
