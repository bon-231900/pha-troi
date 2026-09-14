# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import shutil
import markdown

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"d:\tieu-thuyet"
MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript", "markdown", "volume_01", "arc_01")
STATIC_SRC_DIR = os.path.join(BASE_DIR, "system", "reader_app", "static")
DIST_DIR = os.path.join(BASE_DIR, "system", "reader_app", "dist")

def parse_chapter_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()

    meta = {}
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1].strip()
            body = parts[2].strip()
            for line in fm.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')

    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1) if title_match else meta.get("title", "Chương không tiêu đề")
    
    # Remove # Title from markdown body
    body_clean = re.sub(r"^#\s+.+$\n*", "", body, count=1, flags=re.MULTILINE)

    html_content = markdown.markdown(body_clean, extensions=["extra", "nl2br"])
    return {
        "chapter": int(meta.get("chapter", 1)),
        "title": title,
        "volume": int(meta.get("volume", 1)),
        "arc": int(meta.get("arc", 1)),
        "word_count": int(meta.get("word_count", len(body.split()))),
        "date": meta.get("date", "2026-10-07"),
        "location": meta.get("location", ""),
        "html": html_content
    }

def build():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)
    data_dir = os.path.join(DIST_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. Read all chapters
    files = sorted([f for f in os.listdir(MANUSCRIPT_DIR) if f.endswith(".md") and f.startswith("ch_")])
    chapters_index = []
    
    total_words = 0
    for f in files:
        path = os.path.join(MANUSCRIPT_DIR, f)
        info = parse_chapter_file(path)
        total_words += info["word_count"]
        
        # Save individual chapter JSON
        ch_json_path = os.path.join(data_dir, f"chapter_{info['chapter']}.json")
        with open(ch_json_path, "w", encoding="utf-8") as out:
            json.dump(info, out, ensure_ascii=False, indent=2)
            
        chapters_index.append({
            "chapter": info["chapter"],
            "title": info["title"],
            "volume": info["volume"],
            "arc": info["arc"],
            "word_count": info["word_count"],
            "date": info["date"],
            "location": info["location"]
        })

    # Save chapters index
    index_data = {
        "title": "Phá Trời (Phá Toái Thần Hoang)",
        "author": "An Bình",
        "total": len(chapters_index),
        "total_words": total_words,
        "updated_at": "2026-09-15T00:00:00+07:00",
        "chapters": chapters_index
    }
    with open(os.path.join(data_dir, "chapters.json"), "w", encoding="utf-8") as out:
        json.dump(index_data, out, ensure_ascii=False, indent=2)

    # 2. Copy static assets
    for item in ["icon.svg", "manifest.json"]:
        src = os.path.join(STATIC_SRC_DIR, item)
        dst = os.path.join(DIST_DIR, item)
        shutil.copy2(src, dst)

    print(f"[Build] Đã biên dịch {len(chapters_index)} chương ({total_words:,} từ) vào {DIST_DIR}")
    return len(chapters_index), total_words

if __name__ == "__main__":
    build()
