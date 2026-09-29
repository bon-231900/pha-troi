# -*- coding: utf-8 -*-
"""
audit_orphan_threads.py:
Comprehensive scanner to detect:
1. Items/artifacts picked up or put into backpack that are never mentioned again.
2. Characters introduced with dialogue or confrontation that disappear without closure.
3. Appointments/deadlines mentioned for "ngày mai / tối mai / sáng mai" that are ignored.
4. Mysterious clues/notes/intercepts that evaporate.
"""
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
    paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    chapters[ch_num] = {
        "num": ch_num,
        "path": fpath,
        "content": body,
        "paras": paras
    }

print(f"[+] Đã tải toàn bộ {len(chapters)} chương.")

# 1. SCAN FOR ACQUIRED ITEMS (nhặt được, thu được, cất vào ba lô, đưa cho tôi, trao cho tôi, tìm thấy...)
ITEM_PATTERNS = [
    r'(?:nhặt được|thu được|cất vào ba lô|bỏ vào ba lô|trao cho tôi|đưa cho tôi|tìm thấy|tịch thu từ|đoạt được)\s+([^,.;\n]{5,50})',
    r'(?:thanh|khối|viên|tấm|cuốn|chiếc|mảnh|hộp|lọ|lá|bức)\s+([A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ\s]+)',
]

acquired_items = []
for ch_num, ch_data in chapters.items():
    text = ch_data["content"]
    for pat in ITEM_PATTERNS:
        for m in re.finditer(pat, text):
            item_name = m.group(1).strip()
            item_name = re.sub(r'^(một|chiếc|thanh|khối|viên|tấm|cuốn|chiếc|mảnh|hộp|lọ|bức)\s+', '', item_name, flags=re.IGNORECASE).strip()
            if len(item_name) >= 4 and len(item_name) <= 40:
                generic = ["người", "căn phòng", "thời gian", "không gian", "bước chân", "con đường", "thành phố", "giọng nói", "cảm giác", "hơi thở", "kình lực", "cương huyết"]
                if not any(g in item_name.lower() for g in generic):
                    acquired_items.append((ch_num, item_name, m.group(0)))

print(f"[+] Tìm thấy {len(acquired_items)} vật phẩm/chi tiết tiềm năng được tiếp nhận qua 96 chương.")

orphan_items = {}
for ch_num, item_name, raw_phrase in acquired_items:
    words = [w for w in re.split(r'\W+', item_name) if len(w) > 2]
    if len(words) < 2:
        continue
    core_pattern = r'\b' + r'\s+'.join([re.escape(w) for w in words[:3]])
    
    occurrences = []
    for other_ch in range(1, 97):
        if re.search(core_pattern, chapters[other_ch]["content"], re.IGNORECASE):
            occurrences.append(other_ch)
    
    if occurrences == [ch_num]:
        key = (ch_num, item_name)
        if key not in orphan_items:
            orphan_items[key] = {
                "ch": ch_num,
                "item": item_name,
                "phrase": raw_phrase,
                "occurrences": occurrences
            }

print(f"\n[!] CẢNH BÁO: Phát hiện {len(orphan_items)} vật phẩm CHỈ XUẤT HIỆN DUY NHẤT 1 LẦN trong chương được nhắc đến:")
for (ch, item), data in list(orphan_items.items())[:35]:
    print(f"  - Chương {ch:02d}: '{item}' (Ngữ cảnh: '{data['phrase']}')")

# 2. SCAN FOR UNRESOLVED PROMISES / APPOINTMENTS ("hẹn", "tối mai", "sáng mai", "ngày mai", "giờ này ngày mai")
APPOINTMENT_PATTERNS = [
    r'(?:hẹn gặp|hẹn lúc|sáng mai|tối mai|đêm mai|ngày mai chúng ta|ngày mai tôi sẽ|tám giờ sáng mai|chín giờ sáng mai)\s+([^.\n]{10,80})',
]

print(f"\n[+] Rà soát các cuộc hẹn / lời hứa hẹn mốc thời gian...")
for ch_num in range(1, 96):
    text = chapters[ch_num]["content"]
    next_text = chapters[ch_num + 1]["content"]
    for pat in APPOINTMENT_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            match_str = m.group(0).strip()
            app_words = [w for w in re.split(r'\W+', m.group(1)) if len(w) > 3]
            acknowledged = any(w.lower() in next_text.lower() for w in app_words[:3]) if app_words else False
            if not acknowledged and ("mai" in match_str.lower() or "hẹn" in match_str.lower()):
                print(f"  - Nghi vấn Ch {ch_num:02d} -> Ch {ch_num+1:02d}: '{match_str}'")

# 3. SCAN FOR NAMED CHARACTERS APPEARING ONLY IN 1-2 CHAPTERS
print(f"\n[+] Rà soát các nhân vật xuất hiện chớp nhoáng rồi mất tích...")
CHAR_PATTERN = r'\b(?:Ông|Bác|Chú|Anh|Chị|Cô|Tên|Gã|Thầy|Đại úy|Tiến sĩ|Giáo sư)\s+([A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+(?:\s+[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+){1,2})'

characters = {}
for ch_num, ch_data in chapters.items():
    for m in re.finditer(CHAR_PATTERN, ch_data["content"]):
        name = m.group(1).strip()
        if len(name.split()) >= 2 and len(name) < 30:
            if name in ["Nguyễn Minh An", "Minh An", "Lâm Tịch", "Trịnh Hoài Nam", "Hoài Nam", "Trần Vũ Cương", "Phan Thanh Tùng", "Thanh Tùng", "Trần Vũ Hải Yến", "Hải Yến", "Tạ Lôi", "Trần Bảy", "Bành Đại Lực"]:
                continue
            if name not in characters:
                characters[name] = []
            if ch_num not in characters[name]:
                characters[name].append(ch_num)

single_appearance_chars = {k: v for k, v in characters.items() if len(v) == 1}
print(f"[!] Phát hiện {len(single_appearance_chars)} nhân vật có tên riêng chỉ xuất hiện đúng 1 chương duy nhất:")
for name, chs in list(single_appearance_chars.items())[:30]:
    print(f"  - '{name}' chỉ xuất hiện ở Chương {chs[0]:02d}")
