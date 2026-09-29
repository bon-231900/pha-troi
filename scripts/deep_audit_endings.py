# -*- coding: utf-8 -*-
import glob
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet\manuscript\markdown"
files = glob.glob(os.path.join(BASE_DIR, "**", "ch_*.md"), recursive=True)
files = sorted(files, key=lambda p: int(re.search(r"ch_(\d+)", p).group(1)))

report_lines = []

CLIFF_TRIGGERS = [
    "bỗng", "đột nhiên", "bất thần", "nhưng ngay khi", "ngay khoảnh khắc",
    "ai đó", "bóng người", "đốm sáng", "tiếng gõ", "san hô", "tọa độ",
    "mảnh giấy", "phong bì", "tin nhắn", "cuộc gọi", "chuông reo",
    "tiếng nổ", "lao tới", "xuất hiện", "nhìn thấy", "kinh hoàng", "chết lặng",
    "không thể ngờ", "và rồi", "chính là"
]

report_lines.append("# BÁO CÁO TOÀN DIỆN: RÀ SOÁT TẤT CẢ CÁC ĐIỂM NỐI KẾT CHƯƠNG (SEAMS 1 -> 96)\n")

for i in range(len(files) - 1):
    f1, f2 = files[i], files[i+1]
    ch1 = int(re.search(r"ch_(\d+)", f1).group(1))
    ch2 = int(re.search(r"ch_(\d+)", f2).group(1))
    if ch2 != ch1 + 1:
        continue

    with open(f1, "r", encoding="utf-8") as f:
        raw1 = f.read()
    with open(f2, "r", encoding="utf-8") as f:
        raw2 = f.read()

    body1 = raw1.split("---", 2)[-1] if "---" in raw1 else raw1
    body2 = raw2.split("---", 2)[-1] if "---" in raw2 else raw2

    # Extract title
    t1_match = re.search(r"^#\s+Chương\s+\d+:\s*(.*)", body1, re.MULTILINE)
    t1 = t1_match.group(1).strip() if t1_match else ""
    t2_match = re.search(r"^#\s+Chương\s+\d+:\s*(.*)", body2, re.MULTILINE)
    t2 = t2_match.group(1).strip() if t2_match else ""

    p1 = [p.strip() for p in body1.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    p2 = [p.strip() for p in body2.split("\n\n") if p.strip() and not p.strip().startswith("#")]

    last_p1 = p1[-1] if p1 else ""
    prev_p1 = p1[-2] if len(p1) >= 2 else ""
    first_p2 = p2[0] if p2 else ""
    second_p2 = p2[1] if len(p2) >= 2 else ""

    # Check triggers
    matched_triggers = [w for w in CLIFF_TRIGGERS if w in last_p1.lower()]

    report_lines.append(f"## SEAM {ch1:02d} -> {ch2:02d}: [{t1}] ---> [{t2}]")
    if matched_triggers:
        report_lines.append(f"**CẢNH BÁO MÓC CÂU**: Phát hiện từ khóa giật gân/bất thường: `{', '.join(matched_triggers)}`")
    
    report_lines.append(f"**Cuối chương {ch1}:**\n> {last_p1}\n")
    report_lines.append(f"**Đầu chương {ch2}:**\n> {first_p2}\n")
    report_lines.append("-" * 60 + "\n")

out_path = r"d:\tieu-thuyet\reports\seam_audit_1_to_96.md"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"Đã xuất báo cáo chi tiết toàn bộ 95 điểm nối vào: {out_path}")
