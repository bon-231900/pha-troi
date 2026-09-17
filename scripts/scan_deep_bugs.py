# -*- coding: utf-8 -*-
"""Deep scanner for potential plot holes, character inconsistencies, and lore bugs."""

import glob
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

files = sorted(glob.glob('manuscript/markdown/**/ch_*.md', recursive=True))

print("="*70)
print("1. ĐỊA CHỈ PHÒNG TRỌ CỦA MINH AN QUA CÁC CHƯƠNG")
print("="*70)
room_addresses = {}
for fpath in files:
    ch = int(re.search(r'ch_(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    streets = re.findall(r'(phòng trọ [^\.\n,]{5,50}|đường [A-ZÀ-Ỹa-ỹ\s0-9]{3,25})', text, re.IGNORECASE)
    matched = []
    for s in streets:
        s_lower = s.lower()
        if any(k in s_lower for k in ['nơ trang long', 'ung văn khiêm', 'bình thạnh', 'hàng xanh', 'phòng trọ']):
            matched.append(s.strip())
    if matched:
        room_addresses[ch] = matched[:2]

for ch, addrs in room_addresses.items():
    if ch in [1, 2, 5, 10, 20, 30, 40, 50, 55, 60, 66, 69]:
        print(f"Ch {ch:02d}: {addrs}")

print("\n" + "="*70)
print("2. CÁCH XƯNG HÔ GIỮA TUẤN VÀ MINH AN")
print("="*70)
for fpath in files:
    ch = int(re.search(r'ch_(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    # Find lines where Tuan addresses Minh An
    for l in text.splitlines():
        if 'Tuấn' in l and any(k in l for k in ['báo cáo', 'kính gửi', 'em An', 'anh An', 'cậu An', 'Minh An, em', 'Giám đốc']):
            if len(l.strip()) < 150:
                print(f"Ch {ch:02d}: {l.strip()}")

print("\n" + "="*70)
print("3. VŨ KHÍ: NGUỒN GỐC & QUÁ TRÌNH NÂNG CẤP ĐOẢN CÔN & ĐOẢN ĐAO")
print("="*70)
weapon_mentions = {}
for fpath in files:
    ch = int(re.search(r'ch_(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    con = re.findall(r'(\bđoản côn\b|\bhắc thiết đoản côn\b)', text, re.IGNORECASE)
    dao = re.findall(r'(\btrấn thủy đoản đao\b|\bđoản đao\b)', text, re.IGNORECASE)
    if con or dao:
        weapon_mentions[ch] = (len(con), len(dao))

print(f"Các chương xuất hiện đoản côn: {[ch for ch, v in weapon_mentions.items() if v[0] > 0]}")
print(f"Các chương xuất hiện đoản đao: {[ch for ch, v in weapon_mentions.items() if v[1] > 0]}")

print("\n" + "="*70)
print("4. NHÂN VẬT LÊ BÁ KHIÊM — XUẤT HIỆN Ở ĐÂU VÀ CÓ BỊ QUÊN KHÔNG?")
print("="*70)
khiem_mentions = []
for fpath in files:
    ch = int(re.search(r'ch_(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    if 'khiêm' in text.lower() or 'lê bá khiêm' in text.lower():
        khiem_mentions.append(ch)
print(f"Lê Bá Khiêm xuất hiện tại các chương: {khiem_mentions}")

print("\n" + "="*70)
print("5. HỌC VỊ & DANH XƯNG CỦA TRỊNH HOÀI NAM (Tiến sĩ vs Giáo sư vs Viện trưởng)")
print("="*70)
nam_titles = {}
for fpath in files:
    ch = int(re.search(r'ch_(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    ts = len(re.findall(r'tiến sĩ (?:trịnh hoài )?nam', text, re.IGNORECASE))
    gs = len(re.findall(r'giáo sư (?:trịnh hoài )?nam', text, re.IGNORECASE))
    vt = len(re.findall(r'viện trưởng (?:trịnh hoài )?nam', text, re.IGNORECASE))
    if ts or gs or vt:
        nam_titles[ch] = {'Tiến sĩ': ts, 'Giáo sư': gs, 'Viện trưởng': vt}

for ch, titles in list(nam_titles.items())[:15]:
    print(f"Ch {ch:02d}: {titles}")
for ch, titles in list(nam_titles.items())[-10:]:
    print(f"Ch {ch:02d}: {titles}")
