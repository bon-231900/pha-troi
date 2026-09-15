# -*- coding: utf-8 -*-
"""
NovelOS — Trình biên dịch Web Reader PWA cao cấp cho tiểu thuyết 'Phá Trời' (v2.3)
Phiên bản Clean Slugs Chuẩn SEO & Trải Nghiệm Đọc Chuyên Sâu:
- Hoàn toàn loại bỏ dấu '#' trong URL các chương
- Mỗi chương có một đường dẫn tĩnh chuẩn: /chuong-1/, /chuong-2/, ..., /chuong-58/
- Bấm F5 tải lại trang không bao giờ bị lỗi 404 trên GitHub Pages
- Nội dung chương được Render sẵn 100% (SSG) giúp tải tức thì, không bị giật trang (0 FOUC)
- Tương thích ngược tuyệt đối: tự động chuyển hướng các liên kết cũ có '#' hoặc '?chuong='
- Tích hợp 404.html chuyển hướng thông minh
- Tự động lưu tiến độ vào localStorage khi độc giả truy cập bất kỳ chương nào
- Tùy chỉnh giao diện: 4 Themes, 3 mức Chiều rộng (640 / 760 / 900px), 3 mức Giãn dòng (1.65 / 1.85 / 2.1)
- Âm thanh mưa đêm Sài Gòn Web Audio API (Mặc định Tắt)
"""
import os
import re
import sys
import json
import shutil
import markdown
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.getenv("NOVEL_OS_ROOT", str(Path(__file__).resolve().parent.parent.parent))
DIST_DIR = os.path.join(BASE_DIR, "system", "reader_app", "dist")
STATIC_SRC_DIR = os.path.join(BASE_DIR, "system", "reader_app", "static")

def parse_chapter_file(file_path):
    filename = os.path.basename(file_path)
    fn_match = re.search(r'ch_(\d+)', filename)
    fallback_num = int(fn_match.group(1)) if fn_match else 1

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
    title = title_match.group(1) if title_match else meta.get("title", f"Chương {fallback_num}")
    
    # Remove # Title from markdown body
    body_clean = re.sub(r"^#\s+.+$\n*", "", body, count=1, flags=re.MULTILINE)

    html_content = markdown.markdown(body_clean, extensions=["extra", "nl2br"])
    
    # Plain text excerpt for SEO
    plain_text = re.sub(r'<[^>]+>', ' ', html_content)
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()
    excerpt = (plain_text[:160] + '...') if len(plain_text) > 160 else plain_text

    ch_num = int(meta.get("chapter", fallback_num))
    return {
        "chapter": ch_num,
        "title": title,
        "volume": int(meta.get("volume", 1)),
        "arc": int(meta.get("arc", 1)),
        "word_count": int(meta.get("word_count", len(body.split()))),
        "date": meta.get("date", "2026-10-07"),
        "location": meta.get("location", ""),
        "excerpt": excerpt,
        "html": html_content
    }

def get_shared_css():
    return """
    :root {
      --font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-size: 19px;
      --reader-line-height: 1.85;
      --reader-max-width: 760px;
    }

    /* Theme 1: Peaceful Dark (Mặc định) */
    :root, html.theme-peaceful-dark, body.theme-peaceful-dark {
      --bg-color: #07090e;
      --bg-gradient: radial-gradient(ellipse at 50% 10%, #0d121f 0%, #07090e 80%);
      --text-color: #d6dce7;
      --text-muted: #828d9f;
      --header-bg: rgba(7, 9, 14, 0.92);
      --card-bg: rgba(14, 18, 27, 0.85);
      --card-bg-hover: rgba(22, 28, 42, 0.95);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-glow: rgba(16, 185, 129, 0.25);
      --accent-primary: #10b981;
      --accent-glow: rgba(16, 185, 129, 0.35);
      --gold-primary: #f59e0b;
      --gold-glow: rgba(245, 158, 11, 0.35);
      --cyan-subtle: #38bdf8;
    }

    /* Theme 2: Gentle Light */
    html.theme-gentle-light, body.theme-gentle-light {
      --bg-color: #f7f5f0;
      --bg-gradient: radial-gradient(circle at 50% 10%, #ffffff 0%, #f7f5f0 85%);
      --text-color: #24221f;
      --text-muted: #6b665f;
      --header-bg: rgba(247, 245, 240, 0.94);
      --card-bg: #ede9df;
      --card-bg-hover: #e4dfd3;
      --border-color: rgba(0, 0, 0, 0.09);
      --border-glow: rgba(185, 28, 28, 0.15);
      --accent-primary: #059669;
      --accent-glow: rgba(5, 150, 105, 0.2);
      --gold-primary: #92400e;
      --gold-glow: rgba(146, 64, 14, 0.2);
      --cyan-subtle: #0284c7;
    }

    /* Theme 3: OLED Pure Black */
    html.theme-oled, body.theme-oled {
      --bg-color: #000000;
      --bg-gradient: none;
      --text-color: #d1d5db;
      --text-muted: #6b7280;
      --header-bg: rgba(0, 0, 0, 0.95);
      --card-bg: #09090b;
      --card-bg-hover: #141417;
      --border-color: #27272a;
      --border-glow: rgba(16, 185, 129, 0.3);
      --accent-primary: #10b981;
      --accent-glow: rgba(16, 185, 129, 0.4);
      --gold-primary: #fbbf24;
      --gold-glow: rgba(251, 191, 36, 0.3);
      --cyan-subtle: #38bdf8;
    }

    /* Theme 4: Sepia */
    html.theme-sepia, body.theme-sepia {
      --bg-color: #f4edd8;
      --bg-gradient: radial-gradient(circle at 50% 10%, #faf6eb 0%, #f4edd8 85%);
      --text-color: #3b2d1d;
      --text-muted: #7d6a55;
      --header-bg: rgba(244, 237, 216, 0.95);
      --card-bg: #eae0c7;
      --card-bg-hover: #e0d4b8;
      --border-color: rgba(100, 75, 50, 0.14);
      --border-glow: rgba(160, 80, 20, 0.2);
      --accent-primary: #854d0e;
      --accent-glow: rgba(133, 77, 14, 0.2);
      --gold-primary: #b45309;
      --gold-glow: rgba(180, 83, 9, 0.2);
      --cyan-subtle: #0f766e;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    html { scroll-behavior: smooth; background-color: var(--bg-color); }
    body {
      font-family: var(--font-family); background: var(--bg-gradient); background-color: var(--bg-color);
      color: var(--text-color); min-height: 100vh; overflow-x: hidden; line-height: var(--reader-line-height);
      transition: background 0.3s ease, color 0.3s ease;
    }
    a { color: inherit; text-decoration: none; }

    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: var(--bg-color); }
    ::-webkit-scrollbar-thumb { background: var(--card-bg); border-radius: 4px; border: 1px solid var(--border-color); }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

    #progressBarContainer {
      position: fixed; top: 0; left: 0; width: 100%; height: 3px; background: transparent; z-index: 1050; pointer-events: none;
    }
    #progressBar {
      height: 100%; width: 0%; background: linear-gradient(90deg, var(--gold-primary), var(--accent-primary));
      box-shadow: 0 0 10px var(--accent-glow); transition: width 0.1s ease-out;
    }

    header {
      position: sticky; top: 0; left: 0; right: 0; height: 60px; background: var(--header-bg);
      backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-between; padding: 0 16px; z-index: 999;
      transition: transform 0.25s ease;
    }
    .header-left, .header-right { display: flex; align-items: center; gap: 8px; }
    .btn-brand {
      display: inline-flex; align-items: center; gap: 10px; background: none; border: none;
      cursor: pointer; padding: 4px 8px; border-radius: 24px; transition: all 0.2s ease;
    }
    .btn-brand:hover { background: rgba(255, 255, 255, 0.06); }
    .nav-logo {
      width: 34px; height: 34px; border-radius: 50%; border: 1.5px solid var(--gold-primary);
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.35); object-fit: cover;
    }
    .nav-brand-text {
      font-family: 'Lora', 'Georgia', serif; font-size: 16px; font-weight: 800; letter-spacing: 1.5px; color: var(--gold-primary);
    }
    .nav-live-badge {
      display: none; align-items: center; gap: 4px; padding: 2px 7px; border-radius: 12px;
      background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25);
      font-size: 10px; font-weight: 700; color: #10b981;
    }
    @media (min-width: 900px) { .nav-live-badge { display: inline-flex; } }

    .header-center { flex: 1; min-width: 0; text-align: center; padding: 0 8px; }
    .header-title {
      font-size: 14.5px; font-weight: 700; color: var(--gold-primary); white-space: nowrap;
      overflow: hidden; text-overflow: ellipsis; margin: 0; letter-spacing: 0.3px;
    }
    .header-sub {
      font-size: 11px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0; opacity: 0.85;
    }

    .btn-icon {
      background: none; border: none; color: var(--text-color); width: 38px; height: 38px;
      cursor: pointer; display: inline-flex; align-items: center; justify-content: center;
      border-radius: 10px; transition: all 0.2s ease; position: relative;
    }
    .btn-icon:hover { background: var(--card-bg); color: var(--gold-primary); }
    .btn-icon:active { transform: scale(0.94); }

    .btn-nav-home-pill {
      display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px;
      background: rgba(16, 185, 129, 0.12); border: 1px solid var(--accent-primary);
      color: #34d399; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s ease;
    }
    .btn-nav-home-pill:hover { background: var(--accent-primary); color: #ffffff; }

    .dot-live {
      width: 6px; height: 6px; border-radius: 50%; background: #10b981;
      box-shadow: 0 0 6px #10b981; animation: pulseDot 2s infinite ease-in-out;
    }
    @keyframes pulseDot { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.85); } }

    /* Modals, Drawers & Bottom Sheet */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.72); backdrop-filter: blur(4px);
      z-index: 1000; opacity: 0; pointer-events: none; transition: opacity 0.25s ease;
    }
    .modal-overlay.open { opacity: 1; pointer-events: auto; }

    .drawer {
      position: fixed; top: 0; bottom: 0; width: 86%; max-width: 420px; background: var(--card-bg);
      border-left: 1px solid var(--border-color); z-index: 1001; display: flex; flex-direction: column;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: -8px 0 24px rgba(0, 0, 0, 0.4);
    }
    .drawer-left { left: 0; border-left: none; border-right: 1px solid var(--border-color); transform: translateX(-100%); box-shadow: 8px 0 24px rgba(0, 0, 0, 0.4); }
    .drawer-left.open { transform: translateX(0); }
    .drawer-right { right: 0; transform: translateX(100%); }
    .drawer-right.open { transform: translateX(0); }

    .drawer-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid var(--border-color); }
    .drawer-title { font-size: 15px; font-weight: 800; color: var(--gold-primary); margin: 0; letter-spacing: 0.5px; }
    .drawer-tabs { display: flex; padding: 10px 14px; gap: 6px; border-bottom: 1px solid var(--border-color); background: rgba(0,0,0,0.15); }
    .drawer-tab-btn {
      flex: 1; padding: 7px 4px; border-radius: 8px; background: transparent; border: 1px solid transparent;
      color: var(--text-muted); font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; text-align: center;
    }
    .drawer-tab-btn.active { background: var(--card-bg); border-color: var(--border-color); color: var(--gold-primary); }
    .drawer-search { padding: 10px 16px; border-bottom: 1px solid var(--border-color); }
    .search-input {
      width: 100%; padding: 8px 12px; border-radius: 8px; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color);
      color: var(--text-color); font-size: 13px; outline: none;
    }
    .search-input:focus { border-color: var(--accent-primary); }
    .drawer-body { flex: 1; overflow-y: auto; padding: 10px 14px; }

    /* TOC items */
    .toc-item {
      padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer;
      display: flex; align-items: center; justify-content: space-between; border: 1px solid transparent;
      transition: all 0.18s ease; text-decoration: none; color: inherit;
    }
    .toc-item:hover { background: var(--card-bg-hover); border-color: var(--border-color); }
    .toc-item.active { background: rgba(16, 185, 129, 0.12); border-color: var(--accent-primary); }
    .toc-item.active .toc-name { color: var(--accent-primary); font-weight: 700; }
    .toc-info { min-width: 0; flex: 1; margin-right: 10px; }
    .toc-num {
      font-size: 11px; color: var(--gold-primary); font-weight: 700; text-transform: uppercase;
      margin-bottom: 2px; display: flex; align-items: center; gap: 6px;
    }
    .toc-name { font-size: 13.5px; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .toc-meta { font-size: 11px; color: var(--text-muted); }

    /* Codex Drawer Styles */
    .codex-card {
      background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px; margin-bottom: 14px;
    }
    .codex-card.locked { border-style: dashed; opacity: 0.8; }
    .codex-badge {
      display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;
      background: rgba(245, 158, 11, 0.15); color: var(--gold-primary); margin-bottom: 6px;
    }
    .codex-badge.locked-badge { background: rgba(255, 255, 255, 0.08); color: var(--text-muted); }
    .codex-title { font-size: 15px; font-weight: 700; color: var(--gold-primary); margin: 0 0 6px 0; }
    .codex-desc { font-size: 13px; color: var(--text-color); opacity: 0.9; line-height: 1.6; margin: 0; }
    .codex-stat {
      display: flex; justify-content: space-between; font-size: 12px; padding: 6px 0;
      border-top: 1px dashed var(--border-color); margin-top: 8px; color: var(--text-muted);
    }
    .codex-stat-val { color: var(--accent-primary); font-weight: 600; }
    .codex-unlock-hint { margin-top: 8px; font-size: 11.5px; font-weight: 600; color: var(--accent-primary); }

    /* Settings Bottom Sheet */
    .sheet-bottom {
      position: fixed; bottom: 0; left: 0; right: 0; background: var(--card-bg); z-index: 1002;
      border-top: 1px solid var(--border-color); border-radius: 20px 20px 0 0; max-width: 580px;
      margin: 0 auto; padding: 20px 24px 36px 24px; transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); max-height: 85vh; overflow-y: auto;
    }
    .sheet-bottom.open { transform: translateY(0); }
    .sheet-handle { width: 36px; height: 4px; border-radius: 2px; background: var(--border-color); margin: 0 auto 16px auto; }
    .setting-group { margin-bottom: 18px; }
    .setting-label { font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .theme-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .theme-opt {
      padding: 10px 6px; border-radius: 10px; border: 2px solid var(--border-color); background: rgba(0,0,0,0.1);
      cursor: pointer; text-align: center; font-size: 12px; font-weight: 600; color: var(--text-color); transition: all 0.2s;
    }
    .theme-opt.active { border-color: var(--accent-primary); box-shadow: 0 0 10px var(--accent-glow); }

    .stepper-ctrl {
      display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.15);
      border-radius: 10px; padding: 4px; border: 1px solid var(--border-color);
    }
    .btn-step {
      width: 44px; height: 38px; background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;
    }
    .stepper-val { font-size: 15px; font-weight: 700; color: var(--gold-primary); }

    .btn-opt-group { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .btn-opt-step {
      padding: 9px 4px; border-radius: 8px; border: 1px solid var(--border-color); background: rgba(0,0,0,0.15);
      color: var(--text-color); font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; text-align: center;
    }
    .btn-opt-step:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
    .btn-opt-step.active { background: rgba(16, 185, 129, 0.15); border-color: var(--accent-primary); color: var(--accent-primary); }

    .ambient-widget {
      display: flex; align-items: center; justify-content: space-between; padding: 10px 14px;
      border-radius: 10px; background: rgba(0,0,0,0.15); border: 1px solid var(--border-color); margin-top: 10px;
    }

    #liveToast {
      position: fixed; bottom: 74px; left: 50%; transform: translateX(-50%) translateY(30px);
      background: var(--card-bg); border: 1px solid var(--accent-primary); color: var(--text-color);
      font-size: 13px; font-weight: 600; padding: 10px 18px; border-radius: 30px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4); opacity: 0; pointer-events: none;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); z-index: 2000; white-space: nowrap; display: flex; align-items: center; gap: 8px;
    }
    #liveToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    """

def generate_cover_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#141824"/>
      <stop offset="60%" stop-color="#08090d"/>
      <stop offset="100%" stop-color="#040507"/>
    </radialGradient>
    <linearGradient id="goldText" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
    <linearGradient id="jadeAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="50%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  <rect width="1200" height="630" fill="url(#bgGlow)"/>
  <rect x="30" y="30" width="1140" height="570" fill="none" stroke="#262a38" stroke-width="2" rx="16"/>
  <rect x="42" y="42" width="1116" height="546" fill="none" stroke="rgba(245,158,11,0.2)" stroke-width="1" rx="12"/>
  <g transform="translate(600, 110)">
    <rect x="-190" y="-22" width="380" height="44" rx="22" fill="#131722" stroke="#10b981" stroke-width="1.5"/>
    <circle cx="-160" cy="0" r="5" fill="#10b981" filter="url(#glow)"/>
    <text x="0" y="7" fill="#a7f3d0" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle">ĐÔ THỊ TU CHÂN • TRƯỜNG THIÊN ĐẠI TÁC</text>
  </g>
  <text x="600" y="270" fill="url(#goldText)" font-family="'Palatino', 'Georgia', serif" font-size="108" font-weight="900" letter-spacing="14" text-anchor="middle" filter="url(#glow)">PHÁ TRỜI</text>
  <text x="600" y="330" fill="#94a3b8" font-family="-apple-system, sans-serif" font-size="22" font-weight="500" letter-spacing="8" text-anchor="middle">TIỂU THUYẾT ĐÔ THỊ TU CHÂN • TP. HỒ CHÍ MINH 2026</text>
  <line x1="450" y1="365" x2="750" y2="365" stroke="url(#jadeAccent)" stroke-width="2.5" stroke-linecap="round"/>
  <text x="600" y="420" fill="#cbd5e1" font-family="'Georgia', serif" font-size="20" font-style="italic" text-anchor="middle">"Một nhân viên văn phòng... cho đến khi phát hiện đại phong ấn sông ngầm Sài Gòn."</text>
  <g transform="translate(600, 500)">
    <text x="-320" y="0" fill="#f59e0b" font-family="-apple-system, sans-serif" font-size="15" font-weight="600" text-anchor="middle">📖 ĐỌC ONLINE / OFFLINE 24/7</text>
    <text x="0" y="0" fill="#10b981" font-family="-apple-system, sans-serif" font-size="15" font-weight="600" text-anchor="middle">🌙 CHẾ ĐỘ TỐI BÌNH YÊN & SÁNG THANH NHÃ</text>
    <text x="320" y="0" fill="#38bdf8" font-family="-apple-system, sans-serif" font-size="15" font-weight="600" text-anchor="middle">📱 HỖ TRỢ PWA MOBILE TOÀN DIỆN</text>
  </g>
  <text x="600" y="555" fill="#64748b" font-family="-apple-system, sans-serif" font-size="14" letter-spacing="2" text-anchor="middle">TÁC GIẢ: AN BÌNH • BẢO LƯU MỌI QUYỀN (ALL RIGHTS RESERVED)</text>
</svg>"""

def generate_404_html():
    return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Đang chuyển hướng — Phá Trời</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>
    (function() {
      var path = window.location.pathname;
      var match = path.match(/(?:chuong|chapter)[-_/]?(\\d+)/i);
      if (match) {
        window.location.replace('/pha-troi/chuong-' + match[1] + '/');
      } else {
        window.location.replace('/pha-troi/');
      }
    })();
  </script>
</head>
<body style="background:#07090e; color:#d6dce7; font-family:'Be Vietnam Pro', sans-serif; display:flex; align-items:center; justify-content:center; height:100vh; margin:0; text-align:center;">
  <div>
    <div style="font-size:32px; font-weight:800; color:#f59e0b; margin-bottom:12px;">PHÁ TRỜI</div>
    <p style="color:#828d9f; font-size:15px;">Đang kết nối và chuyển hướng đến chương truyện...</p>
  </div>
</body>
</html>"""

def generate_home_html(chapters_index, total_words):
    total_ch = len(chapters_index)
    shared_css = get_shared_css()

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026</title>
  
  <meta name="title" content="Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026">
  <meta name="description" content="Trường thiên tiểu thuyết đô thị tu chân Phá Trời. Một nhân viên văn phòng tại TP.HCM phát hiện phong ấn sông ngầm 2.5 triệu năm. Thể Đạo từ số 0 giữa đô thị hiện đại. Đọc trọn bộ {total_ch} chương online & offline 24/7.">
  <meta name="keywords" content="Phá Trời, Phá Toái Thần Hoang, Novel OS, tiểu thuyết đô thị, tu chân, thể đạo, Nguyễn Minh An, Lâm Tịch, An Bình">
  <meta name="author" content="An Bình">
  
  <meta property="og:type" content="book">
  <meta property="og:url" content="https://bon-231900.github.io/pha-troi/">
  <meta property="og:title" content="Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026">
  <meta property="og:description" content="Một nhân viên văn phòng tại TP.HCM phát hiện phong ấn sông ngầm 2.5 triệu năm. Không hệ thống, lấy Thể Đạo phàm nhân phá vỡ xiềng xích. Đọc trọn bộ {total_ch} chương.">
  <meta property="og:image" content="https://bon-231900.github.io/pha-troi/assets/cover_vertical.jpg">
  <meta property="og:image:width" content="682">
  <meta property="og:image:height" content="1024">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026">
  <meta name="twitter:description" content="Một nhân viên văn phòng tại TP.HCM phát hiện phong ấn sông ngầm 2.5 triệu năm. Đọc trọn bộ {total_ch} chương online & offline 24/7.">
  <meta name="twitter:image" content="https://bon-231900.github.io/pha-troi/assets/hero_horizontal.jpg">

  <link rel="manifest" href="./manifest.json">
  <link rel="icon" href="./assets/logo.webp" type="image/webp">
  <link rel="apple-touch-icon" href="./assets/logo.webp">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Phá Trời">
  <meta name="theme-color" content="#07090e">

  <link rel="preload" as="image" href="./assets/hero_horizontal.webp" type="image/webp" media="(min-width: 769px)">
  <link rel="preload" as="image" href="./assets/cover_vertical.webp" type="image/webp" media="(max-width: 768px)">
  <link rel="preload" as="image" href="./assets/logo.webp" type="image/webp">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <style>
    {shared_css}

    /* Hero Styling */
    .hero-section {{ position: relative; width: 100%; overflow: hidden; }}
    .hero-desktop {{
      display: none; position: relative; min-height: 520px; max-height: 640px; align-items: center;
      border-bottom: 1px solid var(--border-color); background: #07090e;
    }}
    @media (min-width: 769px) {{ .hero-desktop {{ display: flex; }} .hero-mobile {{ display: none; }} }}
    @media (max-width: 768px) {{ .hero-desktop {{ display: none; }} .hero-mobile {{ display: flex; }} }}

    .hero-bg-picture {{ position: absolute; inset: 0; width: 100%; height: 100%; z-index: 1; }}
    .hero-bg-img {{ width: 100%; height: 100%; object-fit: cover; object-position: center 20%; }}
    .hero-desktop-overlay {{
      position: absolute; inset: 0;
      background: 
        linear-gradient(90deg, rgba(7, 9, 14, 0.96) 0%, rgba(7, 9, 14, 0.88) 36%, rgba(7, 9, 14, 0.48) 65%, rgba(7, 9, 14, 0.12) 80%, rgba(7, 9, 14, 0.55) 100%),
        linear-gradient(0deg, var(--bg-color) 0%, rgba(7, 9, 14, 0.4) 25%, transparent 60%);
      z-index: 2; pointer-events: none;
    }}
    .hero-desktop-content {{
      position: relative; z-index: 3; max-width: 620px; padding: 44px 36px;
      margin-left: max(24px, calc((100vw - 1200px) / 2));
    }}

    .hero-mobile {{
      display: flex; flex-direction: column; position: relative; padding: 24px 16px 28px 16px;
      overflow: hidden; align-items: center; text-align: center; border-bottom: 1px solid var(--border-color);
      background: #07090e;
    }}
    .hero-mobile-backdrop {{
      position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center top;
      filter: blur(28px) brightness(0.24); transform: scale(1.15); z-index: 1; pointer-events: none;
    }}
    .hero-mobile-overlay {{
      position: absolute; inset: 0;
      background: linear-gradient(180deg, rgba(7, 9, 14, 0.45) 0%, rgba(7, 9, 14, 0.85) 60%, var(--bg-color) 100%);
      z-index: 2; pointer-events: none;
    }}
    .hero-mobile-content {{
      position: relative; z-index: 3; width: 100%; max-width: 440px; display: flex; flex-direction: column; align-items: center;
    }}
    .mobile-cover-wrap {{
      width: 160px; height: 240px; border-radius: 14px; box-shadow: 0 16px 36px rgba(0, 0, 0, 0.75), 0 0 24px rgba(16, 185, 129, 0.22);
      border: 1.5px solid rgba(255, 255, 255, 0.16); overflow: hidden; margin-bottom: 14px; position: relative;
    }}
    .mobile-cover-img {{ width: 100%; height: 100%; object-fit: cover; }}

    .hero-badge-pill {{
      display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 20px;
      background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399;
      font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 12px;
    }}
    .hero-title-row {{ display: flex; align-items: center; gap: 14px; margin-bottom: 8px; }}
    .hero-logo-crest {{
      width: 58px; height: 58px; border-radius: 50%; border: 2px solid var(--gold-primary);
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.4); object-fit: cover; flex-shrink: 0;
    }}
    .hero-main-title {{
      font-family: 'Lora', 'Georgia', serif; font-size: 42px; font-weight: 900; letter-spacing: 2px;
      line-height: 1.1; margin: 0;
      background: linear-gradient(135deg, #fef08a 0%, #f59e0b 50%, #b45309 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 30px rgba(245, 158, 11, 0.25);
    }}
    .mobile-title {{ font-size: 32px; letter-spacing: 1.5px; }}
    .hero-subtitle {{ font-size: 14px; font-weight: 700; letter-spacing: 3px; color: #94a3b8; text-transform: uppercase; margin-top: 2px; }}
    .mobile-sub {{ font-size: 12px; letter-spacing: 2px; margin-bottom: 8px; }}
    .hero-description {{ font-size: 14.5px; line-height: 1.75; color: #cbd5e1; margin: 10px 0 16px 0; opacity: 0.95; }}
    .mobile-desc {{ font-size: 13px; margin-bottom: 16px; line-height: 1.6; }}
    .hero-stats-bar {{ display: flex; align-items: center; flex-wrap: wrap; gap: 8px 12px; font-size: 12px; color: var(--text-muted); margin-bottom: 20px; }}
    .hero-stat-tag {{
      display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 6px;
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color); color: #e2e8f0; font-weight: 500;
    }}
    .hero-stat-tag strong {{ color: var(--gold-primary); }}

    .hero-actions {{ display: flex; align-items: center; flex-wrap: wrap; gap: 12px; }}
    .btn-hero-primary {{
      padding: 13px 26px; border-radius: 12px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      border: 1px solid rgba(52, 211, 153, 0.5); color: #ffffff; font-size: 15px; font-weight: 700;
      cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 10px;
      box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35); transition: all 0.22s ease;
    }}
    .btn-hero-primary:hover {{
      background: linear-gradient(135deg, #34d399 0%, #10b981 100%); box-shadow: 0 10px 28px rgba(16, 185, 129, 0.45); transform: translateY(-2px);
    }}
    .btn-hero-primary:active {{ transform: translateY(0) scale(0.98); }}

    .btn-hero-secondary {{
      padding: 13px 20px; border-radius: 12px; background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(8px);
      border: 1px solid var(--border-color); color: var(--text-color); font-size: 14px; font-weight: 600;
      cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s ease;
    }}
    .btn-hero-secondary:hover {{
      background: rgba(255, 255, 255, 0.12); border-color: var(--gold-primary); color: var(--gold-primary); transform: translateY(-1px);
    }}
    .btn-hero-outline {{
      padding: 13px 18px; border-radius: 12px; background: transparent; border: 1px dashed var(--border-color);
      color: var(--text-muted); font-size: 14px; font-weight: 500; cursor: pointer; display: inline-flex;
      align-items: center; justify-content: center; gap: 8px; transition: all 0.2s ease;
    }}
    .btn-hero-outline:hover {{ color: #38bdf8; border-color: #38bdf8; background: rgba(56, 189, 248, 0.06); }}
    .mobile-cta-full {{ width: 100%; padding: 14px; font-size: 15px; margin-bottom: 10px; }}
    .mobile-sub-row {{ display: flex; width: 100%; gap: 8px; }}
    .mobile-sub-row button, .mobile-sub-row a {{ flex: 1; padding: 11px 8px; font-size: 13px; text-align: center; }}

    /* Home Content Container */
    .home-container {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px 80px 20px; }}
    .section-title-wrap {{
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
      margin: 34px 0 16px 0; padding-bottom: 12px; border-bottom: 1px solid var(--border-color);
    }}
    .section-title {{
      font-size: 18px; font-weight: 800; color: var(--gold-primary); letter-spacing: 0.5px; margin: 0;
      display: flex; align-items: center; gap: 10px;
    }}
    .section-title::before {{ content: ""; display: inline-block; width: 4px; height: 18px; background: var(--accent-primary); border-radius: 2px; }}

    .continue-card {{
      background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 16px; padding: 18px 22px;
      display: flex; align-items: center; justify-content: space-between; gap: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
      transition: all 0.2s ease; margin-top: 14px;
    }}
    .continue-card:hover {{ border-color: rgba(16, 185, 129, 0.35); transform: translateY(-1px); }}
    .continue-card.welcome-mode {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(14, 18, 27, 0.9) 100%);
      border-color: rgba(16, 185, 129, 0.25);
    }}
    .continue-left {{ display: flex; align-items: center; gap: 16px; min-width: 0; flex: 1; }}
    .continue-thumb {{
      width: 46px; height: 46px; border-radius: 10px; object-fit: cover; border: 1.5px solid var(--gold-primary); flex-shrink: 0;
    }}
    .continue-info {{ min-width: 0; flex: 1; }}
    .continue-pill {{
      font-size: 11px; font-weight: 700; color: var(--accent-primary); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;
    }}
    .continue-chapter-name {{
      font-size: 15.5px; font-weight: 700; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}
    .continue-progress-meta {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}
    .continue-btn {{
      padding: 10px 18px; border-radius: 10px; background: rgba(16, 185, 129, 0.14); border: 1px solid var(--accent-primary);
      color: #34d399; font-size: 13px; font-weight: 700; cursor: pointer; white-space: nowrap; transition: all 0.2s ease;
    }}
    .continue-btn:hover {{ background: var(--accent-primary); color: #ffffff; }}

    /* TOC Grid */
    .home-toc-filter-row {{ display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; }}
    .home-tabs {{ display: flex; gap: 6px; background: rgba(0,0,0,0.2); padding: 4px; border-radius: 10px; border: 1px solid var(--border-color); }}
    .home-tab-btn {{
      padding: 6px 14px; border-radius: 8px; background: transparent; border: none; color: var(--text-muted);
      font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .home-tab-btn.active {{ background: var(--card-bg); color: var(--gold-primary); box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
    .home-search-box {{ position: relative; min-width: 220px; flex: 1; max-width: 360px; }}
    .home-search-input {{
      width: 100%; padding: 8px 14px 8px 36px; border-radius: 8px; background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); font-size: 13px; outline: none;
    }}
    .home-search-input:focus {{ border-color: var(--accent-primary); }}
    .home-search-icon {{ position: absolute; left: 11px; top: 50%; transform: translateY(-50%); color: var(--text-muted); pointer-events: none; }}
    .home-toc-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 12px; }}
    .home-ch-card {{
      background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px;
      cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 12px; transition: all 0.2s ease;
    }}
    .home-ch-card:hover {{
      background: var(--card-bg-hover); border-color: var(--gold-primary); transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }}
    .home-ch-card.is-current {{
      border-color: var(--gold-primary); background: rgba(245, 158, 11, 0.06); box-shadow: 0 0 16px rgba(245, 158, 11, 0.15);
    }}
    .home-ch-card.is-current .home-ch-title {{ color: var(--gold-primary); font-weight: 700; }}
    .home-ch-card.is-read {{ opacity: 0.88; }}
    .home-ch-info {{ min-width: 0; flex: 1; }}
    .home-ch-meta-top {{ display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--gold-primary); font-weight: 700; margin-bottom: 3px; }}
    .home-ch-title {{
      font-size: 14.5px; font-weight: 600; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 3px;
    }}
    .home-ch-meta-bottom {{ font-size: 11px; color: var(--text-muted); display: flex; gap: 10px; }}
    .home-ch-arrow {{ color: var(--text-muted); transition: transform 0.2s, color 0.2s; }}
    .home-ch-card:hover .home-ch-arrow {{ color: var(--gold-primary); transform: translateX(3px); }}

    .ch-status-tag {{ font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 4px; margin-left: auto; }}
    .ch-status-tag.read {{ background: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.25); }}
    .ch-status-tag.current {{ background: rgba(245, 158, 11, 0.16); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); }}
    .ch-status-tag.unread {{ background: rgba(255, 255, 255, 0.04); color: var(--text-muted); }}

    /* Codex Preview Cards */
    .home-codex-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 14px; margin-bottom: 20px; }}
    .home-codex-card {{
      background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 14px; padding: 16px;
      display: flex; flex-direction: column; cursor: pointer; transition: all 0.22s ease;
    }}
    .home-codex-card:hover {{ border-color: rgba(16, 185, 129, 0.4); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }}
    .home-codex-card.locked {{ border-style: dashed; opacity: 0.76; }}
    .home-codex-badge {{
      align-self: flex-start; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;
      background: rgba(245, 158, 11, 0.12); color: var(--gold-primary); margin-bottom: 8px;
    }}
    .home-codex-badge.locked-badge {{ background: rgba(255, 255, 255, 0.08); color: var(--text-muted); }}
    .home-codex-name {{ font-size: 16px; font-weight: 700; color: var(--text-color); margin: 0 0 6px 0; }}
    .home-codex-desc {{ font-size: 12.5px; color: var(--text-muted); line-height: 1.6; margin: 0; flex: 1; }}

    /* Footer */
    .site-footer {{
      margin-top: 50px; padding: 40px 20px 80px 20px; border-top: 1px solid var(--border-color);
      text-align: center; background: rgba(0, 0, 0, 0.2);
    }}
    .footer-logo {{ width: 46px; height: 46px; border-radius: 50%; border: 1.5px solid var(--gold-primary); margin-bottom: 12px; object-fit: cover; }}
    .footer-title {{ font-family: 'Lora', 'Georgia', serif; font-size: 16px; font-weight: 800; color: var(--gold-primary); letter-spacing: 1px; margin-bottom: 4px; }}
    .footer-sub {{ font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px; }}
    .footer-copy {{ font-size: 11px; color: var(--text-muted); opacity: 0.75; }}
  </style>
</head>
<body class="theme-peaceful-dark">

  <div id="progressBarContainer"><div id="progressBar"></div></div>

  <!-- HEADER -->
  <header id="topHeader">
    <div class="header-left">
      <a href="./" class="btn-brand" title="Trang Chủ Phá Trời">
        <picture>
          <source srcset="./assets/logo.webp" type="image/webp">
          <img src="./assets/logo.jpg" class="nav-logo" alt="Phá Trời">
        </picture>
        <span class="nav-brand-text">PHÁ TRỜI</span>
        <span class="nav-live-badge"><span class="dot-live"></span> {total_ch} CHƯƠNG</span>
      </a>
    </div>

    <div class="header-center">
      <h1 class="header-title" id="headerTitle">Phá Trời (Phá Toái Thần Hoang)</h1>
      <p class="header-sub" id="headerSub">{total_ch} chương • An Bình</p>
    </div>

    <div class="header-right">
      <button class="btn-icon" id="btnMenu" title="Mục Lục Chương (M)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      
      <button class="btn-icon" id="btnCodex" title="Codex Phá Trời — Bách Khoa Thế Giới (C)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
      </button>

      <button class="btn-icon" id="btnAmbient" title="Âm thanh Mưa Đêm Sài Gòn (Thư giãn)">
        <svg id="iconAudioOff" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>
        <svg id="iconAudioOn" style="display:none; color:var(--accent-primary);" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
      </button>

      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Nhanh Sáng / Tối (T)">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg id="iconSun" style="display:none;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button class="btn-icon" id="btnSettings" title="Cài Đặt Đọc Truyện">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
      </button>
    </div>
  </header>

  <!-- HOME VIEW -->
  <div id="homeView">
    <!-- HERO SECTION -->
    <section class="hero-section">
      <!-- Desktop Widescreen Hero -->
      <div class="hero-desktop">
        <picture class="hero-bg-picture">
          <source srcset="./assets/hero_horizontal.webp" type="image/webp">
          <img src="./assets/hero_horizontal.jpg" alt="Phá Trời Hero" class="hero-bg-img" fetchpriority="high">
        </picture>
        <div class="hero-desktop-overlay"></div>
        <div class="hero-desktop-content">
          <div class="hero-badge-pill"><span class="dot-live"></span> ĐÔ THỊ TU CHÂN • TP. HỒ CHÍ MINH 2026</div>
          <div class="hero-title-row">
            <picture>
              <source srcset="./assets/logo.webp" type="image/webp">
              <img src="./assets/logo.jpg" class="hero-logo-crest" alt="Logo Phá Trời">
            </picture>
            <div>
              <h1 class="hero-main-title">PHÁ TRỜI</h1>
              <div class="hero-subtitle">PHÁ TOÁI THẦN HOANG</div>
            </div>
          </div>
          <p class="hero-description">Một nhân viên văn phòng bình thường tại TP.HCM vô tình phát hiện phong ấn cổ xưa 2.5 triệu năm ẩn sâu dưới lòng sông Sài Gòn. Không thiên phú, không gia thế, không hệ thống hack game — Minh An dấn thân vào con đường Thể Đạo, lấy nhục thân phàm nhân phá vỡ vạn trùng xiềng xích.</p>
          <div class="hero-stats-bar">
            <span class="hero-stat-tag">📖 <strong>{total_ch}</strong> Chương</span>
            <span class="hero-stat-tag">⚡ <strong>{total_words:,}</strong> từ</span>
            <span class="hero-stat-tag">🌊 Quyển 1 & 2</span>
            <span class="hero-stat-tag"><span class="dot-live"></span> Đang ra tiếp</span>
          </div>
          <div class="hero-actions">
            <a href="./chuong-1/" class="btn-hero-primary" id="btnHeroReadPrimary">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
              <span id="heroPrimaryText">▶ Bắt Đầu Đọc — Chương 1</span>
            </a>
            <button class="btn-hero-secondary" id="btnHeroTocScroll">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
              <span>Mục Lục ({total_ch})</span>
            </button>
            <button class="btn-hero-outline" id="btnHeroCodexOpen">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
              <span>Codex Phá Trời</span>
            </button>
          </div>
          <div id="heroResetLinkWrap" style="display:none; margin-top:8px; font-size:12.5px; color:var(--text-muted);">
            <span>Đã đọc một phần? </span><a href="./chuong-1/" style="color:var(--accent-primary); font-weight:600;">Đọc lại từ Chương 1</a>
          </div>
        </div>
      </div>

      <!-- Mobile Portrait Cover Hero -->
      <div class="hero-mobile">
        <picture>
          <source srcset="./assets/cover_vertical.webp" type="image/webp">
          <img src="./assets/cover_vertical.jpg" class="hero-mobile-backdrop" alt="Backdrop">
        </picture>
        <div class="hero-mobile-overlay"></div>
        <div class="hero-mobile-content">
          <div class="mobile-cover-wrap">
            <picture>
              <source srcset="./assets/cover_vertical.webp" type="image/webp">
              <img src="./assets/cover_vertical.jpg" class="mobile-cover-img" alt="Phá Trời Bìa Dọc" fetchpriority="high">
            </picture>
          </div>
          <div class="hero-badge-pill"><span class="dot-live"></span> ĐÔ THỊ TU CHÂN • TP.HCM 2026</div>
          <h1 class="hero-main-title mobile-title">PHÁ TRỜI</h1>
          <div class="hero-subtitle mobile-sub">PHÁ TOÁI THẦN HOANG</div>
          <p class="hero-description mobile-desc">Một nhân viên văn phòng bình thường tại TP.HCM phát hiện phong ấn sông ngầm Sài Gòn. Không thiên phú, không hệ thống — lấy Thể Đạo phàm nhân phá vỡ xiềng xích.</p>
          <a href="./chuong-1/" class="btn-hero-primary mobile-cta-full" id="btnMobileHeroReadPrimary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            <span id="mobileHeroPrimaryText">▶ Bắt Đầu Đọc — Chương 1</span>
          </a>
          <div class="mobile-sub-row">
            <button class="btn-hero-secondary" id="btnMobileHeroTocScroll">Mục Lục ({total_ch})</button>
            <button class="btn-hero-outline" id="btnMobileHeroCodexOpen">Codex</button>
          </div>
          <div id="mobileHeroResetWrap" style="display:none; margin-top:8px; font-size:12px; color:var(--text-muted);">
            <a href="./chuong-1/" style="color:var(--accent-primary);">Đọc lại từ Chương 1</a>
          </div>
        </div>
      </div>
    </section>

    <!-- HOME BODY CONTENT -->
    <div class="home-container">
      <!-- SECTION 2: WELCOME & CONTINUE READING -->
      <div id="sectionContinue">
        <div class="continue-card welcome-mode" id="continueReadingCard">
          <div class="continue-left">
            <picture>
              <source srcset="./assets/logo.webp" type="image/webp">
              <img src="./assets/logo.jpg" class="continue-thumb" alt="Phá Trời">
            </picture>
            <div class="continue-info">
              <div class="continue-pill" id="contPill">HÀNH TRÌNH KHỞI ĐẦU</div>
              <div class="continue-chapter-name" id="contChName">Bạn chưa từng đọc Phá Trời? Bắt đầu từ Chương 1</div>
              <div class="continue-progress-meta" id="contChMeta">Dấn thân vào đại phong ấn sông ngầm Sài Gòn 2.5 triệu năm cùng Minh An</div>
            </div>
          </div>
          <a href="./chuong-1/" class="continue-btn" id="btnContinueJump">Bắt Đầu Đọc Chương 1 →</a>
        </div>
      </div>

      <!-- SECTION 3: TABLE OF CONTENTS -->
      <div id="sectionToc">
        <div class="section-title-wrap">
          <h2 class="section-title">MỤC LỤC TRỌN BỘ ({total_ch} CHƯƠNG)</h2>
          <div class="home-search-box">
            <svg class="home-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" class="home-search-input" id="inputHomeSearch" placeholder="Tìm số chương hoặc tiêu đề...">
          </div>
        </div>

        <div class="home-toc-filter-row">
          <div class="home-tabs">
            <button class="home-tab-btn active" data-home-filter="all">Tất Cả ({total_ch})</button>
            <button class="home-tab-btn" data-home-filter="arc1">Hồi 1 (1–46)</button>
            <button class="home-tab-btn" data-home-filter="arc2">Hồi 2 (47–{total_ch}+)</button>
          </div>
          <div style="font-size:12px; color:var(--text-muted);">
            Tổng cộng: <strong style="color:var(--gold-primary);">{total_words:,}</strong> từ bản thảo
          </div>
        </div>

        <div class="home-toc-grid" id="homeTocGrid">
          <!-- Populated dynamically by JavaScript -->
        </div>
      </div>

      <!-- SECTION 4: ENCYCLOPEDIA / CODEX PREVIEW -->
      <div id="sectionCodexPreview">
        <div class="section-title-wrap">
          <div>
            <h2 class="section-title">CODEX PHÁ TRỜI — KHÁM PHÁ THẾ GIỚI</h2>
            <div style="font-size:12.5px; color:var(--text-muted); margin-top:4px;">Hồ sơ nhân vật, cổ vật và thế giới quan đô thị tu chân. Mở khóa theo tiến độ đọc.</div>
          </div>
          <button class="btn-hero-outline" id="btnViewAllCodex" style="padding:6px 14px; font-size:12px;">Mở Bách Khoa Toàn Thư →</button>
        </div>
        <div class="home-codex-grid" id="homeCodexGrid">
          <!-- Populated dynamically based on reading progress -->
        </div>
      </div>

      <!-- SECTION 5: FOOTER -->
      <footer class="site-footer">
        <picture>
          <source srcset="./assets/logo.webp" type="image/webp">
          <img src="./assets/logo.jpg" class="footer-logo" alt="Phá Trời">
        </picture>
        <div class="footer-title">PHÁ TRỜI — PHÁ TOÁI THẦN HOANG</div>
        <div class="footer-sub">Trường thiên tiểu thuyết đô thị tu chân Sài Gòn 2026 • Tác giả: An Bình</div>
        <div class="footer-copy">Vận hành bởi Novel OS • Clean Slugs SEO • 100% Offline PWA • Tự động lưu tiến độ.</div>
      </footer>
    </div>
  </div>

  <!-- MODAL OVERLAY -->
  <div class="modal-overlay" id="modalOverlay"></div>

  <!-- TOC DRAWER -->
  <aside class="drawer drawer-left" id="drawerToc">
    <div class="drawer-header">
      <h2 class="drawer-title">MỤC LỤC TIỂU THUYẾT</h2>
      <button class="btn-icon" id="btnCloseToc">✕</button>
    </div>
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" data-filter="all">Tất Cả (<span id="tocTotalCount">{total_ch}</span>)</button>
      <button class="drawer-tab-btn" data-filter="arc1">Hồi 1 (1–46)</button>
      <button class="drawer-tab-btn" data-filter="arc2">Hồi 2 (47–{total_ch}+)</button>
    </div>
    <div class="drawer-search">
      <input type="text" id="inputTocSearch" class="search-input" placeholder="Tìm chương hoặc từ khóa...">
    </div>
    <div class="drawer-body" id="tocDrawerList"></div>
  </aside>

  <!-- CODEX DRAWER -->
  <aside class="drawer drawer-right" id="drawerCodex">
    <div class="drawer-header">
      <h2 class="drawer-title">CODEX PHÁ TRỜI</h2>
      <button class="btn-icon" id="btnCloseCodex">✕</button>
    </div>
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" id="tabCodexChar" data-codex="char">Nhân Vật</button>
      <button class="drawer-tab-btn" id="tabCodexItem" data-codex="item">Kho Cổ Vật</button>
      <button class="drawer-tab-btn" id="tabCodexLotus" data-codex="lotus">Thức Hải</button>
    </div>
    <div class="drawer-body" id="codexDrawerBody"></div>
  </aside>

  <!-- SETTINGS BOTTOM SHEET -->
  <aside class="sheet-bottom" id="settingsSheet">
    <div class="sheet-handle"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <h3 style="font-size:16px; font-weight:700; color:var(--gold-primary); margin:0;">TÙY CHỈNH ĐỌC TRUYỆN</h3>
      <button class="btn-icon" id="btnCloseSettings" style="width:32px; height:32px;">✕</button>
    </div>
    <div class="setting-group">
      <div class="setting-label">Chủ Đề Giao Diện</div>
      <div class="theme-grid">
        <div class="theme-opt active" data-theme="theme-peaceful-dark" style="background:#07090e; color:#d6dce7;">Tối Bình Yên</div>
        <div class="theme-opt" data-theme="theme-gentle-light" style="background:#f7f5f0; color:#24221f;">Sáng Thanh Nhã</div>
        <div class="theme-opt" data-theme="theme-oled" style="background:#000000; color:#cbd5e1;">OLED Đen</div>
        <div class="theme-opt" data-theme="theme-sepia" style="background:#f4edd8; color:#3b2d1d;">Sepia Cổ Điển</div>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Cỡ Chữ Đọc</div>
      <div class="stepper-ctrl">
        <button class="btn-step" id="btnFontDec">A-</button>
        <span class="stepper-val" id="fontSizeVal">19px</span>
        <button class="btn-step" id="btnFontInc">A+</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Độ Rộng Khung Đọc</div>
      <div class="btn-opt-group">
        <button class="btn-opt-step" data-opt-width="640">Hẹp (640px)</button>
        <button class="btn-opt-step active" data-opt-width="760">Chuẩn (760px)</button>
        <button class="btn-opt-step" data-opt-width="900">Rộng (900px)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Khoảng Cách Dòng</div>
      <div class="btn-opt-group">
        <button class="btn-opt-step" data-opt-lh="1.65">Gọn (1.65)</button>
        <button class="btn-opt-step active" data-opt-lh="1.85">Chuẩn (1.85)</button>
        <button class="btn-opt-step" data-opt-lh="2.1">Thoáng (2.1)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Phông Chữ</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
        <button class="btn-step" id="btnFontSerif" style="width:100%; font-family:serif;">Có Chân (Lora)</button>
        <button class="btn-step" id="btnFontSans" style="width:100%; font-family:sans-serif;">Không Chân (Be Vietnam)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Âm Thanh Thư Giãn (Mưa Đêm Sài Gòn)</div>
      <div class="ambient-widget">
        <button class="btn-icon" id="btnSheetAudioToggle" style="background:var(--card-bg);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
        </button>
        <input type="range" id="audioVolume" min="0" max="1" step="0.05" value="0.25" style="flex:1; margin:0 12px; accent-color:var(--accent-primary);">
        <span id="audioVolVal" style="font-size:12px; color:var(--text-muted); width:32px;">25%</span>
      </div>
    </div>
    <div style="margin-top:16px;">
      <button id="btnCacheAll" style="width:100%; padding:13px; border-radius:12px; background:var(--accent-primary); color:#ffffff; font-weight:700; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        <span id="cacheAllText">Tải Toàn Bộ {total_ch} Chương Để Đọc Offline</span>
      </button>
    </div>
  </aside>

  <div id="liveToast"><span class="dot-live"></span><span id="toastMsg">Thông báo</span></div>

  <script>
    // Check old hash links or query params and redirect to clean slug
    (function checkLegacyRedirect() {{
      const hash = window.location.hash;
      const mHash = hash.match(/#\\/chapter\\/(\\d+)/);
      if (mHash) {{
        window.location.replace('./chuong-' + mHash[1] + '/');
        return;
      }}
      const params = new URLSearchParams(window.location.search);
      const chParam = params.get('chuong');
      if (chParam) {{
        window.location.replace('./chuong-' + chParam + '/');
        return;
      }}
    }})();

    let chaptersData = [];
    let totalChapters = {total_ch};
    let activeArcFilter = 'all';
    let homeArcFilter = 'all';
    let activeCodexTab = 'char';

    const modalOverlay = document.getElementById('modalOverlay');
    const drawerToc = document.getElementById('drawerToc');
    const drawerCodex = document.getElementById('drawerCodex');
    const settingsSheet = document.getElementById('settingsSheet');
    const tocDrawerList = document.getElementById('tocDrawerList');
    const homeTocGrid = document.getElementById('homeTocGrid');
    const homeCodexGrid = document.getElementById('homeCodexGrid');
    const codexDrawerBody = document.getElementById('codexDrawerBody');
    const liveToast = document.getElementById('liveToast');
    const toastMsg = document.getElementById('toastMsg');

    // Web Audio Synthesizer (Pink Noise Rain)
    let audioCtx = null, noiseNode = null, gainNode = null, filterNode = null;
    let isRainPlaying = false, rainVolume = 0.25;

    function initAudio() {{
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }}

    function toggleRainSound() {{
      if (isRainPlaying) {{ stopRainSound(); showToast('🌧️ Đã tắt âm thanh mưa'); }}
      else {{ startRainSound(); showToast('🌧️ Bật âm thanh mưa đêm Sài Gòn (Thư giãn)'); }}
      updateAudioIcons();
    }}

    function startRainSound() {{
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      if (noiseNode) return;
      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < bufferSize; i++) {{
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.045;
        b6 = white * 0.115926;
      }}
      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = noiseBuffer;
      noiseNode.loop = true;
      filterNode = audioCtx.createBiquadFilter();
      filterNode.type = 'lowpass';
      filterNode.frequency.value = 750;
      gainNode = audioCtx.createGain();
      gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
      noiseNode.connect(filterNode);
      filterNode.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      noiseNode.start();
      isRainPlaying = true;
    }}

    function stopRainSound() {{
      if (noiseNode) {{
        try {{ noiseNode.stop(); noiseNode.disconnect(); }} catch (e) {{}}
        noiseNode = null;
      }}
      isRainPlaying = false;
    }}

    function updateAudioIcons() {{
      const offIcon = document.getElementById('iconAudioOff');
      const onIcon = document.getElementById('iconAudioOn');
      if (isRainPlaying) {{
        if (offIcon) offIcon.style.display = 'none';
        if (onIcon) onIcon.style.display = 'inline-block';
      }} else {{
        if (offIcon) offIcon.style.display = 'inline-block';
        if (onIcon) onIcon.style.display = 'none';
      }}
    }}

    document.getElementById('btnAmbient').onclick = toggleRainSound;
    document.getElementById('btnSheetAudioToggle').onclick = toggleRainSound;
    document.getElementById('audioVolume').oninput = (e) => {{
      rainVolume = parseFloat(e.target.value);
      document.getElementById('audioVolVal').innerText = Math.round(rainVolume * 100) + '%';
      if (gainNode && audioCtx) gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
    }};

    function updateContinueReadingCard() {{
      const savedRaw = localStorage.getItem('pha_troi_cur_ch');
      const hasHistory = (savedRaw !== null);
      const savedCh = hasHistory ? parseInt(savedRaw) : 1;
      
      const contCard = document.getElementById('continueReadingCard');
      const contPill = document.getElementById('contPill');
      const contEl = document.getElementById('contChName');
      const metaEl = document.getElementById('contChMeta');
      const btnJump = document.getElementById('btnContinueJump');
      const heroPrimary = document.getElementById('btnHeroReadPrimary');
      const heroReadText = document.getElementById('heroPrimaryText');
      const mobileHeroPrimary = document.getElementById('btnMobileHeroReadPrimary');
      const mobileHeroReadText = document.getElementById('mobileHeroPrimaryText');
      const heroResetWrap = document.getElementById('heroResetLinkWrap');
      const mobileResetWrap = document.getElementById('mobileHeroResetWrap');

      if (!hasHistory || savedCh <= 1) {{
        if (contCard) contCard.classList.add('welcome-mode');
        if (contPill) contPill.innerText = 'HÀNH TRÌNH KHỞI ĐẦU';
        if (contEl) contEl.innerText = 'Bạn chưa từng đọc Phá Trời? Bắt đầu từ Chương 1';
        if (metaEl) metaEl.innerText = 'Dấn thân vào đại phong ấn sông ngầm Sài Gòn 2.5 triệu năm cùng Minh An';
        if (btnJump) {{ btnJump.innerText = 'Bắt Đầu Đọc Chương 1 →'; btnJump.href = './chuong-1/'; }}
        if (heroPrimary) heroPrimary.href = './chuong-1/';
        if (heroReadText) heroReadText.innerText = '▶ Bắt Đầu Đọc — Chương 1';
        if (mobileHeroPrimary) mobileHeroPrimary.href = './chuong-1/';
        if (mobileHeroReadText) mobileHeroReadText.innerText = '▶ Bắt Đầu Đọc — Chương 1';
        if (heroResetWrap) heroResetWrap.style.display = 'none';
        if (mobileResetWrap) mobileResetWrap.style.display = 'none';
      }} else {{
        const chInfo = chaptersData.find(c => c.chapter === savedCh) || {{ title: `Chương ${{savedCh}}`, arc: 1 }};
        const cleanTitle = chInfo.title.replace(/^Chương \\d+:\\s*/i, '');
        const pct = Math.round((savedCh / totalChapters) * 100);
        const targetUrl = `./chuong-${{savedCh}}/`;

        if (contCard) contCard.classList.remove('welcome-mode');
        if (contPill) contPill.innerText = 'TIẾN ĐỘ ĐANG ĐỌC';
        if (contEl) contEl.innerText = `Chương ${{savedCh}}: ${{cleanTitle}}`;
        if (metaEl) metaEl.innerText = `Tiến độ: Chương ${{savedCh}} / ${{totalChapters}} (${{pct}}%) • Hồi ${{chInfo.arc || 1}}`;
        if (btnJump) {{ btnJump.innerText = `Tiếp Tục Đọc Chương ${{savedCh}} →`; btnJump.href = targetUrl; }}
        if (heroPrimary) heroPrimary.href = targetUrl;
        if (heroReadText) heroReadText.innerText = `▶ Tiếp Tục — Chương ${{savedCh}}`;
        if (mobileHeroPrimary) mobileHeroPrimary.href = targetUrl;
        if (mobileHeroReadText) mobileHeroReadText.innerText = `▶ Tiếp Tục — Chương ${{savedCh}}`;
        if (heroResetWrap) heroResetWrap.style.display = 'block';
        if (mobileResetWrap) mobileResetWrap.style.display = 'block';
      }}

      renderHomeToc();
      renderTOC();
      renderCodexPreview(savedCh);
      renderCodexDrawer(savedCh);
    }}

    document.getElementById('btnHeroTocScroll').onclick = () => {{
      document.getElementById('sectionToc').scrollIntoView({{ behavior: 'smooth' }});
    }};
    document.getElementById('btnMobileHeroTocScroll').onclick = () => {{
      document.getElementById('sectionToc').scrollIntoView({{ behavior: 'smooth' }});
    }};
    document.getElementById('btnHeroCodexOpen').onclick = () => openCodex();
    document.getElementById('btnMobileHeroCodexOpen').onclick = () => openCodex();
    document.getElementById('btnViewAllCodex').onclick = () => openCodex();

    async function loadChaptersIndex() {{
      try {{
        const res = await fetch('./data/chapters.json?v=' + Date.now());
        const data = await res.json();
        chaptersData = data.chapters || [];
        totalChapters = chaptersData.length;
        document.getElementById('tocTotalCount').innerText = totalChapters;
        updateContinueReadingCard();
      }} catch (err) {{
        console.warn('Lỗi đọc dữ liệu chapters.json:', err);
      }}
    }}

    function renderTOC() {{
      const searchVal = document.getElementById('inputTocSearch').value.toLowerCase().trim();
      const savedCh = parseInt(localStorage.getItem('pha_troi_cur_ch') || '0');
      const hasHistory = (localStorage.getItem('pha_troi_cur_ch') !== null);

      const filtered = chaptersData.filter(ch => {{
        const matchSearch = !searchVal || ch.title.toLowerCase().includes(searchVal) || String(ch.chapter).includes(searchVal);
        const matchArc = (activeArcFilter === 'all') ||
                         (activeArcFilter === 'arc1' && ch.arc === 1) ||
                         (activeArcFilter === 'arc2' && ch.arc === 2);
        return matchSearch && matchArc;
      }});

      const renderHtml = filtered.map(ch => {{
        let statusBadge = '';
        if (hasHistory) {{
          if (ch.chapter < savedCh) statusBadge = '<span class="ch-status-tag read">✓</span>';
          else if (ch.chapter === savedCh) statusBadge = '<span class="ch-status-tag current">▶</span>';
        }}
        return `
          <a href="./chuong-${{ch.chapter}}/" class="toc-item">
            <div class="toc-info">
              <div class="toc-num">
                <span>Hồi ${{ch.arc || 1}} • Chương ${{ch.chapter}}</span>
                ${{statusBadge}}
              </div>
              <div class="toc-name">${{ch.title.replace(/^Chương \\d+:\\s*/i, '')}}</div>
            </div>
            <span class="toc-meta">${{ch.word_count ? ch.word_count.toLocaleString() + ' từ' : ''}}</span>
          </a>
        `;
      }}).join('');

      tocDrawerList.innerHTML = renderHtml || '<p style="text-align:center; color:var(--text-muted); padding:20px;">Không tìm thấy chương nào.</p>';
    }}

    document.getElementById('inputTocSearch').oninput = renderTOC;

    document.querySelectorAll('.drawer-tab-btn[data-filter]').forEach(btn => {{
      btn.onclick = () => {{
        document.querySelectorAll('.drawer-tab-btn[data-filter]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeArcFilter = btn.dataset.filter;
        renderTOC();
      }};
    }});

    function renderHomeToc() {{
      const searchVal = (document.getElementById('inputHomeSearch')?.value || '').toLowerCase().trim();
      const savedCh = parseInt(localStorage.getItem('pha_troi_cur_ch') || '0');
      const hasHistory = (localStorage.getItem('pha_troi_cur_ch') !== null);

      const filtered = chaptersData.filter(ch => {{
        const matchSearch = !searchVal || ch.title.toLowerCase().includes(searchVal) || String(ch.chapter).includes(searchVal);
        const matchArc = (homeArcFilter === 'all') ||
                         (homeArcFilter === 'arc1' && ch.arc === 1) ||
                         (homeArcFilter === 'arc2' && ch.arc === 2);
        return matchSearch && matchArc;
      }});

      const gridHtml = filtered.map(ch => {{
        let statusBadge = '';
        let cardClass = '';
        if (hasHistory) {{
          if (ch.chapter < savedCh) {{
            statusBadge = '<span class="ch-status-tag read">✓ Đã đọc</span>';
            cardClass = 'is-read';
          }} else if (ch.chapter === savedCh) {{
            statusBadge = '<span class="ch-status-tag current">▶ Đang đọc</span>';
            cardClass = 'is-current';
          }} else {{
            statusBadge = '<span class="ch-status-tag unread">○</span>';
          }}
        }}

        return `
          <a href="./chuong-${{ch.chapter}}/" class="home-ch-card ${{cardClass}}">
            <div class="home-ch-info">
              <div class="home-ch-meta-top">
                <span>HỒI ${{ch.arc || 1}} • CHƯƠNG ${{ch.chapter}}</span>
                ${{statusBadge}}
              </div>
              <div class="home-ch-title">${{ch.title.replace(/^Chương \\d+:\\s*/i, '')}}</div>
              <div class="home-ch-meta-bottom">
                <span>${{ch.word_count ? ch.word_count.toLocaleString() + ' từ' : ''}}</span>
                ${{ch.location ? '<span>• ' + ch.location.split(',')[0] + '</span>' : ''}}
              </div>
            </div>
            <div class="home-ch-arrow">→</div>
          </a>
        `;
      }}).join('');

      if (homeTocGrid) {{
        homeTocGrid.innerHTML = gridHtml || '<p style="text-align:center; color:var(--text-muted); grid-column: 1/-1; padding:30px;">Không tìm thấy chương phù hợp.</p>';
      }}
    }}

    document.getElementById('inputHomeSearch').oninput = renderHomeToc;

    document.querySelectorAll('.home-tab-btn[data-home-filter]').forEach(btn => {{
      btn.onclick = () => {{
        document.querySelectorAll('.home-tab-btn[data-home-filter]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        homeArcFilter = btn.dataset.homeFilter;
        renderHomeToc();
      }};
    }});

    function renderCodexPreview(savedCh) {{
      if (!homeCodexGrid) return;
      const s = parseInt(savedCh) || 1;
      let html = '';

      if (s >= 20) {{
        html += `
          <div class="home-codex-card" onclick="openCodexTab('char')">
            <span class="home-codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
            <div class="home-codex-name">Nguyễn Minh An (25 tuổi)</div>
            <p class="home-codex-desc">Luyện Cốt Trung kỳ (Cốt Nhược Kim Thạch). Đúc cốt ngự kình, kình lực vạn cân, Thức Hải Thanh Liên bảo bọc tâm mạch.</p>
          </div>
        `;
      }} else {{
        html += `
          <div class="home-codex-card" onclick="openCodexTab('char')">
            <span class="home-codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
            <div class="home-codex-name">Nguyễn Minh An (24 tuổi)</div>
            <p class="home-codex-desc">Nhân viên văn phòng bình thường tại TP.HCM. Bắt đầu con đường Thể Đạo từ số 0 sau biến cố trên cầu Sài Gòn.</p>
            <div class="codex-unlock-hint">🔒 Đang rèn luyện Tẩy Tủy Hoán Cốt</div>
          </div>
        `;
      }}

      if (s >= 10) {{
        html += `
          <div class="home-codex-card" onclick="openCodexTab('lotus')">
            <span class="home-codex-badge">NỮ CHÍNH • NGUYÊN THẦN</span>
            <div class="home-codex-name">Lâm Tịch (Bạch Y Tiên Tử)</div>
            <p class="home-codex-desc">Tàn phiến Nguyên Thần viễn cổ 2.5 triệu năm ngụ trong Thức Hải Thanh Liên của Minh An, che chở tâm mạch phàm trần.</p>
          </div>
        `;
      }} else {{
        html += `
          <div class="home-codex-card locked" onclick="openCodexTab('lotus')">
            <span class="home-codex-badge locked-badge">🔒 HỒ SƠ ẨN</span>
            <div class="home-codex-name" style="color:var(--text-muted);">Bóng Hình Bí Ẩn</div>
            <p class="home-codex-desc">Tàn niệm cổ xưa ẩn hiện trong làn sương đêm sông Sài Gòn...</p>
            <div class="codex-unlock-hint">🔒 Đọc đến Chương 10 để mở khóa</div>
          </div>
        `;
      }}

      if (s >= 15) {{
        html += `
          <div class="home-codex-card" onclick="openCodexTab('item')">
            <span class="home-codex-badge">VŨ KHÍ THỰC CHIẾN</span>
            <div class="home-codex-name">Hắc Thiết Đoản Côn</div>
            <p class="home-codex-desc">Rèn từ thép nhíp Zil tôi dầu cám chu sa thạch anh. Dài 52cm, nặng 3.2kg, dẫn truyền Kính Kình hoàn hảo.</p>
          </div>
        `;
      }} else {{
        html += `
          <div class="home-codex-card locked" onclick="openCodexTab('item')">
            <span class="home-codex-badge locked-badge">🔒 KHÍ BINH ẨN</span>
            <div class="home-codex-name" style="color:var(--text-muted);">Vũ Khí Thể Đạo</div>
            <p class="home-codex-desc">Trọng khí thể đạo rèn trong lò lửa thầm lặng của phàm trần...</p>
            <div class="codex-unlock-hint">🔒 Đọc đến Chương 15 để mở khóa</div>
          </div>
        `;
      }}

      if (s >= 25) {{
        html += `
          <div class="home-codex-card" onclick="openCodexTab('item')">
            <span class="home-codex-badge">CỔ KHÍ PHONG ẤN</span>
            <div class="home-codex-name">Trấn Thủy Đoản Đao</div>
            <p class="home-codex-desc">Di vật Thủy Môn Thập Nhị Tiêu niên đại > 2.5 triệu năm. Thuần phục dưới kình lực Thiết Lương Thập Phách.</p>
          </div>
        `;
      }} else {{
        html += `
          <div class="home-codex-card locked" onclick="openCodexTab('item')">
            <span class="home-codex-badge locked-badge">🔒 THẦN BINH ẨN</span>
            <div class="home-codex-name" style="color:var(--text-muted);">Cổ Vật Trấn Thủy</div>
            <p class="home-codex-desc">Cổ đao trấn áp mắt trận phong ấn sâu dưới lòng sông ngầm Sài Gòn...</p>
            <div class="codex-unlock-hint">🔒 Đọc đến Chương 25 để mở khóa</div>
          </div>
        `;
      }}

      homeCodexGrid.innerHTML = html;
    }}

    function renderCodexDrawer(savedCh) {{
      if (!codexDrawerBody) return;
      const s = parseInt(savedCh) || 1;
      let html = '';

      if (activeCodexTab === 'char') {{
        if (s >= 20) {{
          html = `
            <div class="codex-card">
              <span class="codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
              <h3 class="codex-title">Nguyễn Minh An (25 tuổi)</h3>
              <p class="codex-desc">Người bình thường 100% tại TP.HCM năm 2026. Tự lực tôi luyện ý chí và nhục thân, dùng đôi bàn tay trần gánh vác trách nhiệm bảo vệ cõi phàm trần.</p>
              <div class="codex-stat"><span>Cơ Quan</span><span class="codex-stat-val">Viện Địa Tầng Đô Thị</span></div>
              <div class="codex-stat"><span>Cảnh Giới</span><span class="codex-stat-val">Luyện Cốt Trung Kỳ</span></div>
              <div class="codex-stat"><span>Kình Lực</span><span class="codex-stat-val">Cốt Nhược Kim Thạch (Vạn Cân)</span></div>
              <div class="codex-stat"><span>Thể Thuật</span><span class="codex-stat-val">Kính Kình Phản Chấn Thuật</span></div>
            </div>
          `;
        }} else {{
          html = `
            <div class="codex-card">
              <span class="codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
              <h3 class="codex-title">Nguyễn Minh An (24 tuổi)</h3>
              <p class="codex-desc">Nhân viên văn phòng bình thường tại TP.HCM. Tăng ca về muộn trên cầu Sài Gòn thì tao ngộ dị biến sông ngầm. Không linh căn, không hệ thống, bắt đầu từ số 0.</p>
              <div class="codex-stat"><span>Cơ Quan</span><span class="codex-stat-val">Viện Địa Tầng Đô Thị</span></div>
              <div class="codex-stat"><span>Cảnh Giới</span><span class="codex-stat-val">Phàm Thể (Bắt đầu Tẩy Tủy)</span></div>
              <div class="codex-stat"><span>Thể Thuật</span><span class="codex-stat-val">🔒 Mở khóa theo tiến độ đọc</span></div>
            </div>
          `;
        }}
      }} else if (activeCodexTab === 'item') {{
        if (s >= 15) {{
          html += `
            <div class="codex-card">
              <span class="codex-badge">VŨ KHÍ CHÍNH</span>
              <h3 class="codex-title">Hắc Thiết Đoản Côn</h3>
              <p class="codex-desc">Thép nhíp Zil tôi dầu cám chu sa thạch anh do bác Sáu Kiên và Minh An rèn. Chịu lực đè nửa tấn, miễn nhiễm âm sát, dẫn truyền hoàn hảo Kính Kình.</p>
              <div class="codex-stat"><span>Kích Thước</span><span class="codex-stat-val">Dài 52cm • Nặng 3.2kg</span></div>
            </div>
          `;
        }} else {{
          html += `
            <div class="codex-card locked">
              <span class="codex-badge locked-badge">🔒 KHÍ BINH ẨN</span>
              <h3 class="codex-title" style="color:var(--text-muted);">Hắc Thiết Đoản Côn</h3>
              <p class="codex-desc">Vũ khí thô ráp rèn từ phàm thiết tôi trong tâm huyết...</p>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương 15 để mở khóa chi tiết</div>
            </div>
          `;
        }}

        if (s >= 25) {{
          html += `
            <div class="codex-card">
              <span class="codex-badge">CỔ KHÍ TRẤN THỦY</span>
              <h3 class="codex-title">Trấn Thủy Đoản Đao</h3>
              <p class="codex-desc">Thanh đoản đao đồng thau cổ niên đại địa chất > 2.5 triệu năm, cọc tiêu chốt chặn Thủy Môn Tiêu rạch Lò Gốm.</p>
              <div class="codex-stat"><span>Niên Đại</span><span class="codex-stat-val">> 2.5 Triệu Năm</span></div>
            </div>
          `;
        }} else {{
          html += `
            <div class="codex-card locked">
              <span class="codex-badge locked-badge">🔒 CỔ VẬT ẨN</span>
              <h3 class="codex-title" style="color:var(--text-muted);">Trấn Thủy Đoản Đao</h3>
              <p class="codex-desc">Cổ vật trấn áp phong ấn sông ngầm Sài Gòn...</p>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương 25 để mở khóa chi tiết</div>
            </div>
          `;
        }}
      }} else if (activeCodexTab === 'lotus') {{
        if (s >= 10) {{
          html = `
            <div class="codex-card">
              <span class="codex-badge">NỮ CHÍNH • THỨC HẢI</span>
              <h3 class="codex-title">Lâm Tịch (Bạch Y Tiên Tử)</h3>
              <p class="codex-desc">Nguyên Thần Tàn Phiến viễn cổ. Ngủ say trên Thanh Liên Đài ngọc bích bảo bọc tâm thức của Minh An.</p>
              <div class="codex-stat"><span>Trạng Thái</span><span class="codex-stat-val">Ngủ Say (Tĩnh Dưỡng Tàn Hồn)</span></div>
            </div>
          `;
        }} else {{
          html = `
            <div class="codex-card locked">
              <span class="codex-badge locked-badge">🔒 BÍ ẨN THỨC HẢI</span>
              <h3 class="codex-title" style="color:var(--text-muted);">Tàn Niệm Cổ Xưa</h3>
              <p class="codex-desc">Bóng hình áo trắng ngủ say nơi vực sâu vô tận...</p>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương 10 để mở khóa danh tính</div>
            </div>
          `;
        }}
      }}

      codexDrawerBody.innerHTML = html;
    }}

    function openCodexTab(tabName) {{
      activeCodexTab = tabName;
      ['tabCodexChar', 'tabCodexItem', 'tabCodexLotus'].forEach(id => {{
        const btn = document.getElementById(id);
        if (btn) btn.classList.toggle('active', btn.dataset.codex === tabName);
      }});
      openCodex();
    }}

    ['tabCodexChar', 'tabCodexItem', 'tabCodexLotus'].forEach(id => {{
      const btn = document.getElementById(id);
      if (btn) btn.onclick = () => openCodexTab(btn.dataset.codex);
    }});

    function closeAllDrawers() {{
      modalOverlay.classList.remove('open');
      drawerToc.classList.remove('open');
      drawerCodex.classList.remove('open');
      settingsSheet.classList.remove('open');
    }}

    function openToc() {{
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerToc.classList.add('open');
    }}

    function openCodex() {{
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerCodex.classList.add('open');
      const savedCh = parseInt(localStorage.getItem('pha_troi_cur_ch') || '1');
      renderCodexDrawer(savedCh);
    }}

    function openSettings() {{
      closeAllDrawers();
      modalOverlay.classList.add('open');
      settingsSheet.classList.add('open');
    }}

    modalOverlay.onclick = closeAllDrawers;
    document.getElementById('btnMenu').onclick = openToc;
    document.getElementById('btnCloseToc').onclick = closeAllDrawers;
    document.getElementById('btnCodex').onclick = openCodex;
    document.getElementById('btnCloseCodex').onclick = closeAllDrawers;
    document.getElementById('btnSettings').onclick = openSettings;
    document.getElementById('btnCloseSettings').onclick = closeAllDrawers;

    // Reading Settings Handlers
    const THEMES = ['theme-peaceful-dark', 'theme-gentle-light', 'theme-oled', 'theme-sepia'];
    function setTheme(theme) {{
      THEMES.forEach(t => {{
        document.documentElement.classList.remove(t);
        document.body.classList.remove(t);
      }});
      document.documentElement.classList.add(theme);
      document.body.classList.add(theme);

      document.querySelectorAll('.theme-opt').forEach(opt => {{
        opt.classList.toggle('active', opt.dataset.theme === theme);
      }});

      const sunIcon = document.getElementById('iconSun');
      const moonIcon = document.getElementById('iconMoon');
      if (theme === 'theme-gentle-light') {{
        if (sunIcon) sunIcon.style.display = 'inline-block';
        if (moonIcon) moonIcon.style.display = 'none';
      }} else {{
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) moonIcon.style.display = 'inline-block';
      }}
      localStorage.setItem('pha_troi_theme', theme);
    }}

    document.querySelectorAll('.theme-opt').forEach(opt => {{
      opt.onclick = () => {{
        setTheme(opt.dataset.theme);
        showToast('🎨 Đã chuyển giao diện: ' + opt.innerText.trim());
      }};
    }});

    document.getElementById('btnQuickTheme').onclick = () => {{
      const isLight = document.body.classList.contains('theme-gentle-light');
      const target = isLight ? 'theme-peaceful-dark' : 'theme-gentle-light';
      setTheme(target);
      showToast(target === 'theme-gentle-light' ? '☀️ Đã bật giao diện Sáng' : '🌙 Đã bật giao diện Tối');
    }};

    const savedTheme = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
    setTheme(savedTheme);

    let curFontSize = parseInt(localStorage.getItem('pha_troi_font_size') || '19');
    function applyFontSize(size) {{
      curFontSize = Math.max(15, Math.min(26, size));
      document.documentElement.style.setProperty('--font-size', curFontSize + 'px');
      document.getElementById('fontSizeVal').innerText = curFontSize + 'px';
      localStorage.setItem('pha_troi_font_size', curFontSize);
    }}
    document.getElementById('btnFontDec').onclick = () => applyFontSize(curFontSize - 1);
    document.getElementById('btnFontInc').onclick = () => applyFontSize(curFontSize + 1);
    applyFontSize(curFontSize);

    function applyReaderWidth(w) {{
      document.documentElement.style.setProperty('--reader-max-width', w + 'px');
      localStorage.setItem('pha_troi_reader_width', w);
      document.querySelectorAll('.btn-opt-step[data-opt-width]').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.optWidth === String(w));
      }});
    }}
    document.querySelectorAll('.btn-opt-step[data-opt-width]').forEach(btn => {{
      btn.onclick = () => {{
        applyReaderWidth(parseInt(btn.dataset.optWidth));
        showToast('📏 Khung đọc: ' + btn.innerText.trim());
      }};
    }});
    const savedWidth = parseInt(localStorage.getItem('pha_troi_reader_width') || '760');
    applyReaderWidth(savedWidth);

    function applyLineHeight(lh) {{
      document.documentElement.style.setProperty('--reader-line-height', lh);
      localStorage.setItem('pha_troi_line_height', lh);
      document.querySelectorAll('.btn-opt-step[data-opt-lh]').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.optLh === String(lh));
      }});
    }}
    document.querySelectorAll('.btn-opt-step[data-opt-lh]').forEach(btn => {{
      btn.onclick = () => {{
        applyLineHeight(parseFloat(btn.dataset.optLh));
        showToast('📄 Giãn dòng: ' + btn.innerText.trim());
      }};
    }});
    const savedLh = parseFloat(localStorage.getItem('pha_troi_line_height') || '1.85');
    applyLineHeight(savedLh);

    const FONT_SERIF = "'Lora', 'Georgia', serif";
    const FONT_SANS = "'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif";
    document.getElementById('btnFontSerif').onclick = () => {{
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
      localStorage.setItem('pha_troi_font_family', 'serif');
      showToast('📖 Phông chữ Có Chân (Lora)');
    }};
    document.getElementById('btnFontSans').onclick = () => {{
      document.documentElement.style.setProperty('--font-family', FONT_SANS);
      document.body.style.setProperty('--font-family', FONT_SANS);
      localStorage.setItem('pha_troi_font_family', 'sans');
      showToast('📱 Phông chữ Không Chân (Be Vietnam Pro)');
    }};

    const savedFont = localStorage.getItem('pha_troi_font_family');
    if (savedFont === 'serif') {{
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key.toLowerCase() === 't') document.getElementById('btnQuickTheme').click();
      else if (e.key.toLowerCase() === 'm') openToc();
      else if (e.key.toLowerCase() === 'c') openCodex();
      else if (e.key === 'Escape') closeAllDrawers();
    }});

    function showToast(msg) {{
      toastMsg.innerText = msg;
      liveToast.classList.add('show');
      setTimeout(() => liveToast.classList.remove('show'), 2400);
    }}

    document.getElementById('btnCacheAll').onclick = async () => {{
      const btn = document.getElementById('btnCacheAll');
      const text = document.getElementById('cacheAllText');
      btn.disabled = true;
      text.innerText = "Đang tải dữ liệu {total_ch} chương...";

      try {{
        const urlsToCache = [
          './',
          './index.html',
          './data/chapters.json',
          './icon.svg',
          './manifest.json',
          './assets/logo.webp',
          './assets/cover_vertical.webp',
          './assets/hero_horizontal.webp'
        ];
        for (let i = 1; i <= totalChapters; i++) {{
          urlsToCache.push(`./chuong-${{i}}/`);
        }}

        if ('caches' in window) {{
          const cache = await caches.open('pha-troi-v5-complete');
          let count = 0;
          for (const url of urlsToCache) {{
            try {{
              const res = await fetch(url);
              if (res.ok) await cache.put(url, res);
              count++;
              text.innerText = `Đang lưu offline: ${{count}}/${{urlsToCache.length}}...`;
            }} catch (e) {{}}
          }}
          text.innerText = `Đã lưu xong ${{count}} tập tin offline!`;
          showToast(`✨ Đã tải trọn bộ offline thành công!`);
        }} else {{
          text.innerText = "Trình duyệt không hỗ trợ Cache Storage";
        }}
      }} catch (err) {{
        text.innerText = "Lỗi khi lưu offline";
      }} finally {{
        setTimeout(() => {{
          btn.disabled = false;
          text.innerText = "Tải Toàn Bộ {total_ch} Chương Để Đọc Offline";
        }}, 3500);
      }}
    }};

    loadChaptersIndex();

    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', () => {{
        navigator.serviceWorker.register('./sw.js').catch(() => {{}});
      }});
    }}
  </script>
</body>
</html>"""

def generate_chapter_html(ch_info, chapters_index, total_words):
    ch_num = ch_info["chapter"]
    clean_title = ch_info["title"].replace(f"Chương {ch_num}:", "").strip()
    clean_title = re.sub(r"^Chương\s+\d+:\s*", "", clean_title, flags=re.IGNORECASE)
    vol = ch_info.get("volume", 1)
    arc = ch_info.get("arc", 1)
    words = ch_info.get("word_count", 2500)
    read_mins = max(1, round(words / 300))
    total_ch = len(chapters_index)
    shared_css = get_shared_css()

    prev_url = f"../chuong-{ch_num - 1}/" if ch_num > 1 else "javascript:void(0)"
    prev_dis = "disabled" if ch_num <= 1 else ""
    next_url = f"../chuong-{ch_num + 1}/" if ch_num < total_ch else "javascript:void(0)"
    next_dis = "disabled" if ch_num >= total_ch else ""

    toc_items_html = []
    for c in chapters_index:
        active_cls = "active" if c["chapter"] == ch_num else ""
        c_title = c["title"].replace(f"Chương {c['chapter']}:", "").strip()
        c_title = re.sub(r"^Chương\s+\d+:\s*", "", c_title, flags=re.IGNORECASE)
        toc_items_html.append(f"""
          <a href="../chuong-{c['chapter']}/" class="toc-item {active_cls}">
            <div class="toc-info">
              <div class="toc-num">Hồi {c['arc']} • Chương {c['chapter']}</div>
              <div class="toc-name">{c_title}</div>
            </div>
            <span class="toc-meta">{c['word_count']:,} từ</span>
          </a>
        """)
    toc_list_rendered = "".join(toc_items_html)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Phá Trời — Chương {ch_num}: {clean_title}</title>
  
  <meta name="title" content="Phá Trời — Chương {ch_num}: {clean_title}">
  <meta name="description" content="Đọc Chương {ch_num}: {clean_title} — Quyển {vol}, Hồi {arc} ({words:,} từ). {ch_info.get('excerpt', '')}">
  <meta name="author" content="An Bình">
  
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://bon-231900.github.io/pha-troi/chuong-{ch_num}/">
  <meta property="og:title" content="Phá Trời — Chương {ch_num}: {clean_title}">
  <meta property="og:description" content="Đọc Chương {ch_num}: {clean_title} — Đô thị tu chân Sài Gòn 2026.">
  <meta property="og:image" content="https://bon-231900.github.io/pha-troi/assets/cover_vertical.jpg">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Phá Trời — Chương {ch_num}: {clean_title}">
  <meta name="twitter:description" content="Đọc Chương {ch_num}: {clean_title} ({words:,} từ) — Đô thị tu chân Sài Gòn 2026.">
  <meta name="twitter:image" content="https://bon-231900.github.io/pha-troi/assets/hero_horizontal.jpg">

  <link rel="manifest" href="../manifest.json">
  <link rel="icon" href="../assets/logo.webp" type="image/webp">
  <link rel="apple-touch-icon" href="../assets/logo.webp">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Phá Trời">
  <meta name="theme-color" content="#07090e">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <style>
    {shared_css}

    /* Reader View Specific Layout */
    .app-layout {{ display: flex; max-width: 1400px; margin: 0 auto; position: relative; }}

    .desktop-toc-sidebar {{
      display: none; width: 280px; height: calc(100vh - 60px); position: sticky; top: 60px;
      overflow-y: auto; border-right: 1px solid var(--border-color); padding: 18px 12px;
      background: rgba(0,0,0,0.15); flex-shrink: 0;
    }}
    @media (min-width: 1200px) {{ .desktop-toc-sidebar {{ display: block; }} }}

    .main-reader {{
      flex: 1; min-width: 0; padding: 24px 20px 100px 20px;
      display: flex; flex-direction: column; align-items: center;
    }}

    .btn-back-home-wrap {{
      width: 100%; max-width: var(--reader-max-width); display: flex; align-items: center;
      justify-content: space-between; margin-bottom: 18px;
    }}
    .btn-back-home {{
      display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 8px;
      background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-muted);
      font-size: 12.5px; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .btn-back-home:hover {{ color: var(--gold-primary); border-color: var(--gold-primary); }}

    .chapter-hero {{
      width: 100%; max-width: var(--reader-max-width); text-align: center;
      padding: 24px 0 28px 0; border-bottom: 1px solid var(--border-color); margin-bottom: 32px;
    }}
    .chapter-vol-arc {{
      font-size: 12px; font-weight: 800; color: var(--accent-primary); letter-spacing: 2px;
      text-transform: uppercase; margin-bottom: 8px;
    }}
    .chapter-main-title {{
      font-family: 'Lora', 'Georgia', serif; font-size: 28px; font-weight: 800; line-height: 1.35;
      color: var(--gold-primary); margin: 0 0 12px 0;
    }}
    .chapter-meta-line {{
      display: flex; align-items: center; justify-content: center; gap: 12px; font-size: 12.5px; color: var(--text-muted);
    }}

    .novel-body {{
      width: 100%; max-width: var(--reader-max-width); font-size: var(--font-size);
      line-height: var(--reader-line-height); color: var(--text-color); letter-spacing: 0.2px;
      transition: font-size 0.2s ease, max-width 0.2s ease, line-height 0.2s ease;
    }}
    .novel-body p {{ margin-bottom: 1.6em; text-align: justify; text-justify: inter-word; }}
    .novel-body blockquote {{
      border-left: 3px solid var(--gold-primary); padding: 8px 16px; margin: 1.6em 0;
      background: var(--card-bg); border-radius: 0 8px 8px 0; font-style: italic;
    }}
    .novel-body hr {{
      border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--border-color), transparent); margin: 2.5em 0;
    }}

    .chapter-footer-nav {{
      width: 100%; max-width: var(--reader-max-width); display: flex; align-items: center;
      justify-content: space-between; gap: 12px; margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border-color);
    }}
    .btn-nav-chapter {{
      flex: 1; padding: 13px; border-radius: 12px; background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); font-size: 14px; font-weight: 600; cursor: pointer; display: inline-flex;
      align-items: center; justify-content: center; gap: 8px; transition: all 0.2s ease; text-decoration: none;
    }}
    .btn-nav-chapter:hover:not(.disabled) {{
      border-color: var(--accent-primary); color: var(--accent-primary); background: var(--card-bg-hover);
    }}
    .btn-nav-chapter.disabled {{ opacity: 0.35; cursor: not-allowed; pointer-events: none; }}

    .desktop-nav-float {{
      display: none; position: fixed; top: 50%; transform: translateY(-50%); z-index: 800;
    }}
    .desktop-nav-left {{ left: 24px; }}
    .desktop-nav-right {{ right: 24px; }}
    @media (min-width: 1024px) {{ .desktop-nav-float {{ display: flex; flex-direction: column; align-items: center; }} }}
    .btn-float-nav {{
      width: 48px; height: 48px; border-radius: 50%; background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); cursor: pointer; display: flex; align-items: center; justify-content: center;
      box-shadow: 0 6px 18px rgba(0,0,0,0.25); transition: all 0.2s; text-decoration: none;
    }}
    .btn-float-nav:hover:not(.disabled) {{ border-color: var(--gold-primary); color: var(--gold-primary); transform: scale(1.1); }}
    .btn-float-nav.disabled {{ opacity: 0.3; cursor: not-allowed; pointer-events: none; }}

    .bottom-bar {{
      position: fixed; bottom: 0; left: 0; right: 0; height: 58px; background: var(--header-bg);
      backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-top: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-around; z-index: 998; transition: transform 0.25s ease;
    }}
    @media (min-width: 769px) {{ .bottom-bar {{ display: none; }} }}
    .btn-bottom-item {{
      background: none; border: none; color: var(--text-muted); display: flex; flex-direction: column;
      align-items: center; gap: 3px; font-size: 10px; font-weight: 600; cursor: pointer; padding: 6px 12px;
      border-radius: 8px; text-decoration: none;
    }}
    .btn-bottom-item:active {{ color: var(--gold-primary); }}
    .btn-bottom-item.disabled {{ opacity: 0.3; pointer-events: none; }}
    .btn-bottom-item svg {{ width: 20px; height: 20px; }}
  </style>
</head>
<body class="theme-peaceful-dark">

  <div id="progressBarContainer"><div id="progressBar"></div></div>

  <!-- HEADER -->
  <header id="topHeader">
    <div class="header-left">
      <a href="../" class="btn-brand" title="Về Trang Chủ Phá Trời (H)">
        <picture>
          <source srcset="../assets/logo.webp" type="image/webp">
          <img src="../assets/logo.jpg" class="nav-logo" alt="Phá Trời">
        </picture>
        <span class="nav-brand-text">PHÁ TRỜI</span>
        <span class="nav-live-badge"><span class="dot-live"></span> {total_ch} CHƯƠNG</span>
      </a>
    </div>

    <div class="header-center">
      <h1 class="header-title">Chương {ch_num}: {clean_title}</h1>
      <p class="header-sub">Quyển {vol} • Hồi {arc} • {words:,} từ</p>
    </div>

    <div class="header-right">
      <a href="../" class="btn-nav-home-pill" title="Trở về Trang Chủ">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>
        <span>Trang Chủ</span>
      </a>

      <button class="btn-icon" id="btnMenu" title="Mục Lục Chương (M)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      
      <button class="btn-icon" id="btnCodex" title="Codex Phá Trời — Bách Khoa Thế Giới (C)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
      </button>

      <button class="btn-icon" id="btnAmbient" title="Âm thanh Mưa Đêm Sài Gòn (Thư giãn)">
        <svg id="iconAudioOff" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>
        <svg id="iconAudioOn" style="display:none; color:var(--accent-primary);" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
      </button>

      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Nhanh Sáng / Tối (T)">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg id="iconSun" style="display:none;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button class="btn-icon" id="btnSettings" title="Cài Đặt Đọc Truyện">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
      </button>
    </div>
  </header>

  <!-- CHAPTER READER CONTENT -->
  <div class="app-layout">
    <!-- Desktop Persistent Sidebar -->
    <aside class="desktop-toc-sidebar">
      <div style="font-size:13px; font-weight:700; color:var(--gold-primary); margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
        <span>DANH MỤC CHƯƠNG</span>
        <span>{total_ch} chương</span>
      </div>
      <div>{toc_list_rendered}</div>
    </aside>

    <!-- Floating Nav Arrows -->
    <div class="desktop-nav-float desktop-nav-left">
      <a href="{prev_url}" class="btn-float-nav {prev_dis}" title="Chương trước (Phím ←)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
      </a>
    </div>
    <div class="desktop-nav-float desktop-nav-right">
      <a href="{next_url}" class="btn-float-nav {next_dis}" title="Chương sau (Phím →)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </a>
    </div>

    <!-- Main Reader Content -->
    <main class="main-reader">
      <div class="btn-back-home-wrap">
        <a href="../" class="btn-back-home">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
          <span>Về Trang Chủ Phá Trời</span>
        </a>
        <div style="font-size:12px; color:var(--text-muted);">QUYỂN {vol} • HỒI {arc}</div>
      </div>

      <section class="chapter-hero">
        <div class="chapter-vol-arc">QUYỂN {vol} • HỒI {arc}</div>
        <h1 class="chapter-main-title">Chương {ch_num}: {clean_title}</h1>
        <div class="chapter-meta-line">
          <span>📖 {words:,} từ</span>
          <span>•</span>
          <span>⏱️ ~{read_mins} phút đọc</span>
          {f"<span>•</span><span>📍 {ch_info['location']}</span>" if ch_info.get('location') else ""}
        </div>
      </section>

      <article class="novel-body" id="novelContent">
        {ch_info["html"]}
      </article>

      <div class="chapter-footer-nav">
        <a href="{prev_url}" class="btn-nav-chapter {prev_dis}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
          Chương Trước
        </a>
        <a href="../" class="btn-nav-chapter" style="flex:0.6;">Trang Chủ</a>
        <a href="{next_url}" class="btn-nav-chapter {next_dis}">
          Chương Sau
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </a>
      </div>
    </main>
  </div>

  <!-- Mobile Bottom Floating Nav -->
  <nav class="bottom-bar">
    <a href="../" class="btn-bottom-item">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>
      <span>Trang Chủ</span>
    </a>
    <a href="{prev_url}" class="btn-bottom-item {prev_dis}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
      <span>Trước</span>
    </a>
    <button class="btn-bottom-item" id="btnMobileToc">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      <span>Mục Lục</span>
    </button>
    <a href="{next_url}" class="btn-bottom-item {next_dis}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
      <span>Sau</span>
    </a>
    <button class="btn-bottom-item" id="btnMobileSettings">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
      <span>Cài Đặt</span>
    </button>
  </nav>

  <div class="modal-overlay" id="modalOverlay"></div>

  <!-- TOC DRAWER -->
  <aside class="drawer drawer-left" id="drawerToc">
    <div class="drawer-header">
      <h2 class="drawer-title">MỤC LỤC TIỂU THUYẾT</h2>
      <button class="btn-icon" id="btnCloseToc">✕</button>
    </div>
    <div class="drawer-search">
      <input type="text" id="inputTocSearch" class="search-input" placeholder="Tìm chương hoặc từ khóa...">
    </div>
    <div class="drawer-body" id="tocDrawerList">
      {toc_list_rendered}
    </div>
  </aside>

  <!-- CODEX DRAWER -->
  <aside class="drawer drawer-right" id="drawerCodex">
    <div class="drawer-header">
      <h2 class="drawer-title">CODEX PHÁ TRỜI</h2>
      <button class="btn-icon" id="btnCloseCodex">✕</button>
    </div>
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" id="tabCodexChar" data-codex="char">Nhân Vật</button>
      <button class="drawer-tab-btn" id="tabCodexItem" data-codex="item">Kho Cổ Vật</button>
      <button class="drawer-tab-btn" id="tabCodexLotus" data-codex="lotus">Thức Hải</button>
    </div>
    <div class="drawer-body" id="codexDrawerBody"></div>
  </aside>

  <!-- SETTINGS BOTTOM SHEET -->
  <aside class="sheet-bottom" id="settingsSheet">
    <div class="sheet-handle"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <h3 style="font-size:16px; font-weight:700; color:var(--gold-primary); margin:0;">TÙY CHỈNH ĐỌC TRUYỆN</h3>
      <button class="btn-icon" id="btnCloseSettings" style="width:32px; height:32px;">✕</button>
    </div>
    <div class="setting-group">
      <div class="setting-label">Chủ Đề Giao Diện</div>
      <div class="theme-grid">
        <div class="theme-opt active" data-theme="theme-peaceful-dark" style="background:#07090e; color:#d6dce7;">Tối Bình Yên</div>
        <div class="theme-opt" data-theme="theme-gentle-light" style="background:#f7f5f0; color:#24221f;">Sáng Thanh Nhã</div>
        <div class="theme-opt" data-theme="theme-oled" style="background:#000000; color:#cbd5e1;">OLED Đen</div>
        <div class="theme-opt" data-theme="theme-sepia" style="background:#f4edd8; color:#3b2d1d;">Sepia Cổ Điển</div>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Cỡ Chữ Đọc</div>
      <div class="stepper-ctrl">
        <button class="btn-step" id="btnFontDec">A-</button>
        <span class="stepper-val" id="fontSizeVal">19px</span>
        <button class="btn-step" id="btnFontInc">A+</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Độ Rộng Khung Đọc</div>
      <div class="btn-opt-group">
        <button class="btn-opt-step" data-opt-width="640">Hẹp (640px)</button>
        <button class="btn-opt-step active" data-opt-width="760">Chuẩn (760px)</button>
        <button class="btn-opt-step" data-opt-width="900">Rộng (900px)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Khoảng Cách Dòng</div>
      <div class="btn-opt-group">
        <button class="btn-opt-step" data-opt-lh="1.65">Gọn (1.65)</button>
        <button class="btn-opt-step active" data-opt-lh="1.85">Chuẩn (1.85)</button>
        <button class="btn-opt-step" data-opt-lh="2.1">Thoáng (2.1)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Phông Chữ</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
        <button class="btn-step" id="btnFontSerif" style="width:100%; font-family:serif;">Có Chân (Lora)</button>
        <button class="btn-step" id="btnFontSans" style="width:100%; font-family:sans-serif;">Không Chân (Be Vietnam)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Âm Thanh Thư Giãn (Mưa Đêm Sài Gòn)</div>
      <div class="ambient-widget">
        <button class="btn-icon" id="btnSheetAudioToggle" style="background:var(--card-bg);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
        </button>
        <input type="range" id="audioVolume" min="0" max="1" step="0.05" value="0.25" style="flex:1; margin:0 12px; accent-color:var(--accent-primary);">
        <span id="audioVolVal" style="font-size:12px; color:var(--text-muted); width:32px;">25%</span>
      </div>
    </div>
  </aside>

  <div id="liveToast"><span class="dot-live"></span><span id="toastMsg">Thông báo</span></div>

  <script>
    // 1. Lưu tiến độ đọc tức thì vào localStorage
    localStorage.setItem('pha_troi_cur_ch', '{ch_num}');

    // 2. Scroll Progress Bar
    window.addEventListener('scroll', () => {{
      const totalH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = totalH > 0 ? (window.scrollY / totalH) * 100 : 0;
      document.getElementById('progressBar').style.width = pct + '%';
    }});

    // 3. Web Audio Synthesizer (Pink Noise Rain)
    let audioCtx = null, noiseNode = null, gainNode = null, filterNode = null;
    let isRainPlaying = false, rainVolume = 0.25;

    function initAudio() {{
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }}

    function toggleRainSound() {{
      if (isRainPlaying) {{ stopRainSound(); showToast('🌧️ Đã tắt âm thanh mưa'); }}
      else {{ startRainSound(); showToast('🌧️ Bật âm thanh mưa đêm Sài Gòn (Thư giãn)'); }}
      updateAudioIcons();
    }}

    function startRainSound() {{
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      if (noiseNode) return;
      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < bufferSize; i++) {{
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.045;
        b6 = white * 0.115926;
      }}
      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = noiseBuffer;
      noiseNode.loop = true;
      filterNode = audioCtx.createBiquadFilter();
      filterNode.type = 'lowpass';
      filterNode.frequency.value = 750;
      gainNode = audioCtx.createGain();
      gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
      noiseNode.connect(filterNode);
      filterNode.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      noiseNode.start();
      isRainPlaying = true;
    }}

    function stopRainSound() {{
      if (noiseNode) {{
        try {{ noiseNode.stop(); noiseNode.disconnect(); }} catch (e) {{}}
        noiseNode = null;
      }}
      isRainPlaying = false;
    }}

    function updateAudioIcons() {{
      const offIcon = document.getElementById('iconAudioOff');
      const onIcon = document.getElementById('iconAudioOn');
      if (isRainPlaying) {{
        if (offIcon) offIcon.style.display = 'none';
        if (onIcon) onIcon.style.display = 'inline-block';
      }} else {{
        if (offIcon) offIcon.style.display = 'inline-block';
        if (onIcon) onIcon.style.display = 'none';
      }}
    }}

    document.getElementById('btnAmbient').onclick = toggleRainSound;
    document.getElementById('btnSheetAudioToggle').onclick = toggleRainSound;
    document.getElementById('audioVolume').oninput = (e) => {{
      rainVolume = parseFloat(e.target.value);
      document.getElementById('audioVolVal').innerText = Math.round(rainVolume * 100) + '%';
      if (gainNode && audioCtx) gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
    }};

    // 4. Modals & Drawers
    const modalOverlay = document.getElementById('modalOverlay');
    const drawerToc = document.getElementById('drawerToc');
    const drawerCodex = document.getElementById('drawerCodex');
    const settingsSheet = document.getElementById('settingsSheet');
    const codexDrawerBody = document.getElementById('codexDrawerBody');
    const liveToast = document.getElementById('liveToast');
    const toastMsg = document.getElementById('toastMsg');
    let activeCodexTab = 'char';

    function closeAllDrawers() {{
      modalOverlay.classList.remove('open');
      drawerToc.classList.remove('open');
      drawerCodex.classList.remove('open');
      settingsSheet.classList.remove('open');
    }}

    function openToc() {{
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerToc.classList.add('open');
    }}

    function openCodex() {{
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerCodex.classList.add('open');
      renderCodexDrawer({ch_num});
    }}

    function openSettings() {{
      closeAllDrawers();
      modalOverlay.classList.add('open');
      settingsSheet.classList.add('open');
    }}

    modalOverlay.onclick = closeAllDrawers;
    document.getElementById('btnMenu').onclick = openToc;
    const btnMobToc = document.getElementById('btnMobileToc');
    if (btnMobToc) btnMobToc.onclick = openToc;
    document.getElementById('btnCloseToc').onclick = closeAllDrawers;

    document.getElementById('btnCodex').onclick = openCodex;
    document.getElementById('btnCloseCodex').onclick = closeAllDrawers;

    document.getElementById('btnSettings').onclick = openSettings;
    const btnMobSet = document.getElementById('btnMobileSettings');
    if (btnMobSet) btnMobSet.onclick = openSettings;
    document.getElementById('btnCloseSettings').onclick = closeAllDrawers;

    // Filter in Chapter TOC drawer
    document.getElementById('inputTocSearch').oninput = (e) => {{
      const val = e.target.value.toLowerCase().trim();
      document.querySelectorAll('#tocDrawerList .toc-item').forEach(item => {{
        const text = item.innerText.toLowerCase();
        item.style.display = (!val || text.includes(val)) ? 'flex' : 'none';
      }});
    }};

    // Progressive Codex Drawer
    function renderCodexDrawer(s) {{
      let html = '';
      if (activeCodexTab === 'char') {{
        if (s >= 20) {{
          html = `
            <div class="codex-card">
              <span class="codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
              <h3 class="codex-title">Nguyễn Minh An (25 tuổi)</h3>
              <p class="codex-desc">Luyện Cốt Trung kỳ (Cốt Nhược Kim Thạch). Đúc cốt ngự kình, kình lực vạn cân, Thức Hải Thanh Liên bảo bọc tâm mạch.</p>
              <div class="codex-stat"><span>Cơ Quan</span><span class="codex-stat-val">Viện Địa Tầng Đô Thị</span></div>
              <div class="codex-stat"><span>Cảnh Giới</span><span class="codex-stat-val">Luyện Cốt Trung Kỳ</span></div>
            </div>
          `;
        }} else {{
          html = `
            <div class="codex-card">
              <span class="codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
              <h3 class="codex-title">Nguyễn Minh An (24 tuổi)</h3>
              <p class="codex-desc">Nhân viên văn phòng bình thường tại TP.HCM. Bắt đầu con đường Thể Đạo từ số 0 sau biến cố trên cầu Sài Gòn.</p>
              <div class="codex-stat"><span>Cảnh Giới</span><span class="codex-stat-val">Phàm Thể (Tẩy Tủy Hoán Cốt)</span></div>
            </div>
          `;
        }}
      }} else if (activeCodexTab === 'item') {{
        if (s >= 15) {{
          html += `
            <div class="codex-card">
              <span class="codex-badge">VŨ KHÍ CHÍNH</span>
              <h3 class="codex-title">Hắc Thiết Đoản Côn</h3>
              <p class="codex-desc">Thép nhíp Zil tôi dầu cám chu sa thạch anh do bác Sáu Kiên và Minh An rèn. Dài 52cm, nặng 3.2kg, dẫn truyền Kính Kình.</p>
            </div>
          `;
        }} else {{
          html += `
            <div class="codex-card locked">
              <span class="codex-badge locked-badge">🔒 KHÍ BINH ẨN</span>
              <h3 class="codex-title" style="color:var(--text-muted);">Hắc Thiết Đoản Côn</h3>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương 15 để mở khóa chi tiết</div>
            </div>
          `;
        }}

        if (s >= 25) {{
          html += `
            <div class="codex-card">
              <span class="codex-badge">CỔ KHÍ TRẤN THỦY</span>
              <h3 class="codex-title">Trấn Thủy Đoản Đao</h3>
              <p class="codex-desc">Thanh đoản đao đồng thau cổ niên đại địa chất > 2.5 triệu năm, cọc tiêu chốt chặn Thủy Môn Tiêu rạch Lò Gốm.</p>
            </div>
          `;
        }} else {{
          html += `
            <div class="codex-card locked">
              <span class="codex-badge locked-badge">🔒 CỔ VẬT ẨN</span>
              <h3 class="codex-title" style="color:var(--text-muted);">Trấn Thủy Đoản Đao</h3>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương 25 để mở khóa chi tiết</div>
            </div>
          `;
        }}
      }} else if (activeCodexTab === 'lotus') {{
        if (s >= 10) {{
          html = `
            <div class="codex-card">
              <span class="codex-badge">NỮ CHÍNH • THỨC HẢI</span>
              <h3 class="codex-title">Lâm Tịch (Bạch Y Tiên Tử)</h3>
              <p class="codex-desc">Nguyên Thần Tàn Phiến viễn cổ 2.5 triệu năm. Ngủ say trên Thanh Liên Đài ngọc bích bảo bọc tâm thức của Minh An.</p>
            </div>
          `;
        }} else {{
          html = `
            <div class="codex-card locked">
              <span class="codex-badge locked-badge">🔒 BÍ ẨN THỨC HẢI</span>
              <h3 class="codex-title" style="color:var(--text-muted);">Tàn Niệm Cổ Xưa</h3>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương 10 để mở khóa danh tính</div>
            </div>
          `;
        }}
      }}
      codexDrawerBody.innerHTML = html;
    }}

    ['tabCodexChar', 'tabCodexItem', 'tabCodexLotus'].forEach(id => {{
      const btn = document.getElementById(id);
      if (btn) btn.onclick = () => {{
        ['tabCodexChar', 'tabCodexItem', 'tabCodexLotus'].forEach(b => document.getElementById(b)?.classList.remove('active'));
        btn.classList.add('active');
        activeCodexTab = btn.dataset.codex;
        renderCodexDrawer({ch_num});
      }};
    }});

    // 5. Settings Handlers
    const THEMES = ['theme-peaceful-dark', 'theme-gentle-light', 'theme-oled', 'theme-sepia'];
    function setTheme(theme) {{
      THEMES.forEach(t => {{
        document.documentElement.classList.remove(t);
        document.body.classList.remove(t);
      }});
      document.documentElement.classList.add(theme);
      document.body.classList.add(theme);

      document.querySelectorAll('.theme-opt').forEach(opt => {{
        opt.classList.toggle('active', opt.dataset.theme === theme);
      }});

      const sunIcon = document.getElementById('iconSun');
      const moonIcon = document.getElementById('iconMoon');
      if (theme === 'theme-gentle-light') {{
        if (sunIcon) sunIcon.style.display = 'inline-block';
        if (moonIcon) moonIcon.style.display = 'none';
      }} else {{
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) moonIcon.style.display = 'inline-block';
      }}
      localStorage.setItem('pha_troi_theme', theme);
    }}

    document.querySelectorAll('.theme-opt').forEach(opt => {{
      opt.onclick = () => {{
        setTheme(opt.dataset.theme);
        showToast('🎨 Đã chuyển giao diện: ' + opt.innerText.trim());
      }};
    }});

    document.getElementById('btnQuickTheme').onclick = () => {{
      const isLight = document.body.classList.contains('theme-gentle-light');
      const target = isLight ? 'theme-peaceful-dark' : 'theme-gentle-light';
      setTheme(target);
      showToast(target === 'theme-gentle-light' ? '☀️ Đã bật giao diện Sáng' : '🌙 Đã bật giao diện Tối');
    }};

    const savedTheme = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
    setTheme(savedTheme);

    let curFontSize = parseInt(localStorage.getItem('pha_troi_font_size') || '19');
    function applyFontSize(size) {{
      curFontSize = Math.max(15, Math.min(26, size));
      document.documentElement.style.setProperty('--font-size', curFontSize + 'px');
      document.getElementById('fontSizeVal').innerText = curFontSize + 'px';
      localStorage.setItem('pha_troi_font_size', curFontSize);
    }}
    document.getElementById('btnFontDec').onclick = () => applyFontSize(curFontSize - 1);
    document.getElementById('btnFontInc').onclick = () => applyFontSize(curFontSize + 1);
    applyFontSize(curFontSize);

    function applyReaderWidth(w) {{
      document.documentElement.style.setProperty('--reader-max-width', w + 'px');
      localStorage.setItem('pha_troi_reader_width', w);
      document.querySelectorAll('.btn-opt-step[data-opt-width]').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.optWidth === String(w));
      }});
    }}
    document.querySelectorAll('.btn-opt-step[data-opt-width]').forEach(btn => {{
      btn.onclick = () => {{
        applyReaderWidth(parseInt(btn.dataset.optWidth));
        showToast('📏 Khung đọc: ' + btn.innerText.trim());
      }};
    }});
    const savedWidth = parseInt(localStorage.getItem('pha_troi_reader_width') || '760');
    applyReaderWidth(savedWidth);

    function applyLineHeight(lh) {{
      document.documentElement.style.setProperty('--reader-line-height', lh);
      localStorage.setItem('pha_troi_line_height', lh);
      document.querySelectorAll('.btn-opt-step[data-opt-lh]').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.optLh === String(lh));
      }});
    }}
    document.querySelectorAll('.btn-opt-step[data-opt-lh]').forEach(btn => {{
      btn.onclick = () => {{
        applyLineHeight(parseFloat(btn.dataset.optLh));
        showToast('📄 Giãn dòng: ' + btn.innerText.trim());
      }};
    }});
    const savedLh = parseFloat(localStorage.getItem('pha_troi_line_height') || '1.85');
    applyLineHeight(savedLh);

    const FONT_SERIF = "'Lora', 'Georgia', serif";
    const FONT_SANS = "'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif";
    document.getElementById('btnFontSerif').onclick = () => {{
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
      localStorage.setItem('pha_troi_font_family', 'serif');
      showToast('📖 Phông chữ Có Chân (Lora)');
    }};
    document.getElementById('btnFontSans').onclick = () => {{
      document.documentElement.style.setProperty('--font-family', FONT_SANS);
      document.body.style.setProperty('--font-family', FONT_SANS);
      localStorage.setItem('pha_troi_font_family', 'sans');
      showToast('📱 Phông chữ Không Chân (Be Vietnam Pro)');
    }};

    const savedFont = localStorage.getItem('pha_troi_font_family');
    if (savedFont === 'serif') {{
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
    }}

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {{
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowLeft') {{
        const prevBtn = document.querySelector('.desktop-nav-left a');
        if (prevBtn && !prevBtn.classList.contains('disabled')) window.location.href = prevBtn.href;
      }} else if (e.key === 'ArrowRight') {{
        const nextBtn = document.querySelector('.desktop-nav-right a');
        if (nextBtn && !nextBtn.classList.contains('disabled')) window.location.href = nextBtn.href;
      }} else if (e.key.toLowerCase() === 'h') {{
        window.location.href = '../';
      }} else if (e.key.toLowerCase() === 't') {{
        document.getElementById('btnQuickTheme').click();
      }} else if (e.key.toLowerCase() === 'm') {{
        openToc();
      }} else if (e.key.toLowerCase() === 'c') {{
        openCodex();
      }} else if (e.key === 'Escape') {{
        closeAllDrawers();
      }}
    }});

    function showToast(msg) {{
      toastMsg.innerText = msg;
      liveToast.classList.add('show');
      setTimeout(() => liveToast.classList.remove('show'), 2400);
    }}
  </script>
</body>
</html>"""

def generate_sw():
    return """// Service Worker v6 cho Web Reader Phá Trời
const CACHE_NAME = 'pha-troi-reader-v6';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './404.html',
  './manifest.json',
  './icon.svg',
  './cover.svg',
  './assets/logo.webp',
  './assets/cover_vertical.webp',
  './assets/hero_horizontal.webp',
  './data/chapters.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
        }
        return networkResponse;
      }).catch(() => {
        if (e.request.destination === 'document') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
"""

def build():
    print(f"[*] Bat dau bien dich Web App tinh Pha Troi v2.3 (Clean Slugs) tai: {DIST_DIR}")
    os.makedirs(DIST_DIR, exist_ok=True)
    data_dir = os.path.join(DIST_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. Parse all chapters
    manuscript_dir = os.path.join(BASE_DIR, "manuscript", "markdown")
    chapter_paths = []
    for root, _, flist in os.walk(manuscript_dir):
        for f in flist:
            if f.endswith(".md") and f.startswith("ch_"):
                chapter_paths.append(os.path.join(root, f))
    
    def extract_ch(p):
        m = re.search(r'ch_(\d+)', os.path.basename(p))
        return int(m.group(1)) if m else 9999
    
    chapter_paths.sort(key=extract_ch)

    chapters_index = []
    parsed_chapters = []
    total_words = 0
    for path in chapter_paths:
        info = parse_chapter_file(path)
        total_words += info["word_count"]
        parsed_chapters.append(info)
        
        # Save json for api / backward compat
        ch_json_path = os.path.join(data_dir, f"chapter_{info['chapter']}.json")
        with open(ch_json_path, "w", encoding="utf-8") as out:
            json.dump(info, out, ensure_ascii=False, indent=1)
            
        chapters_index.append({
            "chapter": info["chapter"],
            "title": info["title"],
            "volume": info["volume"],
            "arc": info["arc"],
            "word_count": info["word_count"],
            "date": info["date"],
            "location": info["location"]
        })

    index_data = {
        "title": "Phá Trời (Phá Toái Thần Hoang)",
        "author": "An Bình",
        "total": len(chapters_index),
        "total_words": total_words,
        "updated_at": "2026-09-15T19:25:00+07:00",
        "chapters": chapters_index
    }
    with open(os.path.join(data_dir, "chapters.json"), "w", encoding="utf-8") as out:
        json.dump(index_data, out, ensure_ascii=False, indent=1)

    # 2. Copy static assets to dist/assets
    src_assets = os.path.join(STATIC_SRC_DIR, "assets")
    dst_assets = os.path.join(DIST_DIR, "assets")
    if os.path.exists(src_assets):
        if os.path.exists(dst_assets):
            shutil.rmtree(dst_assets)
        shutil.copytree(src_assets, dst_assets)
        print(f"  [+] Copied assets to {dst_assets}")

    # 3. Generate root index.html (Homepage)
    home_html = generate_home_html(chapters_index, total_words)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as out:
        out.write(home_html)
    print("  [+] Generated dist/index.html")

    # 4. Generate Clean Slug Directory for each chapter: dist/chuong-X/index.html
    for ch_info in parsed_chapters:
        ch_slug_dir = os.path.join(DIST_DIR, f"chuong-{ch_info['chapter']}")
        os.makedirs(ch_slug_dir, exist_ok=True)
        ch_html = generate_chapter_html(ch_info, chapters_index, total_words)
        with open(os.path.join(ch_slug_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(ch_html)
    print(f"  [+] Generated {len(parsed_chapters)} Clean Slug chapter pages: dist/chuong-X/index.html")

    # 5. Generate 404.html for smart redirection
    with open(os.path.join(DIST_DIR, "404.html"), "w", encoding="utf-8") as out:
        out.write(generate_404_html())
    print("  [+] Generated dist/404.html")

    # 6. Generate sw.js
    with open(os.path.join(DIST_DIR, "sw.js"), "w", encoding="utf-8") as out:
        out.write(generate_sw())

    # 7. Generate cover.svg
    cover_svg_content = generate_cover_svg()
    with open(os.path.join(DIST_DIR, "cover.svg"), "w", encoding="utf-8") as out:
        out.write(cover_svg_content)

    # 8. Generate manifest.json
    manifest_data = {
        "name": "Phá Trời — Tiểu Thuyết Đô Thị Tu Chân",
        "short_name": "Phá Trời",
        "description": "Ứng dụng đọc tiểu thuyết trọn bộ thời gian thực cho Phá Trời",
        "start_url": "./index.html",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#07090e",
        "theme_color": "#07090e",
        "icons": [
            {
                "src": "./assets/logo.webp",
                "sizes": "512x512",
                "type": "image/webp",
                "purpose": "any maskable"
            },
            {
                "src": "./icon.svg",
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            }
        ]
    }
    with open(os.path.join(DIST_DIR, "manifest.json"), "w", encoding="utf-8") as out:
        json.dump(manifest_data, out, ensure_ascii=False, indent=2)

    # 9. Copy icon.svg
    src_icon = os.path.join(STATIC_SRC_DIR, "icon.svg")
    dst_icon = os.path.join(DIST_DIR, "icon.svg")
    if os.path.exists(src_icon):
        shutil.copy2(src_icon, dst_icon)

    print(f"[Build Complete] {len(chapters_index)} chuong ({total_words:,} tu) Clean Slugs -> {DIST_DIR}")
    return len(chapters_index), total_words

if __name__ == "__main__":
    build()
