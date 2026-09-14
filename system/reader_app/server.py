# -*- coding: utf-8 -*-
import os
import re
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import markdown
import qrcode
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

BASE_DIR = r"d:\tieu-thuyet"
MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript", "markdown", "volume_01", "arc_01")
STATIC_DIR = os.path.join(BASE_DIR, "system", "reader_app", "static")

app = FastAPI(title="Phá Trời Reader Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

def get_chapter_files():
    if not os.path.exists(MANUSCRIPT_DIR):
        return []
    files = sorted([f for f in os.listdir(MANUSCRIPT_DIR) if f.endswith(".md") and f.startswith("ch_")])
    return files

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
    
    # Bỏ dòng # Tiêu đề khỏi body nếu cần
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

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/manifest.json")
def serve_manifest():
    return FileResponse(os.path.join(STATIC_DIR, "manifest.json"))

@app.get("/api/chapters")
def api_chapters():
    files = get_chapter_files()
    chapters = []
    for f in files:
        path = os.path.join(MANUSCRIPT_DIR, f)
        info = parse_chapter_file(path)
        chapters.append({
            "chapter": info["chapter"],
            "title": info["title"],
            "volume": info["volume"],
            "arc": info["arc"],
            "word_count": info["word_count"],
            "date": info["date"]
        })
    return {"total": len(chapters), "chapters": chapters}

@app.get("/api/chapter/{chapter_num}")
def api_chapter(chapter_num: int):
    filename = f"ch_{chapter_num:03d}.md"
    path = os.path.join(MANUSCRIPT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Không tìm thấy chương này")
    return parse_chapter_file(path)

def print_qr(url):
    print("\n" + "="*50)
    print("  ỨNG DỤNG ĐỌC TRUYỆN NỘI BỘ PHÁ TRỜI ĐÃ SẴN SÀNG!")
    print("="*50)
    print(f"\n-> ĐỊA CHỈ TRUY CẬP TRÊN ĐIỆN THOẠI:")
    print(f"   {url}\n")
    print("-> HOẶC QUÉT MÃ QR DƯỚI ĐÂY BẰNG CAMERA ĐIỆN THOẠI:")
    try:
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make()
        qr.print_ascii(invert=True)
    except Exception:
        pass
    print("="*50 + "\n")

if __name__ == "__main__":
    local_ip = "192.168.1.102"
    port = 8888
    mobile_url = f"http://{local_ip}:{port}"
    print_qr(mobile_url)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
