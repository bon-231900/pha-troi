# -*- coding: utf-8 -*-
"""Comprehensive audit of all 70 chapters of Phá Trời Novel OS."""

import os
import sys
import glob
import re
import json

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR
from system.engines.canon_engine import CanonEngine
from system.engines.critique_engine import CritiqueEngine

def audit_all_chapters():
    canon_eng = CanonEngine(DB_PATH)
    critique_eng = CritiqueEngine(DB_PATH)

    files = sorted(glob.glob(os.path.join(MANUSCRIPT_MD_DIR, "**", "ch_*.md"), recursive=True))
    print(f"[*] Tìm thấy tổng cộng {len(files)} tệp chương bản thảo Markdown.")

    results = []
    
    META_WORDS = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"]
    
    NAME_TYPOS = {
        "Minh Ánh": "Nguyễn Minh An",
        "Minh Ang": "Nguyễn Minh An",
        "Lâm Tịnh": "Lâm Tịch"
    }

    for fpath in files:
        fname = os.path.basename(fpath)
        m = re.search(r"ch_(\d+)\.md", fname)
        ch_num = int(m.group(1)) if m else 0

        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        word_count = len(text.split())
        lower_text = text.lower()

        # 1. Meta-words check
        meta_found = {}
        for mw in META_WORDS:
            matches = re.findall(rf"\b{mw}\b", lower_text)
            if matches:
                meta_found[mw] = len(matches)

        # 2. Typos check
        typos_found = {}
        for typo, correct in NAME_TYPOS.items():
            if typo.lower() in lower_text:
                typos_found[typo] = correct

        # 3. Canon forbidden assumptions
        canon_violations = canon_eng.validate_text_for_forbidden_assumptions(text)

        # 4. Cheap cliffhangers
        cliffhangers = [c for c in critique_eng.cheap_cliffhangers if c in lower_text]

        # 5. Sensitive explosive keywords
        sensitive_found = [sw for sw in ["thuốc nổ", "bom", "kíp nổ", "cài bom", "đánh sập"] if sw in lower_text]

        results.append({
            "chapter": ch_num,
            "filename": fname,
            "path": fpath,
            "word_count": word_count,
            "meta_found": meta_found,
            "typos_found": typos_found,
            "canon_violations": canon_violations,
            "cliffhangers": cliffhangers,
            "sensitive_found": sensitive_found
        })

    # Summary Report
    print("\n" + "="*80)
    print("                    BÁO CÁO KIỂM TOÁN TOÀN BỘ 70 CHƯƠNG")
    print("="*80)

    total_words = sum(r["word_count"] for r in results)
    print(f"Tổng số chương: {len(results)}")
    print(f"Tổng số từ: {total_words:,} từ (Trung bình: {total_words//len(results)} từ/chương)")

    # Chapters with word count < 2000 or > 4000
    abnormal_lengths = [r for r in results if r["word_count"] < 2000 or r["word_count"] > 4000]
    print(f"\n1. Độ dài bất thường (< 2.000 hoặc > 4.000 từ): {len(abnormal_lengths)} chương")
    for ab in abnormal_lengths:
        print(f"   - Chương {ab['chapter']:02d}: {ab['word_count']} từ")

    # Meta-words / RULE-07 breakdown
    chapters_with_meta = [r for r in results if r["meta_found"]]
    print(f"\n2. Từ ngữ Meta (RULE-07): {len(chapters_with_meta)} chương phát hiện")
    for cm in chapters_with_meta:
        print(f"   - Chương {cm['chapter']:02d}: {cm['meta_found']}")

    # Name typos
    chapters_with_typos = [r for r in results if r["typos_found"]]
    print(f"\n3. Lỗi chính tả tên nhân vật: {len(chapters_with_typos)} chương phát hiện")
    for ct in chapters_with_typos:
        print(f"   - Chương {ct['chapter']:02d}: {ct['typos_found']}")

    # Canon violations
    chapters_with_canon = [r for r in results if r["canon_violations"]]
    print(f"\n4. Vi phạm Canon (Suy diễn cấm kỵ): {len(chapters_with_canon)} chương phát hiện")
    for cc in chapters_with_canon:
        print(f"   - Chương {cc['chapter']:02d}: {cc['canon_violations']}")

    # Cheap cliffhangers
    chapters_with_cliff = [r for r in results if r["cliffhangers"]]
    print(f"\n5. Sáo ngữ giật gân rẻ tiền (Cheap Cliffhangers): {len(chapters_with_cliff)} chương phát hiện")
    for cf in chapters_with_cliff:
        print(f"   - Chương {cf['chapter']:02d}: {cf['cliffhangers']}")

    # Sensitive explosive keywords
    chapters_with_sensitive = [r for r in results if r["sensitive_found"]]
    print(f"\n6. Từ khóa nhạy cảm vũ khí nổ: {len(chapters_with_sensitive)} chương phát hiện")
    for cs in chapters_with_sensitive:
        print(f"   - Chương {cs['chapter']:02d}: {cs['sensitive_found']}")

    # Save to json report
    report_file = os.path.join(BASE_DIR, "state", "manuscript_audit_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_chapters": len(results),
            "total_words": total_words,
            "chapters": results
        }, f, ensure_ascii=False, indent=2)
    print(f"\n[+] Đã lưu báo cáo chi tiết vào: {report_file}")

if __name__ == "__main__":
    audit_all_chapters()
