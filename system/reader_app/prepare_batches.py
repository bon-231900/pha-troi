# -*- coding: utf-8 -*-
import os
import json

DIST_DIR = r"d:\tieu-thuyet\system\reader_app\dist"
SCRATCH_DIR = r"C:\Users\ADMIN\.gemini\antigravity\brain\27f361fe-4c12-45ac-8f78-bc13847be80a\scratch"
os.makedirs(SCRATCH_DIR, exist_ok=True)

# Batch 1: Core files + Chapters 1 to 15
batch1_files = []
for fname in ["index.html", "manifest.json", "sw.js", "icon.svg"]:
    with open(os.path.join(DIST_DIR, fname), "r", encoding="utf-8") as f:
        batch1_files.append({"path": fname, "content": f.read()})

with open(os.path.join(DIST_DIR, "data", "chapters.json"), "r", encoding="utf-8") as f:
    batch1_files.append({"path": "data/chapters.json", "content": f.read()})

for ch in range(1, 16):
    fpath = os.path.join(DIST_DIR, "data", f"chapter_{ch}.json")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            batch1_files.append({"path": f"data/chapter_{ch}.json", "content": f.read()})

with open(os.path.join(SCRATCH_DIR, "batch1.json"), "w", encoding="utf-8") as out:
    json.dump(batch1_files, out, ensure_ascii=False)

print(f"Batch 1 prepared: {len(batch1_files)} files")

# Batch 2: Chapters 16 to 30
batch2_files = []
for ch in range(16, 31):
    fpath = os.path.join(DIST_DIR, "data", f"chapter_{ch}.json")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            batch2_files.append({"path": f"data/chapter_{ch}.json", "content": f.read()})

with open(os.path.join(SCRATCH_DIR, "batch2.json"), "w", encoding="utf-8") as out:
    json.dump(batch2_files, out, ensure_ascii=False)

print(f"Batch 2 prepared: {len(batch2_files)} files")

# Batch 3: Chapters 31 to 46
batch3_files = []
for ch in range(31, 47):
    fpath = os.path.join(DIST_DIR, "data", f"chapter_{ch}.json")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            batch3_files.append({"path": f"data/chapter_{ch}.json", "content": f.read()})

with open(os.path.join(SCRATCH_DIR, "batch3.json"), "w", encoding="utf-8") as out:
    json.dump(batch3_files, out, ensure_ascii=False)

print(f"Batch 3 prepared: {len(batch3_files)} files")
