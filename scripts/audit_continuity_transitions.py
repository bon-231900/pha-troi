# -*- coding: utf-8 -*-
"""
Audit narrative continuity and hook resolution between consecutive chapters (Ch 1 -> 96).
Checks if items, messages, cliffhangers, or entities introduced at the end of Ch N
are dropped, contradicted, or ignored at the start of Ch N+1.
"""
import os
import glob
import re
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"

def strip_frontmatter_and_heading(text):
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    text = re.sub(r'^#\s*.*?\n', '', text)
    return text.strip()

def get_paragraphs(text):
    clean = strip_frontmatter_and_heading(text)
    paras = [p.strip() for p in clean.split('\n\n') if p.strip()]
    return paras

def audit_transitions():
    files = glob.glob(os.path.join(BASE_DIR, 'manuscript', 'markdown', '**', 'ch_*.md'), recursive=True)
    ch_files = {}
    for f in files:
        m = re.search(r'ch_(\d+)\.md', os.path.basename(f))
        if m:
            ch_files[int(m.group(1))] = f

    report_lines = []
    report_lines.append("# BÁO CÁO TOÀN DIỆN: TÍNH LIỀN MẠCH & KẾT NỐI GIỮA CÁC CHƯƠNG (CHƯƠNG 1 - 96)\n")
    report_lines.append("Rà soát chuyển tiếp giữa 95 cặp chương liên tiếp để phát hiện:")
    report_lines.append("1. Chi tiết, đồ vật, thư từ, tin nhắn, lời cảnh báo ở cuối chương N bị 'bốc hơi' ở đầu chương N+1.")
    report_lines.append("2. Lệch pha không gian/thời gian hoặc hành động bị đứt gãy đột ngột.\n")

    suspicious_count = 0

    HOOK_PATTERNS = [
        (r'(?:lá thư|bức thư|mảnh giấy|mảnh vải|tấm da|phao cứu sinh|chiếc phao|tờ giấy|phong bì)', 'THƯ TỪ / TÀI LIỆU / VẬT CHỨA TIN'),
        (r'(?:tin nhắn|cuộc gọi|điện thoại|bộ đàm|chuông điện thoại|thông báo khẩn|email|tin mật)', 'TÍN HIỆU / TIN NHẮN / BỘ ĐÀM'),
        (r'(?:kẻ phản bội|lão phu|bóng người|người đàn ông lạ|bóng đen|tiếng thét|kẻ đột nhập)', 'NHÂN VẬT BẤT NGỜ / KẺ BÍ ẨN'),
        (r'(?:tiếng nổ|phát súng|viên đạn|mũi lao|tiếng còi hú|báo động|thất thủ|chìm lỉm)', 'BIẾN CỐ / TẤN CÔNG / KHẨN CẤP'),
        (r'(?:thanh đao|đoản đao|đoản côn|lệnh bài|thanh kiếm|vũ khí|mảnh kiếm)', 'BINH KHÍ / CỔ VẬT PHÁT LỘ'),
    ]

    for i in range(1, 96):
        if i not in ch_files or (i + 1) not in ch_files:
            continue
        
        with open(ch_files[i], 'r', encoding='utf-8') as f:
            content_curr = f.read()
        with open(ch_files[i + 1], 'r', encoding='utf-8') as f:
            content_next = f.read()

        paras_curr = get_paragraphs(content_curr)
        paras_next = get_paragraphs(content_next)

        end_paras = paras_curr[-3:] if len(paras_curr) >= 3 else paras_curr
        start_paras = paras_next[:4] if len(paras_next) >= 4 else paras_next

        end_text = "\n\n".join(end_paras)
        start_text = "\n\n".join(start_paras)

        # Detect hooks in end_text
        detected_hooks = []
        for pat, label in HOOK_PATTERNS:
            matches = re.findall(pat, end_text, flags=re.IGNORECASE)
            if matches:
                # Check if matches appear in start_text (first 4 paragraphs of next chapter)
                # or in next chapter at all
                found_in_start = any(m.lower() in start_text.lower() for m in matches)
                found_in_next_full = any(m.lower() in content_next.lower() for m in matches)
                detected_hooks.append({
                    'type': label,
                    'matches': list(set(matches)),
                    'found_in_start': found_in_start,
                    'found_in_next_full': found_in_next_full
                })

        # Check for potential drop: hook exists in end of Ch i, but NOT in start of Ch i+1
        unresolved_in_start = [h for h in detected_hooks if not h['found_in_start']]

        status_icon = "🟢"
        if unresolved_in_start:
            # If not even in the entire next chapter, that's high risk (like ch 83 -> 84)
            missing_entirely = [h for h in unresolved_in_start if not h['found_in_next_full']]
            if missing_entirely:
                status_icon = "🔴 NGUY CƠ GÃY MẠCH CAO"
                suspicious_count += 1
            else:
                status_icon = "🟡 CẦN KIỂM CHỨNG NHỊP NỐI"

        report_lines.append(f"### [Chuyển tiếp {i:02d} ➔ {i+1:02d}] {status_icon}")
        if detected_hooks:
            report_lines.append("**Các móc nối / chi tiết nhận diện ở cuối chương trước:**")
            for h in detected_hooks:
                report_lines.append(f"- [{h['type']}]: `{', '.join(h['matches'])}` (Đầu chương sau: {'Có nhắc' if h['found_in_start'] else 'Không nhắc ở mở đầu'} | Toàn chương sau: {'Có xuất hiện' if h['found_in_next_full'] else 'MẤT HÚT'})")
        
        report_lines.append("\n**Đoạn cuối Chương " + str(i) + ":**")
        for p in end_paras[-2:]:
            report_lines.append(f"> {p}")

        report_lines.append("\n**Đoạn đầu Chương " + str(i+1) + ":**")
        for p in start_paras[:2]:
            report_lines.append(f"> {p}")

        report_lines.append("\n---\n")

    summary_header = f"## TỔNG KẾT: {suspicious_count} cặp chuyển tiếp có nguy cơ gãy mạch cao (chi tiết biến mất hoàn toàn)\n\n"
    report_lines.insert(3, summary_header)

    report_path = os.path.join(BASE_DIR, 'reports', 'inter_chapter_continuity_audit.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print(f"Báo cáo hoàn tất tại: {report_path}")
    print(f"Tổng số cặp chuyển tiếp nguy cơ cao: {suspicious_count}")

if __name__ == '__main__':
    audit_transitions()
