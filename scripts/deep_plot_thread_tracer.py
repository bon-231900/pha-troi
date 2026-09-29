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
        "lines": body.splitlines()
    }

print("Loaded 96 chapters.")

# Specific investigations:
# 1. Investigate the 12 stakes (Thủy Môn Thập Nhị Tiêu):
# How was each stake handled? Did Minh An keep an artifact from each, or seal it on site?
stakes_info = [
    "Lò Gốm", "Phú Định", "Mũi Đèn Đỏ", "Cầu Mống", "Ba Son", 
    "Hải Uyên", "Chứa Chan", "Trấn Ba", "Soài Rạp", "Ba Lai", "Cổ Chiên", "Đất Mũi"
]

print("\n=== 1. THỦY MÔN THẬP NHỊ TIÊU CHECK ===")
for stake in stakes_info:
    found_in = [ch for ch, data in chapters.items() if stake.lower() in data["text"].lower()]
    print(f"  * {stake}: xuất hiện trong {len(found_in)} chương (từ Ch {min(found_in) if found_in else 'N/A'} đến Ch {max(found_in) if found_in else 'N/A'})")

# 2. Key Characters tracking:
# Who are the recurring vs one-off characters?
characters_to_trace = [
    "Ba Khiêm", "Bác Ba", "Lê Gia",
    "Trịnh Hoài Nam", "Tiến sĩ Nam",
    "Tuấn", "Kỹ sư Tuấn",
    "Phan Thanh Tùng", "Chú Tùng",
    "Trần Văn Hùng", "Đại úy Hùng", "Thuyền trưởng Hùng",
    "Trần Vũ Cương", "thợ lặn Cương",
    "Sáu Kiên", "Bác Sáu",
    "Bảy Thâm", "tiệm đồ cổ",
    "Thầy Cảnh", "Vạn Phát",
    "Tạ Lôi",
    "Trần Bảy", "Bảy Thép",
    "Bành Đại Lực",
    "Trần Văn Định", "Giáo sư Định",
    "Già Y Dăm", "Y Dăm", "Y Krông",
    "Trần Vũ Hải Yến", "Hải Yến",
    "Bạch Y Thần Nữ", "Lâm Tịch"
]

print("\n=== 2. NHÂN VẬT & ĐỊA ĐIỂM QUAN TRỌNG ===")
for char in characters_to_trace:
    found_in = [ch for ch, data in chapters.items() if char.lower() in data["text"].lower()]
    print(f"  * {char:<22}: {len(found_in):2d} chương -> {found_in[:10]}{'...' if len(found_in)>10 else ''}")

# 3. Check for items mentioned in backpack / inventory across chapters:
backpack_items = [
    "Hắc Thiết Đoản Côn",
    "Trấn Thủy Đoản Đao",
    "Hắc Thủy Huyền Thạch",
    "Định Hải Huyền Châu",
    "Trấn Giang Huyền Tỷ",
    "Tỏa Long Huyền Tỷ",
    "Thanh Long Lân Kiếm",
    "Mộc Hoàng Lôi Tâm Thạch",
    "Sổ Tay Trắc Địa",
    "chiếc bật lửa Zippo",
    "hộp đồng",
    "ống nhôm",
    "bản đồ 1996"
]

print("\n=== 3. VẬT PHẨM TRONG BA LÔ / BẢO VẬT ===")
for it in backpack_items:
    found_in = [ch for ch, data in chapters.items() if it.lower() in data["text"].lower()]
    print(f"  * {it:<26}: {len(found_in):2d} chương -> {found_in[:12]}{'...' if len(found_in)>12 else ''}")
