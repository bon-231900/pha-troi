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
    r"^(?:Bốn|Năm|Sáu|Bảy|Tám|Chín|Mười|Mười một|Mười hai|Một|Hai|Ba)\s+giờ(?:\s+\w+)*\s+(?:sáng|trưa|chiều|tối|đêm|cùng ngày)[\.:]?\s*$",
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

    # 4. Kiểm tra Kết chương hô khẩu hiệu Shonen (!)
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    if lines:
        last_line = lines[-1]
        if last_line.endswith("!"):
            issues.append({
                "type": "SHONEN_EXCLAMATION_ENDING",
                "severity": "HIGH",
                "details": f"Chương kết thúc bằng câu hô khẩu hiệu dấu chấm than (!): '{last_line}'"
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

        print(f"\n[Chương {ch:03d}] {os.path.basename(fpath)} — {len(issues)} vấn đề phát hiện:")
        if not issues:
            print("  ✓ Hoàn toàn tinh sạch! Không phát hiện mùi AI.")
        else:
            for iss in issues:
                sev = iss['severity']
                icon = "[🔴 CRITICAL]" if sev == "CRITICAL" else "[🟡 HIGH]" if sev == "HIGH" else "[⚪ MEDIUM]"
                print(f"  {icon} {iss['type']}: {iss['details']}")

    print("\n" + "=" * 70)
    print(f"  TỔNG KẾT: {total_issues_count} vấn đề mùi AI cần xử lý.")
    print("=" * 70)

if __name__ == "__main__":
    main()
