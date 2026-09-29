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

chapters = {}
for fpath in files:
    ch_num = int(re.search(r"ch_(\d+)", fpath).group(1))
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    body = content.split("---", 2)[-1] if "---" in content else content
    chapters[ch_num] = {
        "num": ch_num,
        "path": fpath,
        "text": body,
        "paras": [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    }

print("Loaded 96 chapters.")

# Let's search for all questions asked by Minh An or Lâm Tịch that suggest an unresolved task:
# e.g., "phải tìm", "cần phải", "phải đến", "chưa rõ", "rốt cuộc là", "ai là người", "mật mã"
# And check whether any tasks stated in chapter N were dropped in N+1/N+2.

TASK_PATTERNS = [
    r'(?:phải nhanh chóng|cần phải điều tra|sẽ đích thân đến|phải đến|sẽ đến|hẹn vào|chuẩn bị đến)\s+([^,.;\n]{5,50})',
]

print("\n=== CÁC Ý ĐỊNH / NHIỆM VỤ ĐƯỢC NÊU RA ===")
for ch in range(1, 96):
    text = chapters[ch]["text"]
    for pat in TASK_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            target = m.group(1).strip()
            # Check if target is mentioned in next 3 chapters
            next_3_text = " ".join([chapters[c]["text"] for c in range(ch+1, min(97, ch+4))])
            target_words = [w for w in re.split(r'\W+', target) if len(w) > 3]
            if target_words:
                found = any(w.lower() in next_3_text.lower() for w in target_words)
                if not found:
                    print(f"Ch {ch:02d}: '{m.group(0)}' -> KHÔNG THẤY nhắc trong 3 chương tiếp theo!")

# Check for specific items mentioned in earlier chapters that were never mentioned again
print("\n=== KIỂM TRA ĐỒ VẬT MỒ CÔI NỘI DUNG (DROPPED PROPS) ===")
props_to_check = [
    ("trâm ngọc", "Cố Hồn Trâm / trâm cài"),
    ("chiếc bật lửa Zippo", "bật lửa Zippo của cha"),
    ("thanh đục", "thanh đục rèn ở Hóc Môn"),
    ("bình rượu thuốc", "rượu thuốc Đoán Cốt"),
    ("lệnh bài", "lệnh bài Thiết Vệ Tam"),
    ("cuộn da dê", "da dê Cửu U"),
    ("hộp đồng", "hộp đồng mai rùa"),
    ("chiếc đinh neo", "đinh neo âm cương"),
    ("tấm bạt dứa", "bạt dứa gói đồ"),
    ("túi vải nhung", "vải nhung bọc thạch"),
    ("ống nhôm", "ống nhôm dã chiến 1996"),
    ("mặt dây chuyền", "dây chuyền"),
    ("sổ tay", "sổ tay trắc địa"),
]

for kw, desc in props_to_check:
    occurrences = [ch for ch, d in chapters.items() if kw.lower() in d["text"].lower()]
    print(f"Prop '{desc}' ({kw}): xuất hiện ở {len(occurrences)} chương: {occurrences}")
