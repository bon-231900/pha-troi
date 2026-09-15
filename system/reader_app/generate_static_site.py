# -*- coding: utf-8 -*-
"""
NovelOS — Trình biên dịch Web Reader PWA cao cấp cho tiểu thuyết 'Phá Trời'
Hỗ trợ:
- 2 Giao diện chủ đạo: Tối Bình Yên (Peaceful Dark) & Sáng Nhẹ Nhàng (Gentle Light)
- Tương thích hoàn hảo Desktop (Màn hình rộng + Phím tắt) & Mobile (Touch + PWA Offline)
- Bách khoa toàn thư tương tác (Codex): Hồ sơ Minh An, Kho Bảo Vật, Đài Sen Lâm Tịch
- Bộ tổng hợp âm thanh thư giãn Web Audio API (Mưa đêm Sài Gòn & Sóng nước ven sông)
- Bộ lọc mục lục theo Hồi 1 & Hồi 2, thanh cuộn nhảy nhanh chương
- Thẻ Open Graph / Social Media Preview chuẩn mực
"""
import os
import re
import sys
import json
import shutil
import markdown

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path

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
    
    ch_num = int(meta.get("chapter", fallback_num))
    return {
        "chapter": ch_num,
        "title": title,
        "volume": int(meta.get("volume", 1)),
        "arc": int(meta.get("arc", 1)),
        "word_count": int(meta.get("word_count", len(body.split()))),
        "date": meta.get("date", "2026-10-07"),
        "location": meta.get("location", ""),
        "html": html_content
    }

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

  <!-- Border ornament -->
  <rect x="30" y="30" width="1140" height="570" fill="none" stroke="#262a38" stroke-width="2" rx="16"/>
  <rect x="42" y="42" width="1116" height="546" fill="none" stroke="rgba(245,158,11,0.2)" stroke-width="1" rx="12"/>

  <!-- Top Badge -->
  <g transform="translate(600, 110)">
    <rect x="-190" y="-22" width="380" height="44" rx="22" fill="#131722" stroke="#10b981" stroke-width="1.5"/>
    <circle cx="-160" cy="0" r="5" fill="#10b981" filter="url(#glow)"/>
    <text x="0" y="7" fill="#a7f3d0" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle">NOVEL OS • TRƯỜNG THIÊN 3.000 CHƯƠNG</text>
  </g>

  <!-- Main Title -->
  <text x="600" y="270" fill="url(#goldText)" font-family="'Palatino', 'Georgia', serif" font-size="108" font-weight="900" letter-spacing="14" text-anchor="middle" filter="url(#glow)">PHÁ TRỜI</text>
  
  <text x="600" y="330" fill="#94a3b8" font-family="-apple-system, sans-serif" font-size="22" font-weight="500" letter-spacing="8" text-anchor="middle">TIỂU THUYẾT ĐÔ THỊ TU CHÂN • TP. HỒ CHÍ MINH 2026</text>

  <!-- Divider -->
  <line x1="450" y1="365" x2="750" y2="365" stroke="url(#jadeAccent)" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Subtitle / Logline -->
  <text x="600" y="420" fill="#cbd5e1" font-family="'Georgia', serif" font-size="20" font-style="italic" text-anchor="middle">"Lấy nhục thân phàm nhân vượt qua vạn trùng xiềng xích, đúc rèn ý chí kiên định giữa cõi nhân gian."</text>

  <!-- Features Grid Bottom -->
  <g transform="translate(600, 500)">
    <text x="-320" y="0" fill="#f59e0b" font-family="-apple-system, sans-serif" font-size="15" font-weight="600" text-anchor="middle">📖 ĐỌC ONLINE / OFFLINE 24/7</text>
    <text x="0" y="0" fill="#10b981" font-family="-apple-system, sans-serif" font-size="15" font-weight="600" text-anchor="middle">🌙 CHẾ ĐỘ TỐI BÌNH YÊN & SÁNG THANH NHÃ</text>
    <text x="320" y="0" fill="#38bdf8" font-family="-apple-system, sans-serif" font-size="15" font-weight="600" text-anchor="middle">📱 HỖ TRỢ PWA MOBILE TOÀN DIỆN</text>
  </g>
  
  <!-- Author Signature -->
  <text x="600" y="555" fill="#64748b" font-family="-apple-system, sans-serif" font-size="14" letter-spacing="2" text-anchor="middle">TÁC GIẢ: AN BÌNH • BẢO LƯU MỌI QUYỀN (ALL RIGHTS RESERVED)</text>
</svg>"""

def generate_html(chapters_index, total_words):
    return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Phá Trời — Đọc Truyện Trọn Bộ</title>
  
  <!-- SEO & Social Open Graph Metadata -->
  <meta name="title" content="Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026">
  <meta name="description" content="Trường thiên tiểu thuyết đô thị tu chân: Phá Trời. Một người bình thường bước chân vào Thể Đạo từ con số 0 giữa đô thị hiện đại. Đọc trọn bộ online & offline 24/7.">
  <meta name="keywords" content="Phá Trời, Novel OS, tiểu thuyết đô thị, tu chân, thể đạo, Nguyễn Minh An, Lâm Tịch, An Bình">
  <meta name="author" content="An Bình">
  
  <!-- Open Graph / Facebook / Zalo -->
  <meta property="og:type" content="book">
  <meta property="og:url" content="https://bon-231900.github.io/pha-troi/">
  <meta property="og:title" content="Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026">
  <meta property="og:description" content="Một người bình thường bước chân vào Thể Đạo từ con số 0 giữa đô thị hiện đại. Đọc trọn bộ online & offline 24/7.">
  <meta property="og:image" content="https://bon-231900.github.io/pha-troi/cover.svg">
  <meta property="og:image:type" content="image/svg+xml">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Phá Trời — Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026">
  <meta name="twitter:description" content="Một người bình thường bước chân vào Thể Đạo từ con số 0 giữa đô thị hiện đại. Đọc trọn bộ online & offline 24/7.">
  <meta name="twitter:image" content="https://bon-231900.github.io/pha-troi/cover.svg">

  <link rel="manifest" href="./manifest.json">
  <link rel="icon" href="./icon.svg" type="image/svg+xml">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Phá Trời">
  <meta name="theme-color" content="#08090d">

  <!-- Google Fonts for Vietnamese Typography (Be Vietnam Pro & Lora) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <style>
    /* ==========================================================================
       1. GLOBAL TYPOGRAPHY & LAYOUT VARIABLES
       ========================================================================== */
    :root {
      --font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --font-size: 19px;
      --line-height: 1.85;
      --max-width: 760px;
    }

    /* ==========================================================================
       2. COLOR THEMES
       ========================================================================== */
    :root, html.theme-peaceful-dark, body.theme-peaceful-dark {
      /* Theme 1: Peaceful Dark (Mặc định - Tối Bình Yên) */
      --bg-color: #08090d;
      --bg-gradient: radial-gradient(circle at 50% 15%, #121522 0%, #08090d 75%);
      --text-color: #d6dce7;
      --text-muted: #8b95a5;
      --header-bg: rgba(8, 9, 13, 0.88);
      --card-bg: #11131c;
      --card-bg-hover: #181b28;
      --border-color: rgba(255, 255, 255, 0.08);
      --accent-primary: #10b981; /* Thanh Liên Ngọc */
      --accent-glow: rgba(16, 185, 129, 0.35);
      --gold-primary: #f59e0b; /* Hoàng Kim Chu Sa */
      --gold-glow: rgba(245, 158, 11, 0.35);
    }

    /* Theme 2: Gentle Light (Sáng Nhẹ Nhàng / Bạch Trà Thanh Nhã) */
    html.theme-gentle-light, body.theme-gentle-light {
      --bg-color: #f7f5f0;
      --bg-gradient: radial-gradient(circle at 50% 10%, #ffffff 0%, #f7f5f0 85%);
      --text-color: #24221f;
      --text-muted: #6b665f;
      --header-bg: rgba(247, 245, 240, 0.92);
      --card-bg: #ede9df;
      --card-bg-hover: #e5e0d4;
      --border-color: rgba(0, 0, 0, 0.08);
      --accent-primary: #b91c1c; /* Chu Sa Trầm */
      --accent-glow: rgba(185, 28, 28, 0.2);
      --gold-primary: #92400e; /* Đồng Thau Cổ */
      --gold-glow: rgba(146, 64, 14, 0.2);
    }

    /* Theme 3: OLED Pure Black */
    html.theme-oled, body.theme-oled {
      --bg-color: #000000;
      --bg-gradient: none;
      --text-color: #cbd5e1;
      --text-muted: #64748b;
      --header-bg: rgba(0, 0, 0, 0.95);
      --card-bg: #090a0d;
      --card-bg-hover: #12141a;
      --border-color: rgba(255, 255, 255, 0.09);
      --accent-primary: #34d399;
      --accent-glow: rgba(52, 211, 153, 0.3);
      --gold-primary: #fbbf24;
      --gold-glow: rgba(251, 191, 36, 0.3);
    }

    /* Theme 4: Sepia Cổ Điển */
    html.theme-sepia, body.theme-sepia {
      --bg-color: #f4edd8;
      --bg-gradient: radial-gradient(circle at 50% 10%, #fbf4e2 0%, #f4edd8 85%);
      --text-color: #3b2d1d;
      --text-muted: #78654c;
      --header-bg: rgba(244, 237, 216, 0.94);
      --card-bg: #e8dcc3;
      --card-bg-hover: #decfae;
      --border-color: rgba(60, 40, 20, 0.1);
      --accent-primary: #8b0000;
      --accent-glow: rgba(139, 0, 0, 0.2);
      --gold-primary: #854d0e;
      --gold-glow: rgba(133, 77, 14, 0.2);
    }

    /* ==========================================================================
       2. RESET & GLOBAL STYLES
       ========================================================================== */
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    html, body {
      margin: 0; padding: 0;
      background: var(--bg-color);
      background-image: var(--bg-gradient);
      background-attachment: fixed;
      color: var(--text-color);
      font-family: var(--font-family);
      font-size: var(--font-size);
      line-height: var(--line-height);
      min-height: 100vh;
      transition: background-color 0.28s cubic-bezier(0.4, 0, 0.2, 1), color 0.28s ease;
      overflow-x: hidden;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }

    /* ==========================================================================
       3. TOP PROGRESS BAR (LUMINOUS AURA)
       ========================================================================== */
    #progressBarContainer {
      position: fixed; top: 0; left: 0; right: 0; height: 3px;
      background: transparent; z-index: 1001; pointer-events: none;
    }
    #progressBar {
      height: 100%; width: 0%;
      background: linear-gradient(90deg, var(--accent-primary), var(--gold-primary));
      box-shadow: 0 0 10px var(--accent-glow);
      transition: width 0.12s ease-out;
    }

    /* ==========================================================================
       4. HEADER NAVIGATION
       ========================================================================== */
    header {
      position: fixed; top: 0; left: 0; right: 0; height: 56px;
      background: var(--header-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 16px; z-index: 900;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    header.hidden { transform: translateY(-100%); }

    .header-left, .header-right {
      display: flex; align-items: center; gap: 6px;
    }

    .btn-icon {
      background: none; border: none; color: var(--text-color);
      width: 40px; height: 40px; cursor: pointer;
      display: inline-flex; align-items: center; justify-content: center;
      border-radius: 10px; transition: all 0.2s ease;
      position: relative;
    }
    .btn-icon:hover {
      background: var(--card-bg);
      color: var(--gold-primary);
    }
    .btn-icon:active { transform: scale(0.94); }

    .header-center {
      flex: 1; min-width: 0; text-align: center; padding: 0 10px;
    }
    .header-title {
      font-size: 15px; font-weight: 700; color: var(--gold-primary);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      margin: 0; letter-spacing: 0.3px;
    }
    .header-sub {
      font-size: 11px; color: var(--text-muted);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      margin: 0; opacity: 0.85;
    }

    .badge-live {
      display: inline-flex; align-items: center; gap: 5px;
      padding: 3px 8px; border-radius: 20px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.25);
      font-size: 11px; font-weight: 600; color: #10b981;
    }
    .dot-live {
      width: 6px; height: 6px; border-radius: 50%; background: #10b981;
      box-shadow: 0 0 6px #10b981;
      animation: pulseDot 2s infinite ease-in-out;
    }
    @keyframes pulseDot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* ==========================================================================
       5. MAIN CONTAINER & READING LAYOUT
       ========================================================================== */
    .app-layout {
      display: flex; justify-content: center; min-height: 100vh;
      padding-top: 68px; padding-bottom: 84px;
    }

    .main-reader {
      width: 100%; max-width: var(--max-width);
      padding: 24px 20px 60px 20px;
      margin: 0 auto;
    }

    /* Desktop Sidebar (Persistent TOC on large screens) */
    .desktop-toc-sidebar {
      display: none;
      width: 290px; height: calc(100vh - 68px);
      position: sticky; top: 68px;
      overflow-y: auto; padding: 16px;
      border-right: 1px solid var(--border-color);
      scrollbar-width: thin;
    }
    @media (min-width: 1200px) {
      .app-layout.has-sidebar .desktop-toc-sidebar { display: block; }
      .app-layout.has-sidebar .main-reader { margin-left: 30px; }
    }

    /* Chapter Header in Reader */
    .chapter-hero {
      text-align: center; margin-bottom: 36px; padding-bottom: 24px;
      border-bottom: 1px dashed var(--border-color);
    }
    .chapter-vol-arc {
      display: inline-block; font-size: 12px; font-weight: 700;
      letter-spacing: 2px; text-transform: uppercase;
      color: var(--accent-primary); margin-bottom: 10px;
      padding: 4px 12px; border-radius: 6px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid var(--border-color);
    }
    .chapter-main-title {
      font-size: 27px; font-weight: 800; line-height: 1.35;
      margin: 12px 0 14px 0; color: var(--gold-primary);
      letter-spacing: 0.5px;
    }
    .chapter-meta-line {
      display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 14px;
      font-size: 13px; color: var(--text-muted);
    }

    /* Novel Content Body */
    .novel-body p {
      margin: 0 0 1.35em 0;
      text-align: justify;
      hyphens: auto;
    }
    .novel-body hr {
      border: none;
      text-align: center;
      margin: 2.2em 0;
    }
    .novel-body hr::after {
      content: "✦  ✦  ✦";
      color: var(--gold-primary);
      opacity: 0.6;
      letter-spacing: 12px;
      font-size: 14px;
    }
    .novel-body em {
      font-style: italic;
      color: var(--text-color);
      opacity: 0.95;
    }
    .novel-body strong {
      color: var(--gold-primary);
      font-weight: 700;
    }

    /* Chapter Foot Navigation */
    .chapter-footer-nav {
      margin-top: 50px; padding-top: 24px;
      border-top: 1px solid var(--border-color);
      display: flex; justify-content: space-between; align-items: center; gap: 12px;
    }
    .btn-nav-chapter {
      flex: 1; padding: 13px 16px; border-radius: 12px;
      background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); font-size: 15px; font-weight: 600;
      cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
      transition: all 0.2s ease;
    }
    .btn-nav-chapter:hover:not(:disabled) {
      background: var(--card-bg-hover);
      border-color: var(--gold-primary);
      color: var(--gold-primary);
      transform: translateY(-1px);
    }
    .btn-nav-chapter:disabled {
      opacity: 0.35; cursor: not-allowed;
    }

    /* ==========================================================================
       6. MOBILE BOTTOM BAR
       ========================================================================== */
    .bottom-bar {
      position: fixed; bottom: 0; left: 0; right: 0; height: 58px;
      background: var(--header-bg);
      backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      border-top: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-around;
      padding: 0 10px; z-index: 900;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bottom-bar.hidden { transform: translateY(100%); }

    .btn-bottom-item {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      background: none; border: none; color: var(--text-muted);
      font-size: 11px; font-weight: 500; cursor: pointer; padding: 4px 10px;
      border-radius: 8px; transition: color 0.2s;
    }
    .btn-bottom-item svg { width: 22px; height: 22px; margin-bottom: 2px; }
    .btn-bottom-item.active, .btn-bottom-item:hover {
      color: var(--gold-primary);
    }

    /* ==========================================================================
       7. DRAWERS & MODALS (TOC, CODEX, SETTINGS)
       ========================================================================== */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
      z-index: 999; opacity: 0; pointer-events: none;
      transition: opacity 0.25s ease;
    }
    .modal-overlay.open { opacity: 1; pointer-events: auto; }

    /* Drawer Common (TOC, Codex) */
    .drawer {
      position: fixed; top: 0; bottom: 0; width: 88%; max-width: 420px;
      background: var(--card-bg); z-index: 1000;
      box-shadow: 0 0 35px rgba(0, 0, 0, 0.6);
      display: flex; flex-direction: column;
      transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .drawer-left { left: 0; transform: translateX(-100%); border-right: 1px solid var(--border-color); }
    .drawer-left.open { transform: translateX(0); }

    .drawer-right { right: 0; transform: translateX(100%); border-left: 1px solid var(--border-color); }
    .drawer-right.open { transform: translateX(0); }

    .drawer-header {
      padding: 16px 20px; border-bottom: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-between;
      background: rgba(0,0,0,0.15);
    }
    .drawer-title { font-size: 17px; font-weight: 700; color: var(--gold-primary); margin: 0; }
    
    .drawer-tabs {
      display: flex; border-bottom: 1px solid var(--border-color);
      background: rgba(0,0,0,0.1);
    }
    .drawer-tab-btn {
      flex: 1; padding: 12px 6px; background: none; border: none;
      color: var(--text-muted); font-size: 13px; font-weight: 600;
      cursor: pointer; text-align: center; border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .drawer-tab-btn.active {
      color: var(--accent-primary);
      border-bottom-color: var(--accent-primary);
      background: rgba(16, 185, 129, 0.05);
    }

    .drawer-search {
      padding: 10px 16px; border-bottom: 1px solid var(--border-color);
    }
    .search-input {
      width: 100%; padding: 9px 12px; border-radius: 8px;
      background: rgba(0, 0, 0, 0.2); border: 1px solid var(--border-color);
      color: var(--text-color); font-size: 14px; outline: none;
    }
    .search-input:focus { border-color: var(--accent-primary); }

    .drawer-body {
      flex: 1; overflow-y: auto; padding: 10px 16px;
      scrollbar-width: thin;
    }

    /* Chapter item in TOC */
    .toc-item {
      padding: 12px 14px; border-radius: 10px; margin-bottom: 6px;
      cursor: pointer; display: flex; align-items: center; justify-content: space-between;
      border: 1px solid transparent; transition: all 0.18s ease;
    }
    .toc-item:hover {
      background: var(--card-bg-hover);
      border-color: var(--border-color);
    }
    .toc-item.active {
      background: rgba(16, 185, 129, 0.12);
      border-color: var(--accent-primary);
    }
    .toc-item.active .toc-name {
      color: var(--accent-primary); font-weight: 700;
    }
    .toc-info { min-width: 0; flex: 1; margin-right: 10px; }
    .toc-num { font-size: 11px; color: var(--gold-primary); font-weight: 700; text-transform: uppercase; margin-bottom: 2px; }
    .toc-name { font-size: 14px; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .toc-meta { font-size: 11px; color: var(--text-muted); }

    /* Codex Card Styles */
    .codex-card {
      background: rgba(0,0,0,0.2); border: 1px solid var(--border-color);
      border-radius: 12px; padding: 14px; margin-bottom: 14px;
    }
    .codex-badge {
      display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px;
      border-radius: 4px; background: rgba(245, 158, 11, 0.15); color: var(--gold-primary);
      margin-bottom: 6px;
    }
    .codex-title { font-size: 15px; font-weight: 700; color: var(--gold-primary); margin: 0 0 6px 0; }
    .codex-desc { font-size: 13px; color: var(--text-color); opacity: 0.9; line-height: 1.6; margin: 0; }
    .codex-stat {
      display: flex; justify-content: space-between; font-size: 12px;
      padding: 6px 0; border-top: 1px dashed var(--border-color); margin-top: 8px;
      color: var(--text-muted);
    }
    .codex-stat-val { color: var(--accent-primary); font-weight: 600; }

    /* Settings Bottom Sheet */
    .sheet-bottom {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: var(--card-bg); z-index: 1000;
      border-top: 1px solid var(--border-color);
      border-radius: 20px 20px 0 0;
      max-width: 580px; margin: 0 auto;
      padding: 20px 24px 36px 24px;
      transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .sheet-bottom.open { transform: translateY(0); }
    .sheet-handle {
      width: 36px; height: 4px; border-radius: 2px;
      background: var(--border-color); margin: 0 auto 16px auto;
    }

    .setting-group { margin-bottom: 18px; }
    .setting-label {
      font-size: 12px; font-weight: 700; color: var(--text-muted);
      text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
    }
    .theme-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .theme-opt {
      padding: 10px 6px; border-radius: 10px; border: 2px solid var(--border-color);
      background: rgba(0,0,0,0.1); cursor: pointer; text-align: center;
      font-size: 12px; font-weight: 600; color: var(--text-color);
      transition: all 0.2s;
    }
    .theme-opt.active {
      border-color: var(--accent-primary);
      box-shadow: 0 0 10px var(--accent-glow);
    }

    .stepper-ctrl {
      display: flex; align-items: center; justify-content: space-between;
      background: rgba(0,0,0,0.15); border-radius: 10px; padding: 4px;
      border: 1px solid var(--border-color);
    }
    .btn-step {
      width: 44px; height: 38px; background: var(--card-bg);
      border: 1px solid var(--border-color); color: var(--text-color);
      border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;
    }
    .stepper-val { font-size: 15px; font-weight: 700; color: var(--gold-primary); }

    /* Floating Side Desktop Navigation */
    .desktop-nav-float {
      display: none; position: fixed; top: 50%; transform: translateY(-50%);
      z-index: 800;
    }
    .desktop-nav-left { left: 24px; }
    .desktop-nav-right { right: 24px; }
    @media (min-width: 1024px) {
      .desktop-nav-float { display: flex; flex-direction: column; align-items: center; }
    }
    .btn-float-nav {
      width: 48px; height: 48px; border-radius: 50%;
      background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 6px 18px rgba(0,0,0,0.25);
      transition: all 0.2s;
    }
    .btn-float-nav:hover:not(:disabled) {
      border-color: var(--gold-primary);
      color: var(--gold-primary);
      transform: scale(1.1);
    }
    .btn-float-nav:disabled { opacity: 0.3; cursor: not-allowed; }

    /* Toast Notification */
    #liveToast {
      position: fixed; bottom: 74px; left: 50%; transform: translateX(-50%) translateY(30px);
      background: var(--card-bg); border: 1px solid var(--accent-primary);
      color: var(--text-color); font-size: 13px; font-weight: 600;
      padding: 10px 18px; border-radius: 30px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      opacity: 0; pointer-events: none; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 2000; white-space: nowrap; display: flex; align-items: center; gap: 8px;
    }
    #liveToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }

    /* Audio Ambient Widget */
    .ambient-widget {
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 14px; border-radius: 10px; background: rgba(0,0,0,0.15);
      border: 1px solid var(--border-color); margin-top: 10px;
    }
  </style>
</head>
<body class="theme-peaceful-dark">

  <!-- Progress Bar Top -->
  <div id="progressBarContainer">
    <div id="progressBar"></div>
  </div>

  <!-- HEADER -->
  <header id="topHeader">
    <div class="header-left">
      <button class="btn-icon" id="btnMenu" title="Mục Lục Chương (M)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      <button class="btn-icon" id="btnCodex" title="Bách Khoa Cổ Vật & Hồ Sơ (C)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
      </button>
    </div>

    <div class="header-center">
      <h1 class="header-title" id="headerTitle">Phá Trời (Phá Toái Thần Hoang)</h1>
      <p class="header-sub" id="headerSub">Đang tải...</p>
    </div>

    <div class="header-right">
      <!-- Ambient Rain Toggle -->
      <button class="btn-icon" id="btnAmbient" title="Âm thanh Mưa Đêm Sài Gòn (Thư giãn)">
        <svg id="iconAudioOff" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>
        <svg id="iconAudioOn" style="display:none; color:var(--accent-primary);" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
      </button>

      <!-- Quick Theme Switcher (Mặt trăng / Mặt trời) -->
      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Nhanh Sáng / Tối (T)">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg id="iconSun" style="display:none;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button class="btn-icon" id="btnSettings" title="Cài Đặt Đọc Truyện">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
      </button>
    </div>
  </header>

  <!-- APP LAYOUT -->
  <div class="app-layout" id="appLayout">

    <!-- DESKTOP PERSISTENT TOC SIDEBAR -->
    <aside class="desktop-toc-sidebar" id="desktopTocSidebar">
      <div style="font-size:13px; font-weight:700; color:var(--gold-primary); margin-bottom:12px; display:flex; justify-content:space-between;">
        <span>DANH MỤC CHƯƠNG</span>
        <span id="dtTocCount">57 chương</span>
      </div>
      <div id="desktopTocList"></div>
    </aside>

    <!-- FLOATING DESKTOP ARROWS -->
    <div class="desktop-nav-float desktop-nav-left">
      <button class="btn-float-nav" id="btnFloatPrev" title="Chương trước (Phím ←)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
      </button>
    </div>
    <div class="desktop-nav-float desktop-nav-right">
      <button class="btn-float-nav" id="btnFloatNext" title="Chương sau (Phím →)">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </button>
    </div>

    <!-- MAIN READER AREA -->
    <main class="main-reader" id="mainReader">
      <!-- Chapter Hero Header -->
      <section class="chapter-hero">
        <div class="chapter-vol-arc" id="heroVolArc">QUYỂN 1 • HỒI 1</div>
        <h1 class="chapter-main-title" id="heroTitle">Đang nạp bản thảo...</h1>
        <div class="chapter-meta-line">
          <span id="heroWordCount">0 từ</span>
          <span>•</span>
          <span id="heroDate">2026-10-07</span>
          <span>•</span>
          <span class="badge-live"><span class="dot-live"></span> PWA 24/7</span>
        </div>
      </section>

      <!-- Novel Content -->
      <article class="novel-body" id="novelContent">
        <p style="text-align:center; color:var(--text-muted); padding: 40px 0;">Đang kết nối kho bản thảo Novel OS...</p>
      </article>

      <!-- Bottom Nav Inside Content -->
      <div class="chapter-footer-nav">
        <button class="btn-nav-chapter" id="btnFooterPrev">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
          Chương Trước
        </button>
        <button class="btn-nav-chapter" id="btnFooterNext">
          Chương Sau
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>
      </div>
    </main>
  </div>

  <!-- MOBILE BOTTOM NAVIGATION -->
  <nav class="bottom-bar" id="bottomBar">
    <button class="btn-bottom-item" id="btnMobilePrev">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
      <span>Trước</span>
    </button>
    <button class="btn-bottom-item" id="btnMobileToc">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      <span>Mục Lục</span>
    </button>
    <button class="btn-bottom-item" id="btnMobileCodex">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
      <span>Bảo Vật</span>
    </button>
    <button class="btn-bottom-item" id="btnMobileNext">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
      <span>Sau</span>
    </button>
  </nav>

  <!-- MODAL OVERLAY -->
  <div class="modal-overlay" id="modalOverlay"></div>

  <!-- TOC DRAWER (MỤC LỤC BẢN THẢO) -->
  <aside class="drawer drawer-left" id="drawerToc">
    <div class="drawer-header">
      <h2 class="drawer-title">MỤC LỤC TIỂU THUYẾT</h2>
      <button class="btn-icon" id="btnCloseToc">✕</button>
    </div>
    
    <!-- Filter Tabs (Hồi 1, Hồi 2, Tất Cả) -->
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" data-filter="all">Tất Cả (<span id="tocTotalCount">57</span>)</button>
      <button class="drawer-tab-btn" data-filter="arc1">Hồi 1 (1–46)</button>
      <button class="drawer-tab-btn" data-filter="arc2">Hồi 2 (47–57+)</button>
    </div>

    <div class="drawer-search">
      <input type="text" id="inputTocSearch" class="search-input" placeholder="Tìm chương hoặc từ khóa...">
    </div>

    <div class="drawer-body" id="tocDrawerList">
      <!-- Generated via JS -->
    </div>
  </aside>

  <!-- CODEX DRAWER (BÁCH KHOA TOÀN THƯ PHÁ TRỜI) -->
  <aside class="drawer drawer-right" id="drawerCodex">
    <div class="drawer-header">
      <h2 class="drawer-title">BÁCH KHOA TOÀN THƯ</h2>
      <button class="btn-icon" id="btnCloseCodex">✕</button>
    </div>

    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" id="tabCodexChar" data-codex="char">Nhân Vật</button>
      <button class="drawer-tab-btn" id="tabCodexItem" data-codex="item">Kho Bảo Vật</button>
      <button class="drawer-tab-btn" id="tabCodexLotus" data-codex="lotus">Thức Hải</button>
    </div>

    <div class="drawer-body" id="codexBody">
      <!-- Tab 1: Nguyễn Minh An -->
      <div id="codexPaneChar">
        <div class="codex-card">
          <span class="codex-badge">NAM CHÍNH • THỂ ĐẠO</span>
          <h3 class="codex-title">Nguyễn Minh An (25 tuổi)</h3>
          <p class="codex-desc">Người bình thường 100% tại TP.HCM năm 2026. Tự lực tôi luyện ý chí và nhục thân, dùng đôi bàn tay trần gánh vác trách nhiệm bảo vệ cõi phàm trần.</p>
          <div class="codex-stat"><span>Chức Vụ</span><span class="codex-stat-val">Giám Đốc Kỹ Thuật Dữ Liệu</span></div>
          <div class="codex-stat"><span>Cơ Quan</span><span class="codex-stat-val">Viện Nghiên Cứu Địa Tầng Đô Thị</span></div>
          <div class="codex-stat"><span>Cảnh Giới</span><span class="codex-stat-val">Luyện Cốt Trung Kỳ (Cốt Nhược Kim Thạch)</span></div>
          <div class="codex-stat"><span>Thương Tật</span><span class="codex-stat-val">4 Vết Sẹo Đạn Chì (Đã Lành Da)</span></div>
          <div class="codex-stat"><span>Công Pháp</span><span class="codex-stat-val">Đoán Cốt Thập Nhị Thức (Thức 5)</span></div>
          <div class="codex-stat"><span>Thể Thuật</span><span class="codex-stat-val">Kính Kình Phản Chấn Thuật</span></div>
        </div>
      </div>

      <!-- Tab 2: Kho Bảo Vật -->
      <div id="codexPaneItem" style="display:none;">
        <div class="codex-card">
          <span class="codex-badge">VŨ KHÍ CHÍNH HOÀN THIỆN</span>
          <h3 class="codex-title">Hắc Thiết Đoản Côn</h3>
          <p class="codex-desc">Thép nhíp Zil tôi dầu cám chu sa thạch anh do bác Sáu Kiên và Minh An rèn. Chịu lực đè nửa tấn, miễn nhiễm âm sát, dẫn truyền hoàn hảo Kính Kình.</p>
          <div class="codex-stat"><span>Kích Thước</span><span class="codex-stat-val">Dài 52cm • Nặng 3.2kg</span></div>
          <div class="codex-stat"><span>Độ Bền</span><span class="codex-stat-val">100 / 100 (Hoàn Hảo)</span></div>
        </div>

        <div class="codex-card">
          <span class="codex-badge">CỔ KHÍ TRẤN THỦY</span>
          <h3 class="codex-title">Trấn Thủy Đoản Đao</h3>
          <p class="codex-desc">Một trong 'Thủy Môn Thập Nhị Tiêu' bảo vệ lưu vực sông ngòi Sài Gòn. Đúc từ hợp kim tiền sử (>2.5 triệu năm), đã được Minh An thuần hóa bằng Luyện Cốt kình lực.</p>
          <div class="codex-stat"><span>Đặc Điểm</span><span class="codex-stat-val">Hoàng Đồng Ánh Kim (33cm)</span></div>
          <div class="codex-stat"><span>Tần Số</span><span class="codex-stat-val">7.83 Hz (Schumann)</span></div>
        </div>

        <div class="codex-card">
          <span class="codex-badge">DI VẬT BẢN MỆNH</span>
          <h3 class="codex-title">Trâm Ngọc Cổ (Cố Hồn Trâm)</h3>
          <p class="codex-desc">Di vật của Lâm Tịch neo đậu trong túi ngực trái Minh An. Cầu nối duy nhất giữa thế giới thực và Thanh Liên Đài nơi thức hải.</p>
          <div class="codex-stat"><span>Tình Trạng</span><span class="codex-stat-val">3 Vết Rạn Tơ • Thu Liễm Quang Hoa</span></div>
        </div>

        <div class="codex-card">
          <span class="codex-badge">VẬT PHẨM TIÊU HAO</span>
          <h3 class="codex-title">Khí Huyết Thông Cốt Tửu</h3>
          <p class="codex-desc">Rượu thuốc bồi bổ tủy xương cổ phương ngâm thảo dược Bát Tràng. Đã dùng khử độc chì sau trận Ba Láng.</p>
          <div class="codex-stat"><span>Mức Còn Lại</span><span class="codex-stat-val">~20% Bình (0.65 Lít)</span></div>
        </div>
      </div>

      <!-- Tab 3: Thức Hải Lâm Tịch -->
      <div id="codexPaneLotus" style="display:none;">
        <div class="codex-card" style="border-color:rgba(16,185,129,0.3); background:rgba(16,185,129,0.04);">
          <span class="codex-badge" style="background:rgba(16,185,129,0.2); color:#10b981;">NGUYÊN THẦN TỔN HẠI</span>
          <h3 class="codex-title" style="color:#10b981;">Lâm Tịch (Bạch Y Kiếm Tu)</h3>
          <p class="codex-desc">Tồn tại viễn cổ đứng trên đỉnh cao chư thiên vị diện. Đạo cơ tan vỡ trong đại chiến diệt thế, nguyên thần cốt lõi neo đậu vào ý thức Minh An.</p>
          <div class="codex-stat"><span>Nơi Trú Ngụ</span><span class="codex-stat-val">Thanh Liên Đài (Thức Hải)</span></div>
          <div class="codex-stat"><span>Trạng Thái</span><span class="codex-stat-val">Trầm Miên Sâu Dài Hạn</span></div>
          <div class="codex-stat"><span>Tiến Độ Hồi Phục</span><span class="codex-stat-val">~1.5%</span></div>
          <div class="codex-stat"><span>Khẩu Quyết Mới</span><span class="codex-stat-val">"Dĩ cốt định huyết, vạn kiếp bất di"</span></div>
        </div>
      </div>
    </div>
  </aside>

  <!-- SETTINGS BOTTOM SHEET -->
  <aside class="sheet-bottom" id="settingsSheet">
    <div class="sheet-handle"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
      <h3 style="font-size:16px; font-weight:700; margin:0; color:var(--gold-primary);">CÀI ĐẶT GIAO DIỆN ĐỌC</h3>
      <button class="btn-icon" id="btnCloseSettings">✕</button>
    </div>

    <!-- Theme Selection (4 Themes) -->
    <div class="setting-group">
      <div class="setting-label">Chế Độ Hiển Thị</div>
      <div class="theme-grid">
        <div class="theme-opt active" data-theme="theme-peaceful-dark" style="background:#08090d; color:#d6dce7;">
          Tối Bình Yên
        </div>
        <div class="theme-opt" data-theme="theme-gentle-light" style="background:#f7f5f0; color:#24221f;">
          Sáng Thanh Nhã
        </div>
        <div class="theme-opt" data-theme="theme-oled" style="background:#000000; color:#cbd5e1;">
          OLED Đen
        </div>
        <div class="theme-opt" data-theme="theme-sepia" style="background:#f4edd8; color:#3b2d1d;">
          Sepia Cổ Điển
        </div>
      </div>
    </div>

    <!-- Font Size Stepper -->
    <div class="setting-group">
      <div class="setting-label">Cỡ Chữ Đọc</div>
      <div class="stepper-ctrl">
        <button class="btn-step" id="btnFontDec">A-</button>
        <span class="stepper-val" id="fontSizeVal">19</span>
        <button class="btn-step" id="btnFontInc">A+</button>
      </div>
    </div>

    <!-- Font Family -->
    <div class="setting-group">
      <div class="setting-label">Phông Chữ</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
        <button class="btn-step" id="btnFontSerif" style="width:100%; font-family:serif;">Có Chân (Bookerly)</button>
        <button class="btn-step" id="btnFontSans" style="width:100%; font-family:sans-serif;">Không Chân (Inter)</button>
      </div>
    </div>

    <!-- Ambient Audio Volume -->
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

    <!-- Cache Offline Button -->
    <div style="margin-top:16px;">
      <button id="btnCacheAll" style="width:100%; padding:13px; border-radius:12px; background:var(--accent-primary); color:#ffffff; font-weight:700; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        <span id="cacheAllText">Tải Toàn Bộ 57 Chương Để Đọc Offline</span>
      </button>
    </div>
  </aside>

  <!-- LIVE TOAST -->
  <div id="liveToast">
    <span class="dot-live"></span>
    <span id="toastMsg">Thông báo</span>
  </div>

  <!-- SCRIPT LOGIC -->
  <script>
    // State Variables
    let chaptersData = [];
    let currentChapter = parseInt(localStorage.getItem('pha_troi_cur_ch') || '1');
    let totalChapters = 57;
    let uiVisible = true;
    let activeArcFilter = 'all';

    // DOM Elements
    const topHeader = document.getElementById('topHeader');
    const bottomBar = document.getElementById('bottomBar');
    const progressBar = document.getElementById('progressBar');
    const mainReader = document.getElementById('mainReader');
    const heroTitle = document.getElementById('heroTitle');
    const heroVolArc = document.getElementById('heroVolArc');
    const heroWordCount = document.getElementById('heroWordCount');
    const heroDate = document.getElementById('heroDate');
    const novelContent = document.getElementById('novelContent');
    const headerTitle = document.getElementById('headerTitle');
    const headerSub = document.getElementById('headerSub');

    // Drawers
    const modalOverlay = document.getElementById('modalOverlay');
    const drawerToc = document.getElementById('drawerToc');
    const drawerCodex = document.getElementById('drawerCodex');
    const settingsSheet = document.getElementById('settingsSheet');
    const tocDrawerList = document.getElementById('tocDrawerList');
    const desktopTocList = document.getElementById('desktopTocList');
    const liveToast = document.getElementById('liveToast');
    const toastMsg = document.getElementById('toastMsg');

    // 1. Web Audio Synthesizer (Pink Noise + Low-Pass Soft Rain)
    let audioCtx = null;
    let noiseNode = null;
    let gainNode = null;
    let filterNode = null;
    let isRainPlaying = false;
    let rainVolume = 0.25;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function toggleRainSound() {
      if (isRainPlaying) {
        stopRainSound();
        showToast('🌧️ Đã tắt âm thanh mưa');
      } else {
        startRainSound();
        showToast('🌧️ Bật âm thanh mưa đêm Sài Gòn (Thư giãn)');
      }
      updateAudioIcons();
    }

    function startRainSound() {
      initAudio();
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      if (noiseNode) return;

      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.045;
        b6 = white * 0.115926;
      }

      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = noiseBuffer;
      noiseNode.loop = true;

      filterNode = audioCtx.createBiquadFilter();
      filterNode.type = 'lowpass';
      filterNode.frequency.value = 750; // Soft rain sound

      gainNode = audioCtx.createGain();
      gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);

      noiseNode.connect(filterNode);
      filterNode.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      noiseNode.start();
      isRainPlaying = true;
    }

    function stopRainSound() {
      if (noiseNode) {
        try { noiseNode.stop(); noiseNode.disconnect(); } catch (e) {}
        noiseNode = null;
      }
      isRainPlaying = false;
    }

    function updateAudioIcons() {
      const offIcon = document.getElementById('iconAudioOff');
      const onIcon = document.getElementById('iconAudioOn');
      if (isRainPlaying) {
        offIcon.style.display = 'none';
        onIcon.style.display = 'inline-block';
      } else {
        offIcon.style.display = 'inline-block';
        onIcon.style.display = 'none';
      }
    }

    document.getElementById('btnAmbient').onclick = toggleRainSound;
    document.getElementById('btnSheetAudioToggle').onclick = toggleRainSound;
    document.getElementById('audioVolume').oninput = (e) => {
      rainVolume = parseFloat(e.target.value);
      document.getElementById('audioVolVal').innerText = Math.round(rainVolume * 100) + '%';
      if (gainNode) {
        gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
      }
    };

    // 2. Load Chapters Index
    async function loadChaptersIndex(isInitial = false) {
      try {
        const res = await fetch('./data/chapters.json?v=' + Date.now());
        const data = await res.json();
        chaptersData = data.chapters || [];
        totalChapters = chaptersData.length;
        document.getElementById('tocTotalCount').innerText = totalChapters;
        document.getElementById('dtTocCount').innerText = `${totalChapters} chương`;

        renderTOC();

        if (isInitial) {
          if (currentChapter > totalChapters) currentChapter = 1;
          loadChapter(currentChapter);
        }
      } catch (err) {
        console.warn('Đang đọc ở chế độ Offline:', err);
        if (isInitial) loadChapter(currentChapter);
      }
    }

    function renderTOC() {
      const searchVal = document.getElementById('inputTocSearch').value.toLowerCase().trim();
      const filtered = chaptersData.filter(ch => {
        const matchSearch = !searchVal || ch.title.toLowerCase().includes(searchVal) || String(ch.chapter).includes(searchVal);
        const matchArc = (activeArcFilter === 'all') ||
                         (activeArcFilter === 'arc1' && ch.arc === 1) ||
                         (activeArcFilter === 'arc2' && ch.arc === 2);
        return matchSearch && matchArc;
      });

      const renderHtml = filtered.map(ch => `
        <div class="toc-item ${ch.chapter === currentChapter ? 'active' : ''}" onclick="selectChapter(${ch.chapter})">
          <div class="toc-info">
            <div class="toc-num">Hồi ${ch.arc || 1} • Chương ${ch.chapter}</div>
            <div class="toc-name">${ch.title.replace(/^Chương \\d+:\\s*/i, '')}</div>
          </div>
          <span class="toc-meta">${ch.word_count ? ch.word_count.toLocaleString() + ' từ' : ''}</span>
        </div>
      `).join('');

      tocDrawerList.innerHTML = renderHtml || '<p style="text-align:center; color:var(--text-muted); padding:20px;">Không tìm thấy chương nào.</p>';
      if (desktopTocList) desktopTocList.innerHTML = renderHtml;
    }

    document.getElementById('inputTocSearch').oninput = renderTOC;

    // Filter Buttons in TOC
    document.querySelectorAll('.drawer-tab-btn[data-filter]').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.drawer-tab-btn[data-filter]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeArcFilter = btn.dataset.filter;
        renderTOC();
      };
    });

    // 3. Load Chapter Content
    async function loadChapter(num) {
      currentChapter = num;
      localStorage.setItem('pha_troi_cur_ch', num);
      window.scrollTo(0, 0);

      // Update Nav buttons
      const isFirst = (currentChapter <= 1);
      const isLast = (currentChapter >= totalChapters);
      ['btnFloatPrev', 'btnFooterPrev', 'btnMobilePrev'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.disabled = isFirst;
      });
      ['btnFloatNext', 'btnFooterNext', 'btnMobileNext'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.disabled = isLast;
      });

      heroTitle.innerText = 'Đang tải bản thảo...';
      
      try {
        const res = await fetch(`./data/chapter_${num}.json`);
        const data = await res.json();

        headerTitle.innerText = `Chương ${data.chapter}: ${data.title.replace(/^Chương \\d+:\\s*/i, '')}`;
        headerSub.innerText = `Quyển ${data.volume || 1} • Hồi ${data.arc || 1} • ${data.word_count ? data.word_count.toLocaleString() + ' từ' : ''}`;
        
        heroVolArc.innerText = `QUYỂN ${data.volume || 1} • HỒI ${data.arc || 1}`;
        heroTitle.innerText = data.title;
        heroWordCount.innerText = `${data.word_count ? data.word_count.toLocaleString() : '0'} từ`;
        heroDate.innerText = data.date || '2026-10-07';

        novelContent.innerHTML = data.html;

        // Re-render TOC active items
        renderTOC();
      } catch (err) {
        novelContent.innerHTML = `<p style="color:#ef4444; text-align:center; padding:40px 0;">Không thể tải chương ${num}. Vui lòng thử lại hoặc mở cài đặt tải offline.</p>`;
      }
    }

    function selectChapter(num) {
      closeAllDrawers();
      loadChapter(num);
    }

    function prevChapter() { if (currentChapter > 1) loadChapter(currentChapter - 1); }
    function nextChapter() { if (currentChapter < totalChapters) loadChapter(currentChapter + 1); }

    // Nav Bindings
    document.getElementById('btnFloatPrev').onclick = prevChapter;
    document.getElementById('btnFloatNext').onclick = nextChapter;
    document.getElementById('btnFooterPrev').onclick = prevChapter;
    document.getElementById('btnFooterNext').onclick = nextChapter;
    document.getElementById('btnMobilePrev').onclick = prevChapter;
    document.getElementById('btnMobileNext').onclick = nextChapter;

    // 4. Drawers & Modals Controls
    function closeAllDrawers() {
      modalOverlay.classList.remove('open');
      drawerToc.classList.remove('open');
      drawerCodex.classList.remove('open');
      settingsSheet.classList.remove('open');
    }

    function openToc() {
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerToc.classList.add('open');
    }

    function openCodex() {
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerCodex.classList.add('open');
    }

    function openSettings() {
      closeAllDrawers();
      modalOverlay.classList.add('open');
      settingsSheet.classList.add('open');
    }

    document.getElementById('btnMenu').onclick = openToc;
    document.getElementById('btnMobileToc').onclick = openToc;
    document.getElementById('btnCloseToc').onclick = closeAllDrawers;

    document.getElementById('btnCodex').onclick = openCodex;
    document.getElementById('btnMobileCodex').onclick = openCodex;
    document.getElementById('btnCloseCodex').onclick = closeAllDrawers;

    document.getElementById('btnSettings').onclick = openSettings;
    document.getElementById('btnCloseSettings').onclick = closeAllDrawers;
    modalOverlay.onclick = closeAllDrawers;

    // Codex Tab Switching
    document.querySelectorAll('.drawer-tab-btn[data-codex]').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.drawer-tab-btn[data-codex]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const codex = btn.dataset.codex;
        document.getElementById('codexPaneChar').style.display = (codex === 'char') ? 'block' : 'none';
        document.getElementById('codexPaneItem').style.display = (codex === 'item') ? 'block' : 'none';
        document.getElementById('codexPaneLotus').style.display = (codex === 'lotus') ? 'block' : 'none';
      };
    });

    // 5. Reading Progress Bar
    window.addEventListener('scroll', () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (height > 0) ? (winScroll / height) * 100 : 0;
      progressBar.style.width = scrolled + '%';
    });

    // 6. Zen Mode (Tap to toggle Top/Bottom Bars)
    novelContent.addEventListener('click', (e) => {
      if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
        uiVisible = !uiVisible;
        topHeader.classList.toggle('hidden', !uiVisible);
        bottomBar.classList.toggle('hidden', !uiVisible);
      }
    });

    // 7. Theme Controls
    function setTheme(theme) {
      document.documentElement.className = theme;
      document.body.className = theme;
      localStorage.setItem('pha_troi_theme', theme);
      document.querySelectorAll('.theme-opt').forEach(el => {
        el.classList.toggle('active', el.dataset.theme === theme);
      });
      // Toggle sun/moon icons
      const isDark = theme.includes('dark') || theme.includes('oled');
      document.getElementById('iconMoon').style.display = isDark ? 'inline-block' : 'none';
      document.getElementById('iconSun').style.display = isDark ? 'none' : 'inline-block';

      const themeColors = {
        'theme-peaceful-dark': '#08090d',
        'theme-gentle-light': '#f7f5f0',
        'theme-sepia': '#f4edd8',
        'theme-oled': '#000000'
      };
      const themeMeta = document.querySelector('meta[name="theme-color"]');
      if (themeMeta && themeColors[theme]) {
        themeMeta.setAttribute('content', themeColors[theme]);
      }
    }

    document.querySelectorAll('.theme-opt').forEach(btn => {
      btn.onclick = () => setTheme(btn.dataset.theme);
    });

    // Quick Theme Switcher Button (Toggle between Peaceful Dark and Gentle Light)
    document.getElementById('btnQuickTheme').onclick = () => {
      const cur = document.body.className;
      if (cur === 'theme-gentle-light') {
        setTheme('theme-peaceful-dark');
        showToast('🌙 Đã chuyển sang Chế độ Tối Bình Yên');
      } else {
        setTheme('theme-gentle-light');
        showToast('☀️ Đã chuyển sang Chế độ Sáng Thanh Nhã');
      }
    };

    // Load initial theme
    const savedTheme = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
    setTheme(savedTheme);

    // 8. Typography Controls
    let curFontSize = parseInt(localStorage.getItem('pha_troi_font_size') || '19');
    function updateFontSize(sz) {
      curFontSize = Math.min(Math.max(sz, 15), 28);
      document.documentElement.style.setProperty('--font-size', curFontSize + 'px');
      document.getElementById('fontSizeVal').innerText = curFontSize;
      localStorage.setItem('pha_troi_font_size', curFontSize);
    }
    document.getElementById('btnFontInc').onclick = () => updateFontSize(curFontSize + 1);
    document.getElementById('btnFontDec').onclick = () => updateFontSize(curFontSize - 1);
    updateFontSize(curFontSize);

    const FONT_SERIF = "'Lora', 'Merriweather', 'Cambria', 'Georgia', 'Times New Roman', serif";
    const FONT_SANS = "'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";

    document.getElementById('btnFontSerif').onclick = () => {
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
      localStorage.setItem('pha_troi_font_family', 'serif');
      showToast('📖 Phông chữ Có Chân (Lora Book)');
    };
    document.getElementById('btnFontSans').onclick = () => {
      document.documentElement.style.setProperty('--font-family', FONT_SANS);
      document.body.style.setProperty('--font-family', FONT_SANS);
      localStorage.setItem('pha_troi_font_family', 'sans');
      showToast('📱 Phông chữ Không Chân (Be Vietnam Pro)');
    };

    const savedFont = localStorage.getItem('pha_troi_font_family');
    if (savedFont === 'serif') {
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
    }

    // 9. Keyboard Shortcuts (Desktop Widescreen)
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowLeft') prevChapter();
      else if (e.key === 'ArrowRight') nextChapter();
      else if (e.key.toLowerCase() === 't') document.getElementById('btnQuickTheme').click();
      else if (e.key.toLowerCase() === 'm') openToc();
      else if (e.key.toLowerCase() === 'c') openCodex();
      else if (e.key === 'Escape') closeAllDrawers();
    });

    // 10. Toast Helper
    function showToast(msg) {
      toastMsg.innerText = msg;
      liveToast.classList.add('show');
      setTimeout(() => liveToast.classList.remove('show'), 2400);
    }

    // 11. Cache All Chapters for Offline Reading
    document.getElementById('btnCacheAll').onclick = async () => {
      const btn = document.getElementById('btnCacheAll');
      const text = document.getElementById('cacheAllText');
      btn.disabled = true;
      text.innerText = "Đang tải dữ liệu 57 chương...";

      try {
        const urlsToCache = [
          './data/chapters.json',
          './icon.svg',
          './manifest.json'
        ];
        for (let i = 1; i <= totalChapters; i++) {
          urlsToCache.push(`./data/chapter_${i}.json`);
        }

        if ('caches' in window) {
          const cache = await caches.open('pha-troi-v2-complete');
          let count = 0;
          for (const url of urlsToCache) {
            try {
              const res = await fetch(url);
              if (res.ok) await cache.put(url, res);
              count++;
              text.innerText = `Đang lưu offline: ${count}/${urlsToCache.length}...`;
            } catch (e) {}
          }
          text.innerText = `Đã lưu xong ${count} tập tin offline!`;
          showToast(`✨ Đã tải trọn bộ offline thành công!`);
        } else {
          text.innerText = "Trình duyệt không hỗ trợ Cache Storage";
        }
      } catch (err) {
        text.innerText = "Lỗi khi lưu offline";
      } finally {
        setTimeout(() => {
          btn.disabled = false;
          text.innerText = "Tải Toàn Bộ 57 Chương Để Đọc Offline";
        }, 3500);
      }
    };

    // Initial Load
    loadChaptersIndex(true);

    // Register Service Worker for PWA
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').catch(() => {});
      });
    }
  </script>
</body>
</html>"""

def generate_sw():
    return """// Service Worker cho Web Reader Phá Trời
const CACHE_NAME = 'pha-troi-reader-v3';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './cover.svg',
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
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const isHtml = e.request.mode === 'navigate' || (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html'));
  if (isHtml) {
    e.respondWith(
      fetch(e.request).then((res) => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
        }
        return res;
      }).catch(() => caches.match(e.request).then((cached) => cached || caches.match('./index.html')))
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, responseClone);
          });
        }
        return networkResponse;
      }).catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
"""

def build():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)
    data_dir = os.path.join(DIST_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. Parse all chapters recursively from manuscript directory
    chapter_paths = []
    base_manuscript = os.path.join(BASE_DIR, "manuscript", "markdown")
    for root, _, flist in os.walk(base_manuscript):
        for f in flist:
            if f.endswith(".md") and f.startswith("ch_"):
                chapter_paths.append(os.path.join(root, f))
    
    def extract_ch(p):
        m = re.search(r'ch_(\d+)', os.path.basename(p))
        return int(m.group(1)) if m else 9999
    
    chapter_paths.sort(key=extract_ch)

    chapters_index = []
    total_words = 0
    for path in chapter_paths:
        info = parse_chapter_file(path)
        total_words += info["word_count"]
        
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
        "updated_at": "2026-10-18T08:00:00+07:00",
        "chapters": chapters_index
    }
    with open(os.path.join(data_dir, "chapters.json"), "w", encoding="utf-8") as out:
        json.dump(index_data, out, ensure_ascii=False, indent=1)

    # 2. Generate index.html
    html_content = generate_html(chapters_index, total_words)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as out:
        out.write(html_content)

    # 3. Generate sw.js
    with open(os.path.join(DIST_DIR, "sw.js"), "w", encoding="utf-8") as out:
        out.write(generate_sw())

    # 4. Generate cover.svg
    cover_svg_content = generate_cover_svg()
    with open(os.path.join(DIST_DIR, "cover.svg"), "w", encoding="utf-8") as out:
        out.write(cover_svg_content)

    # 5. Generate manifest.json
    manifest_data = {
        "name": "Phá Trời — Tiểu Thuyết Đô Thị Tu Chân",
        "short_name": "Phá Trời",
        "description": "Ứng dụng đọc truyện trọn bộ thời gian thực cho Phá Trời",
        "start_url": "./index.html",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#08090d",
        "theme_color": "#08090d",
        "icons": [
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

    # 6. Copy icon.svg
    src_icon = os.path.join(BASE_DIR, "system", "reader_app", "static", "icon.svg")
    dst_icon = os.path.join(DIST_DIR, "icon.svg")
    if os.path.exists(src_icon):
        shutil.copy2(src_icon, dst_icon)

    print(f"[Build Complete] {len(chapters_index)} chuong ({total_words:,} tu) -> {DIST_DIR}")
    return len(chapters_index), total_words

if __name__ == "__main__":
    build()
