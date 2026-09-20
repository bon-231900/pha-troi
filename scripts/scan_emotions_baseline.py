# -*- coding: utf-8 -*-
"""Batch scan recent chapters to establish emotional baseline in reader_emotional_ledger."""

import os
import sys
import glob
import sqlite3

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.engines.emotion_dopamine_engine import EmotionDopamineEngine
from system.core.config import MANUSCRIPT_MD_DIR

def run_scan():
    eng = EmotionDopamineEngine()
    ch_files = sorted(glob.glob(os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", "ch_*.md")))
    print(f"[*] Tìm thấy {len(ch_files)} chương trong Arc 2 để quét cảm xúc...")

    for fpath in ch_files:
        fname = os.path.basename(fpath)
        ch_num = int(fname.split("_")[1].split(".")[0])
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
        res = eng.analyze_text(ch_num, text, arc_id="arc_02")
        print(f"  -> Chương {ch_num:03d}: Pathos={res['pathos_score']:.2f} | Dopamine={res['dopamine_score']:.2f} | Grounding={res['grounding_score']:.2f} | {res['pacing_assessment']}")

    print("\n[*] ĐÁNH GIÁ TỔNG QUAN TOÀN ARC 2:")
    audit = eng.audit_arc_pacing("arc_02")
    print(f"  - Tổng số chương đã quét: {audit['total_chapters_logged']}")
    print(f"  - Điểm Bi Thương trung bình (Pathos Avg): {audit['avg_pathos']:.2f}/10.0")
    print(f"  - Điểm Thăng Hoa trung bình (Dopamine Avg): {audit['avg_dopamine']:.2f}/10.0")
    print(f"  - Điểm Đời Thường trung bình (Grounding Avg): {audit['avg_grounding']:.2f}/10.0")
    print("  - Cảnh báo nhịp độ:")
    for w in audit['warnings']:
        print(f"    [!] {w}")

if __name__ == "__main__":
    run_scan()
