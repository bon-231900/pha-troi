# -*- coding: utf-8 -*-
"""
Anti-AI Smell Auditor & Human Cadence Linter for Pha Troi
Phát hiện và cảnh báo 6 nhóm tử huyệt văn phong AI trong bản thảo.
Sử dụng:
    py scripts/audit_anti_ai_smells.py --chapter 90 91
    py scripts/audit_anti_ai_smells.py --all
    py scripts/audit_anti_ai_smells.py --fix-bolds --chapter 90 91
"""
import os
import sys
import re
import argparse
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"
MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript", "markdown")

CLICHE_PHRASES = [
    ("mỉm cười điềm đạm", "Văn mẫu dịch convert Tiên hiệp"),
    ("thanh tao", "Văn mẫu miêu tả nhân vật nữ convert"),
    ("hít sâu một hơi", "Cử chỉ sáo mòn kinh điển của LLM"),
    ("hít một hơi thật sâu", "Cử chỉ sáo mòn kinh điển của LLM"),
    ("sáng quắc như đèn pha", "Ví von so sánh công nghiệp của LLM"),
    ("sáng quắc như chim ưng", "So sánh rập khuôn"),
    ("nắm chặt nắm đấm", "Cử chỉ gồng cứng shonen"),
    ("siết chặt nắm tay", "Cử chỉ gồng cứng shonen"),
    ("mở bừng mắt", "Phản xạ thức tỉnh rập khuôn"),
    ("run lên lạc đi", "Biểu cảm kích động thái quá"),
    ("hơn ai hết, hắn hiểu rằng", "Cụm chuyển ý triết lý rởm của AI"),
    ("hơn ai hết", "Cụm từ sáo mòn của AI"),
    ("như một lẽ tất nhiên", "Liên từ áp đặt logic của AI"),
    ("thời gian như ngưng đọng", "Ẩn dụ sáo mòn"),
    ("bầu không khí khẩn trương, căng thẳng tột độ", "Văn mẫu kịch bản của AI"),
    ("hừng hực vẻ phấn khích tột cùng", "Cảm xúc cường điệu hóa của AI"),
]

TIMESTAMP_PATTERN = re.compile(
    r"^(?:(?:Bốn|Năm|Sáu|Bảy|Tám|Chín|Mười|Mười một|Mười hai|Mười ba|Mười bốn|Mười lăm|Mười sáu|Mười bảy|Mười tám|Mười chín|Hai mươi|Hai mươi mốt|Hai mươi hai|Hai mươi ba|Hai mươi tư|Một|Hai|Ba|\d{1,2})\s+giờ(?:\s+[a-zà-ỹ0-9]+)*\s+(?:sáng|trưa|chiều|tối|đêm|cùng ngày)[\.:]?)\s*$",
    re.IGNORECASE | re.MULTILINE
)

def split_frontmatter(content: str):
    """Tách frontmatter YAML khỏi thân bài."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", content

def audit_text(text: str, filename: str = ""):
    frontmatter, body = split_frontmatter(text)
    issues = []

    # 1. Kiểm tra In đậm thực thể (**...**)
    bolds = re.findall(r"\*\*([^*]+)\*\*", body)
    if bolds:
        issues.append({
            "type": "ENTITY_BOLD",
            "severity": "CRITICAL",
            "count": len(bolds),
            "details": f"Phát hiện {len(bolds)} cụm từ bị in đậm trong thân bài: {bolds[:5]}..."
        })

    # 2. Kiểm tra Mốc giờ cơ học ngắt đoạn
    timestamps = TIMESTAMP_PATTERN.findall(body)
    if timestamps:
        issues.append({
            "type": "MECHANICAL_TIMESTAMP",
            "severity": "HIGH",
            "count": len(timestamps),
            "details": f"Phát hiện {len(timestamps)} mốc giờ cơ học đứng riêng thành đoạn: {timestamps}"
        })

    # 3. Kiểm tra Sáo ngữ & Cử chỉ LLM
    body_lower = body.lower()
    for phrase, note in CLICHE_PHRASES:
        count = len(re.findall(re.escape(phrase), body_lower))
        if count > 0:
            issues.append({
                "type": "AI_CLICHE_PHRASE",
                "severity": "MEDIUM",
                "phrase": phrase,
                "count": count,
                "details": f"Cụm từ sáo mòn '{phrase}' ({count} lần) — Ghi chú: {note}"
            })

    # 4. Kiểm tra Kết chương hô khẩu hiệu Shonen (!) & Mo-tip "Mới thực sự bắt đầu"
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    if lines:
        last_para = lines[-1].lower()
        if lines[-1].endswith("!"):
            issues.append({
                "type": "SHONEN_EXCLAMATION_ENDING",
                "severity": "HIGH",
                "details": f"Chương kết thúc bằng câu hô khẩu hiệu dấu chấm than (!): '{lines[-1]}'"
            })
        
        beginning_markers = [
            "thật sự bắt đầu", "thực sự bắt đầu", "chính thức bắt đầu", "vừa mới bắt đầu",
            "chỉ mới bắt đầu", "mới chỉ là bắt đầu", "hành trình mới bắt đầu", "bão tố bắt đầu",
            "phong bão bắt đầu", "sóng gió bắt đầu", "chỉ vừa bắt đầu", "mới là bắt đầu"
        ]
        matched_ending = [m for m in beginning_markers if m in last_para]
        if matched_ending:
            issues.append({
                "type": "FORMULAIC_ENDING_MOTIF",
                "severity": "CRITICAL",
                "details": f"Kết chương dập khuôn mo-tip 'Mọi thứ mới thật sự bắt đầu' ({matched_ending}): '{lines[-1][:90]}...'"
            })

        teaser_markers = [
            "sẵn sàng cho", "sẵn sàng bước", "sẵn sàng cùng nhau",
            "thử thách đang chờ", "thử thách phía trước", "thử thách cam go", "những thử thách lớn",
            "hành trình mới đang", "hành trình mới đầy", "chân trời mới đang vẫy",
            "chân trời mới cho hành trình", "tiến vào thử thách", "bước vào thử thách",
            "khởi đầu của một đại", "giương buồm xuất trận", "xuất quân",
            "bước tiếp trên hành trình", "chuẩn bị cho chuyến", "chuẩn bị bước vào",
            "đang chờ đợi phía trước", "đang vẫy gọi", "tiến vào thử thách"
        ]
        matched_teasers = [m for m in teaser_markers if m in last_para]
        if matched_teasers:
            issues.append({
                "type": "FORMULAIC_ENDING_TEASER",
                "severity": "CRITICAL",
                "details": f"Kết chương dập khuôn mo-tip 'Chuẩn bị có thử thách / Hành trình mới' ({matched_teasers}): '{lines[-1][:90]}...'"
            })

    # 4.5. Kiểm tra Mở đầu chương dập khuôn mo-tip "Bây giờ là mấy giờ"
    # Lấy 3 dòng đầu tiên sau tiêu đề chương
    non_header_lines = [l.strip() for l in lines if not l.startswith("#") and not l.startswith("---")]
    if non_header_lines:
        first_few = " ".join(non_header_lines[:3]).lower()
        opening_time_match = re.search(r"\b(?:bốn|năm|sáu|bảy|tám|chín|mười|mười một|mười hai|mười ba|mười bốn|mười lăm|mười sáu|mười bảy|mười tám|mười chín|hai mươi|hai mươi mốt|hai mươi hai|hai mươi ba|hai mươi tư|một|hai|ba|\d{1,2})\s+giờ(?:\s+[^,\.\n]+?)?\s+(?:sáng|trưa|chiều|tối|đêm)", first_few)
        if opening_time_match:
            issues.append({
                "type": "FORMULAIC_OPENING_TIMESTAMP",
                "severity": "CRITICAL",
                "details": f"Mở đầu chương dập khuôn mo-tip 'Bây giờ là mấy giờ': '{non_header_lines[0]}'"
            })

    # 4.6. Kiểm tra Cụm từ "Vận dụng công pháp / Cảnh giới" thô sượng (Stilted Cultivation)
    stilted_cultivation_terms = [
        ("vận dụng công pháp", "Dùng từ sượng, máy móc thay vì miêu tả cảm giác thể chất"),
        ("vận dụng cảnh giới", "Dùng từ sượng, máy móc như thông số game"),
        ("vận hành công pháp", "Văn mẫu convert lặp lại máy móc"),
        ("vận chuyển kình lực", "Cụm từ sáo mòn, thiếu chi tiết cơ bắp gân cốt"),
        ("kích hoạt cảnh giới", "Tư duy gamer/bot, không phải văn học thể đạo"),
        ("dưới sự gia trì của", "Văn mẫu dịch máy game RPG"),
        ("dưới tác dụng của cảnh giới", "Lối hành văn báo cáo khoa học nhầm chỗ"),
        ("uy áp cảnh giới", "Khái niệm sáo mòn tu tiên mạng"),
        ("sức mạnh cảnh giới", "Khái niệm sáo mòn tu tiên mạng"),
        ("tầng thứ cảnh giới", "Khái niệm sáo mòn"),
        ("vận hành kình lực", "Từ ngữ sáo mòn lặp lại"),
    ]
    for term, note in stilted_cultivation_terms:
        count = len(re.findall(re.escape(term), body_lower))
        if count > 0:
            issues.append({
                "type": "STILTED_CULTIVATION_PHRASE",
                "severity": "HIGH",
                "phrase": term,
                "count": count,
                "details": f"Cụm từ tu luyện thô sượng '{term}' ({count} lần) — {note}"
            })

    # 5. Kiểm tra Thoại đọc thông số kỹ thuật (Exposition Dump)
    dialogues = re.findall(r'["“]([^"”]+)["”]', body)
    tech_keywords = ["sợi kevlar", "quang học ngầm sâu", "năm 1996", "âm một ngàn", "hertz", "đầu dò cảm biến"]
    for d in dialogues:
        words = len(d.split())
        matched_kw = [kw for kw in tech_keywords if kw in d.lower()]
        if words > 30 and len(matched_kw) >= 2:
            issues.append({
                "type": "EXPOSITION_DUMP_DIALOGUE",
                "severity": "HIGH",
                "details": f"Thoại dài ({words} từ) nhồi nhét thông số kỹ thuật ({matched_kw}): '{d[:80]}...'"
            })

    return issues

def strip_bolds_from_body(text: str) -> str:
    frontmatter, body = split_frontmatter(text)
    cleaned_body = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    if frontmatter:
        return f"---{frontmatter}---{cleaned_body}"
    return cleaned_body

def find_chapter_file(chapter_num: int):
    target = f"ch_{chapter_num:03d}.md"
    for root, _, files in os.walk(MANUSCRIPT_DIR):
        if target in files:
            return os.path.join(root, target)
    return None

def main():
    parser = argparse.ArgumentParser(description="Audit anti-AI smells in Pha Troi manuscript")
    parser.add_argument("--chapter", nargs="+", type=int, help="Chapter numbers to audit")
    parser.add_argument("--all", action="store_true", help="Audit all chapters")
    parser.add_argument("--fix-bolds", action="store_true", help="Auto remove **bold** tags from text")
    parser.add_argument("--summary-only", action="store_true", help="Only show summary statistics")
    args = parser.parse_args()

    target_files = []
    if args.chapter:
        for ch in args.chapter:
            fpath = find_chapter_file(ch)
            if fpath:
                target_files.append((ch, fpath))
            else:
                print(f"[!] Không tìm thấy file cho Chương {ch}")
    elif args.all:
        for root, _, files in os.walk(MANUSCRIPT_DIR):
            for f in sorted(files):
                if f.startswith("ch_") and f.endswith(".md"):
                    m = re.search(r"ch_(\d+)\.md", f)
                    ch = int(m.group(1)) if m else 0
                    target_files.append((ch, os.path.join(root, f)))
    else:
        print("Vui lòng chỉ định --chapter [số ...] hoặc --all")
        return

    print("=" * 70)
    print(f"  BẮT ĐẦU KIỂM TOÁN MÙI AI CHO {len(target_files)} CHƯƠNG")
    print("=" * 70)

    total_issues_count = 0
    stats_by_type = {}
    chapters_by_type = {}
    for ch, fpath in target_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        if args.fix_bolds:
            new_content = strip_bolds_from_body(content)
            if new_content != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[FIXED] Đã gỡ sạch thẻ in đậm cho Chương {ch}")
                content = new_content

        issues = audit_text(content, fpath)
        total_issues_count += len(issues)

        # Thống kê theo loại
        for iss in issues:
            itype = iss["type"]
            stats_by_type[itype] = stats_by_type.get(itype, 0) + 1
            if itype not in chapters_by_type:
                chapters_by_type[itype] = []
            chapters_by_type[itype].append(ch)

        if not args.summary_only:
            print(f"\n[Chương {ch:03d}] {os.path.basename(fpath)} — {len(issues)} vấn đề phát hiện:")
            if not issues:
                print("  ✓ Hoàn toàn tinh sạch! Không phát hiện mùi AI.")
            else:
                for iss in issues:
                    sev = iss['severity']
                    icon = "[🔴 CRITICAL]" if sev == "CRITICAL" else "[🟡 HIGH]" if sev == "HIGH" else "[⚪ MEDIUM]"
                    print(f"  {icon} {iss['type']}: {iss['details']}")

    print("\n" + "=" * 70)
    print(f"  TỔNG KẾT TOÀN DIỆN {len(target_files)} CHƯƠNG: {total_issues_count} VẤN ĐỀ ĐƯỢC PHÁT HIỆN")
    print("=" * 70)
    for itype, count in sorted(stats_by_type.items(), key=lambda x: x[1], reverse=True):
        affected_chs = len(set(chapters_by_type.get(itype, [])))
        print(f"  * {itype:<30}: {count:>4} lượt vi phạm (trong {affected_chs:>2}/{len(target_files)} chương)")
    print("=" * 70)

if __name__ == "__main__":
    main()
