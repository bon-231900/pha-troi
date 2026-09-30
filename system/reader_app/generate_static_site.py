# -*- coding: utf-8 -*-
"""
NovelOS — Trình tạo ứng dụng Web Đọc Tĩnh Phá Trời (Clean Slugs SSG)
Phiên bản 2.5: Đầy đủ 12 Phase trải nghiệm đọc truyện hoàn chỉnh
Bảo tồn visual identity, tối ưu mobile, PWA offline, SEO, Reader UX.
"""
import os
import sys
import json
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
import sqlite3
import markdown

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.getenv("NOVEL_OS_ROOT", str(Path(__file__).resolve().parent.parent.parent))
DIST_DIR = os.path.join(BASE_DIR, "system", "reader_app", "dist")
STATIC_SRC_DIR = os.path.join(BASE_DIR, "system", "reader_app", "static")
SITE_URL = os.getenv("SITE_URL", "https://phatroi.com")
GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID", "G-PELE9QCESB")
ASSET_VERSION = int(time.time())

try:
    from system.reader_app.seo_pages import SEO_PAGES, render_seo_page_html
except ImportError:
    from seo_pages import SEO_PAGES, render_seo_page_html

def get_db_chapter_summaries():
    """Doc tom tat tung chuong tu timeline_events trong novel_os.db."""
    db_path = os.path.join(BASE_DIR, "database", "novel_os.db")
    if not os.path.exists(db_path):
        return {}
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT chapter_num, summary FROM timeline_events")
        res = {row[0]: row[1] for row in cur.fetchall()}
        conn.close()
        return res
    except Exception as e:
        print(f"[WARN] Khong the doc timeline_events tu novel_os.db: {e}")
        return {}

def optimize_seo_title(ch_num, clean_title, custom_title=""):
    """Toi uu Title cho Google SERP trong khoang 48-60 ky tu."""
    if custom_title:
        return custom_title if "| phatroi.com" in custom_title else f"{custom_title} | phatroi.com"
    full = f"Phá Trời Chương {ch_num}: {clean_title} — Đọc Online | phatroi.com"
    if len(full) <= 60:
        return full
    v2 = f"Phá Trời Chương {ch_num}: {clean_title} | phatroi.com"
    if len(v2) <= 60:
        return v2
    prefix = f"Phá Trời Chương {ch_num}: "
    suffix = " | phatroi.com"
    avail = 60 - len(prefix) - len(suffix) - 3
    short_clean = clean_title[:avail].rsplit(' ', 1)[0].strip() + "..."
    return f"{prefix}{short_clean}{suffix}"

def clean_body_narrative(text):
    """Loc bo cac moc thoi gian mo dau de lay cau tu su hap dan."""
    t = re.sub(r'^[#*\-—\s]+', '', text).strip()
    t = re.sub(r'^(Năm|Sáu|Bảy|Tám|Chín|Mười|Mười một|Mười hai|\d+)\s+giờ(\s+\d+\s+phút)?\s+(sáng|trưa|chiều|tối|đêm)[^.]*\.\s*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'^(Ngày\s+\d+\s+tháng\s+\d+[^.]*\.\s*)', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def optimize_seo_description(ch_num, clean_title, custom_desc="", db_summary="", plain_text=""):
    """Toi uu Description cho Google SERP Snippet trong khoang 145-158 ky tu."""
    TARGET_MIN = 145
    TARGET_MAX = 158

    candidate = custom_desc.strip() if custom_desc else ""
    if not candidate and db_summary:
        candidate = db_summary.strip()
    if not candidate:
        candidate = clean_body_narrative(plain_text)

    candidate = re.sub(r'\s+', ' ', candidate).strip()

    # Mau 1: Doc Pha Troi Chuong {ch_num}: {clean_title}. {snippet}... Doc mien phi tai phatroi.com.
    prefix = f"Đọc Phá Trời Chương {ch_num}: {clean_title}."
    cta_short = " Đọc miễn phí tại phatroi.com."
    avail = TARGET_MAX - len(prefix) - len(cta_short) - 1

    if avail >= 25:
        cut = candidate[:avail - 3].rsplit(' ', 1)[0].strip().rstrip('.,;:-')
        candidate_snippet = f"{prefix} {cut}...{cta_short}"
        if TARGET_MIN <= len(candidate_snippet) <= TARGET_MAX:
            return candidate_snippet

    # Mau 2: {snippet}... — Doc Pha Troi Chuong {ch_num} tai phatroi.com.
    cta_ch = f" — Đọc Phá Trời Chương {ch_num} tại phatroi.com."
    avail_ch = TARGET_MAX - len(cta_ch)
    if avail_ch >= 30:
        cut_ch = candidate[:avail_ch - 3].rsplit(' ', 1)[0].strip().rstrip('.,;:-')
        candidate_ch = f"{cut_ch}...{cta_ch}"
        if TARGET_MIN <= len(candidate_ch) <= TARGET_MAX:
            return candidate_ch

    # Mau 3: {snippet}... — Doc tieu thuyet Pha Troi Chuong {ch_num} tai phatroi.com.
    cta_long = f" — Đọc tiểu thuyết Phá Trời Chương {ch_num} tại phatroi.com."
    avail_long = TARGET_MAX - len(cta_long)
    if avail_long >= 20:
        cut_long = candidate[:avail_long - 3].rsplit(' ', 1)[0].strip().rstrip('.,;:-')
        candidate_long = f"{cut_long}...{cta_long}"
        if TARGET_MIN <= len(candidate_long) <= TARGET_MAX:
            return candidate_long

    # Mau 4: Fallback can chinh padding
    base_prefix = f"Đọc Phá Trời Chương {ch_num}: {clean_title}. "
    avail_fill = TARGET_MAX - len(base_prefix) - len(" Đọc tại phatroi.com.")
    fill_cut = candidate[:avail_fill - 3].rsplit(' ', 1)[0].strip().rstrip('.,;:-')
    res = f"{base_prefix}{fill_cut}... Đọc tại phatroi.com."

    if len(res) < TARGET_MIN:
        res = res.replace(" Đọc tại phatroi.com.", " Đọc truyện online miễn phí tại phatroi.com.")
        if len(res) > TARGET_MAX:
            res = res[:TARGET_MAX - 3].rsplit(' ', 1)[0].strip().rstrip('.,;:-') + "..."

    return res[:TARGET_MAX]


def get_codex_items():
    reg_path = os.path.join(BASE_DIR, "canon", "codex", "codex_registry.json")
    if os.path.exists(reg_path):
        try:
            with open(reg_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Khong the doc codex_registry.json: {e}")
    return []

CHAPTER_LOCATIONS_FALLBACK = {
    1: "Ngã tư Hàng Xanh & Đường Ung Văn Khiêm, Bình Thạnh, TP.HCM",
    2: "Phòng trọ đường Ung Văn Khiêm, Bình Thạnh, TP.HCM",
    3: "Sông Sài Gòn & Bán đảo Thanh Đa, Bình Thạnh, TP.HCM",
    4: "Quán cà phê cóc đường D2 (Nguyễn Gia Trí), Bình Thạnh, TP.HCM",
    5: "Bờ kè kênh Nhiêu Lộc - Thị Nghè, TP.HCM",
    6: "Phòng trọ Ung Văn Khiêm, Bình Thạnh, TP.HCM",
    7: "Ngã tư Hàng Xanh & Cầu Sài Gòn, TP.HCM",
    8: "Phòng trọ mái tôn, Bình Thạnh, TP.HCM",
    9: "Bờ kênh Nhiêu Lộc & Cầu Thị Nghè, TP.HCM",
    10: "Bến Bạch Đằng & Sông Sài Gòn, Quận 1, TP.HCM",
    11: "Tòa nhà văn phòng Quận 1, TP.HCM",
    12: "Phòng trọ Bình Thạnh & Thức hải Minh An, TP.HCM",
    13: "Công viên bờ sông Sài Gòn, TP. Thủ Đức, TP.HCM",
    14: "Quán trà cổ đường Lương Nhữ Học, Quận 5, TP.HCM",
    15: "Tòa nhà văn phòng Quận 1 & Trung tâm dữ liệu, TP.HCM",
    16: "Võ đường cổ hẻm đường Trần Hưng Đạo, Quận 5, TP.HCM",
    17: "Dòng kênh Tàu Hủ & Bến Bình Đông, Quận 8, TP.HCM",
    18: "Võ đường cổ Quận 5 & Phòng trọ Bình Thạnh, TP.HCM",
    19: "Đại lộ Mai Chí Thọ & Hầm Thủ Thiêm, TP.HCM",
    20: "Đỉnh tòa tháp Bitexco & Bầu trời Quận 1, TP.HCM",
    21: "Bàn trà đêm bờ sông Sài Gòn, Quận 1, TP.HCM",
    22: "Địa tầng ngầm Sài Gòn & Thức hải Minh An, TP.HCM"
}

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

    # Normalize ALL CAPS chapter titles to Title Case
    m_ch = re.match(r'^(Chương\s+\d+:\s*)(.+)$', title, flags=re.IGNORECASE)
    if m_ch:
        ch_digits = re.search(r'\d+', m_ch.group(1)).group(0)
        prefix = f"Chương {ch_digits}: "
        sub_t = m_ch.group(2).strip()
        if not any(c.islower() for c in sub_t):
            sub_t = " ".join(w.capitalize() for w in sub_t.split())
        title = prefix + sub_t
    elif not any(c.islower() for c in title):
        title = " ".join(w.capitalize() for w in title.split())
    
    # Remove # Title from markdown body
    body_clean = re.sub(r"^#\s+.+$\n*", "", body, count=1, flags=re.MULTILINE)

    html_content = markdown.markdown(body_clean, extensions=["extra", "nl2br"])
    
    # Plain text excerpt for SEO
    plain_text = re.sub(r'<[^>]+>', ' ', html_content)
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()
    excerpt = (plain_text[:160] + '...') if len(plain_text) > 160 else plain_text

    ch_num = int(meta.get("chapter", fallback_num))
    location = meta.get("location", "")
    if not location and ch_num in CHAPTER_LOCATIONS_FALLBACK:
        location = CHAPTER_LOCATIONS_FALLBACK[ch_num]

    custom_desc = meta.get("description", "") or meta.get("seo_description", "") or meta.get("desc", "")
    custom_title = meta.get("seo_title", "")

    return {
        "chapter": ch_num,
        "title": title,
        "volume": int(meta.get("volume", 1)),
        "arc": int(meta.get("arc", 1)),
        "word_count": int(meta.get("word_count", len(body.split()))),
        "date": meta.get("date", "2026-10-07"),
        "location": location,
        "excerpt": excerpt,
        "plain_text": plain_text,
        "custom_desc": custom_desc.strip(),
        "custom_title": custom_title.strip(),
        "html": html_content
    }

def get_shared_css():
    return """
    :root {
      /* Typography Tokens */
      --font-reading: 'Lora', 'Georgia', serif;
      --font-ui: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-family: var(--font-ui);
      --font-size: 19px;
      --reader-line-height: 1.85;
      --reader-max-width: 740px;

      /* Spacing Scale (8pt System) */
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 24px;
      --space-6: 32px;
      --space-7: 48px;
      --space-8: 64px;

      /* Radii (Clean, non-pill) */
      --radius-sm: 4px;
      --radius-md: 6px;
      --radius-lg: 8px;

      /* Motion */
      --motion-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
      --motion-base: 220ms cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Theme 1: Saigon Night (Mặc định - Deep Blue-Black & Rain Blue) */
    :root, html.theme-peaceful-dark, body.theme-peaceful-dark, html.theme-saigon-night, body.theme-saigon-night {
      --bg-color: #0b0f17;
      --bg-gradient: radial-gradient(ellipse at 50% 0%, #111827 0%, #0b0f17 75%);
      --text-color: #e2e8f0;
      --text-muted: #8492a6;
      --header-bg: #0b0f17;
      --card-bg: #111722;
      --card-bg-hover: #182232;
      --border-color: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.04);
      --accent-primary: #517a8f;
      --accent-hover: #638fa6;
      --gold-primary: #e5c07b;
      --gold-hover: #f3d498;
      --cyan-subtle: #41677d;
    }

    /* Theme 2: Warm Dark (Trầm Ấm - Warm Charcoal & Warm Ivory) */
    html.theme-warm-dark, body.theme-warm-dark, html.theme-oled, body.theme-oled {
      --bg-color: #121110;
      --bg-gradient: radial-gradient(ellipse at 50% 0%, #1a1816 0%, #121110 75%);
      --text-color: #e6dfd5;
      --text-muted: #91887e;
      --header-bg: #121110;
      --card-bg: #181715;
      --card-bg-hover: #211f1c;
      --border-color: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.04);
      --accent-primary: #8a7a60;
      --accent-hover: #a19074;
      --gold-primary: #e5c07b;
      --gold-hover: #f3d498;
      --cyan-subtle: #635847;
    }

    /* Theme 3: Sepia (Thư Tịch Cổ - Warm Paper & Dark Brown) */
    html.theme-sepia, body.theme-sepia {
      --bg-color: #f1e8d0;
      --bg-gradient: radial-gradient(circle at 50% 0%, #f8f1de 0%, #f1e8d0 85%);
      --text-color: #3b2d1d;
      --text-muted: #7d6a55;
      --header-bg: #f1e8d0;
      --card-bg: #e6dcbe;
      --card-bg-hover: #ded2b2;
      --border-color: rgba(100, 75, 50, 0.14);
      --border-subtle: rgba(100, 75, 50, 0.07);
      --accent-primary: #4d6d63;
      --accent-hover: #3b574e;
      --gold-primary: #8c5b1e;
      --gold-hover: #734814;
      --cyan-subtle: #415e55;
    }

    /* Theme 4: Paper (Giấy Sáng / Editorial Light - Soft Off-White & Dark Neutral) */
    html.theme-gentle-light, body.theme-gentle-light, html.theme-paper, body.theme-paper {
      --bg-color: #f7f5f0;
      --bg-gradient: radial-gradient(circle at 50% 0%, #ffffff 0%, #f7f5f0 85%);
      --text-color: #24221f;
      --text-muted: #6b665f;
      --header-bg: #f7f5f0;
      --card-bg: #ede9df;
      --card-bg-hover: #e4dfd3;
      --border-color: rgba(0, 0, 0, 0.09);
      --border-subtle: rgba(0, 0, 0, 0.05);
      --accent-primary: #3d6070;
      --accent-hover: #2e4b58;
      --gold-primary: #8f6b28;
      --gold-hover: #73541c;
      --cyan-subtle: #355363;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
    html { scroll-behavior: smooth; background-color: var(--bg-color); }
    body {
      font-family: var(--font-family); background: var(--bg-gradient); background-color: var(--bg-color);
      color: var(--text-color); min-height: 100vh; overflow-x: hidden; line-height: var(--reader-line-height);
      transition: background 0.3s ease, color 0.3s ease;
      position: relative;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.02'/%3E%3C/svg%3E");
      pointer-events: none;
      z-index: 9999;
    }
    a { color: inherit; text-decoration: none; }

    /* Editorial Typography Principles */
    h1, h2, h3, h4, h5, h6 { text-wrap: balance; }
    p { text-wrap: pretty; }

    /* Accessibility focus and motion */
    :focus-visible { outline: 2px solid var(--accent-primary); outline-offset: 2px; }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-color); }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

    #progressBarContainer {
      position: fixed; top: 0; left: 0; width: 100%; height: 2px; background: transparent; z-index: 1050; pointer-events: none;
    }
    #progressBar {
      height: 100%; width: 0%; background: var(--gold-primary);
      transition: width 0.1s ease-out;
    }

    header#topHeader {
      position: sticky; top: 0; left: 0; right: 0; width: 100%; max-width: 100vw; box-sizing: border-box;
      height: calc(56px + env(safe-area-inset-top, 0px));
      padding: env(safe-area-inset-top, 0px) 20px 0 20px;
      background: var(--header-bg);
      border-bottom: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-between; z-index: 999;
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), background 0.3s ease;
    }
    header#topHeader.header-unpinned { transform: translateY(-100%) !important; }
    header#topHeader.header-pinned { transform: translateY(0) !important; }
    .header-left { display: flex; align-items: center; gap: 8px; flex-shrink: 0; z-index: 2; }
    .header-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; z-index: 2; margin-left: auto; }
    .btn-brand {
      display: inline-flex; align-items: center; gap: 10px; background: none; border: none;
      cursor: pointer; padding: 4px 6px; border-radius: 6px; transition: opacity 0.2s ease;
    }
    .btn-brand:hover { opacity: 0.85; }
    .nav-logo {
      width: 32px; height: 32px; border-radius: 50%; border: 1.5px solid var(--gold-primary);
      object-fit: cover;
    }
    .nav-brand-text {
      font-family: 'Lora', 'Georgia', serif; font-size: 15px; font-weight: 700; letter-spacing: 1.5px; color: var(--gold-primary);
    }
    .nav-live-badge {
      display: none; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 4px;
      background: transparent; border: 1px solid var(--border-color);
      font-size: 11px; font-weight: 500; color: var(--text-muted);
    }
    @media (min-width: 900px) { .nav-live-badge { display: inline-flex; } }

    .header-center {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      padding: 0 8px;
      max-width: min(560px, calc(100% - 480px));
      min-width: 0;
      overflow: hidden;
      pointer-events: none;
      z-index: 1;
    }
    /* Header Center on Homepage - Hidden initially, revealed when scrolling past Hero */
    body.is-home .header-center {
      opacity: 0;
      transform: translate(-50%, -70%);
      pointer-events: none;
      transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1), transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    body.is-home header#topHeader.scrolled-past-hero .header-center {
      opacity: 1;
      transform: translate(-50%, -50%);
      pointer-events: auto;
    }
    header#topHeader.scrolled-past-hero {
      border-bottom-color: rgba(229, 192, 123, 0.2);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    .header-title {
      display: block; width: 100%;
      font-size: 13.5px; font-weight: 600; color: var(--text-color); white-space: nowrap;
      overflow: hidden; text-overflow: ellipsis; margin: 0; letter-spacing: 0.3px;
    }
    .header-sub {
      display: block; width: 100%;
      font-size: 11px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin: 0; opacity: 0.85;
    }
    .reader-progress-badge {
      font-size: 10.5px; font-weight: 600; color: var(--gold-primary);
      background: transparent; border: 1px solid var(--border-color);
      padding: 1px 6px; border-radius: 4px; display: inline-flex; align-items: center;
      margin-left: 6px; vertical-align: middle;
    }

    .btn-icon {
      background: none; border: 1px solid transparent; color: var(--text-muted); width: 36px; height: 36px;
      cursor: pointer; display: inline-flex; align-items: center; justify-content: center;
      border-radius: 6px; transition: color 0.2s, border-color 0.2s; position: relative; flex-shrink: 0;
    }
    .btn-icon:hover { color: var(--gold-primary); border-color: var(--border-color); }
    .btn-icon:active { transform: scale(0.96); }

    .btn-nav-home-pill {
      display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: var(--radius-md);
      background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-muted); font-size: 12px; font-weight: 600; cursor: pointer; transition: all var(--motion-fast);
      white-space: nowrap;
    }
    .btn-nav-home-pill:hover { border-color: var(--gold-primary); color: var(--gold-primary); }

    @media (max-width: 768px) {
      .btn-nav-home-pill { display: none !important; }
      .header-desktop-only { display: none !important; }
      header#topHeader { padding: env(safe-area-inset-top, 0px) 10px 0 10px; }
      .header-left, .header-right { gap: 4px; }
      .header-center { max-width: calc(100% - 200px); }
      .btn-icon { width: 35px; height: 35px; }
      .nav-brand-text { font-size: 14px; letter-spacing: 0.8px; }
      .nav-logo { width: 30px; height: 30px; }
      body.is-home:not(.scrolled-past-hero) .header-center { display: none; }
      body.is-home header#topHeader.scrolled-past-hero .header-center { display: block; }
    }

    .dot-live {
      width: 6px; height: 6px; border-radius: 50%; background: var(--gold-primary);
      opacity: 0.85;
    }

    /* Chapter Meta Badges */
    .chapter-meta-pills {
      display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 8px; font-size: 12px;
    }
    .meta-pill {
      display: inline-flex; align-items: center; gap: 5px; padding: 4px 11px; border-radius: 20px;
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color); color: var(--text-muted);
      font-size: 11.5px; font-weight: 500;
    }

    /* Modals, Drawers & Bottom Sheet */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.72); backdrop-filter: blur(4px);
      z-index: 1000; opacity: 0; pointer-events: none; transition: opacity 0.25s ease;
    }
    .modal-overlay.open { opacity: 1; pointer-events: auto; }

    .drawer {
      position: fixed; top: 0; bottom: 0; width: 88%; max-width: 400px; background: var(--card-bg);
      border-left: 1px solid var(--border-color); z-index: 1001; display: flex; flex-direction: column;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: -8px 0 24px rgba(0, 0, 0, 0.4);
      box-sizing: border-box;
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

    /* TOC Progress Summary */
    .toc-progress-summary {
      padding: 12px 16px; border-bottom: 1px solid var(--border-color); background: rgba(0, 0, 0, 0.12);
    }
    .toc-progress-text {
      display: flex; justify-content: space-between; font-size: 12px; font-weight: 600;
      color: var(--text-muted); margin-bottom: 6px;
    }
    .toc-progress-text strong { color: var(--gold-primary); }
    .toc-progress-track {
      width: 100%; height: 5px; border-radius: 3px; background: rgba(255, 255, 255, 0.08); overflow: hidden;
    }
    .toc-progress-fill {
      height: 100%; background: linear-gradient(90deg, var(--gold-primary), var(--accent-primary));
      border-radius: 3px; transition: width 0.3s ease;
    }

    /* TOC items */
    .toc-item {
      padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer;
      display: flex; align-items: center; justify-content: space-between; border: 1px solid transparent;
      border-left: 2px solid transparent;
      transition: all 0.18s ease; text-decoration: none; color: inherit; box-sizing: border-box;
    }
    .toc-item:hover { background: var(--card-bg-hover); border-color: var(--border-color); border-left-color: var(--gold-primary); }
    .toc-item.active { background: rgba(229, 192, 123, 0.08); border-color: var(--gold-primary); border-left-color: var(--gold-primary); }
    .toc-item.active .toc-name { color: var(--gold-primary); font-weight: 700; }
    .toc-info { min-width: 0; flex: 1; margin-right: 10px; overflow: hidden; }
    .toc-num {
      font-size: 11px; color: var(--gold-primary); font-weight: 700; text-transform: uppercase;
      margin-bottom: 2px; display: flex; align-items: center; gap: 6px;
    }
    .toc-num::before {
      content: "❖";
      font-size: 8px;
      opacity: 0.85;
    }
    .toc-name { font-size: 13px; color: var(--text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .toc-meta { font-size: 11px; color: var(--text-muted); flex-shrink: 0; }

    /* Chapter Status Indicators - Editorial */
    .ch-status-tag {
      font-size: 10px; font-weight: 600; padding: 1px 6px; border-radius: 3px;
      display: inline-flex; align-items: center; gap: 3px;
    }
    .ch-status-tag.read {
      background: transparent; color: var(--text-muted); border: 1px solid var(--border-subtle);
    }
    .ch-status-tag.current {
      background: rgba(229, 192, 123, 0.12); color: var(--gold-primary); border: 1px solid var(--gold-primary);
    }
    .ch-status-tag.unread {
      display: none;
    }

    /* Codex Drawer Styles */
    .codex-progress-pill {
      font-size: 11px; font-weight: 600; color: var(--gold-primary);
      background: transparent; border: 1px solid var(--border-color);
      padding: 2px 8px; border-radius: 4px; display: inline-flex; align-items: center; gap: 5px;
    }
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
      border-top: 1px solid var(--border-color); border-radius: 20px 20px 0 0; max-width: 580px; width: 100%;
      box-sizing: border-box; margin: 0 auto;
      padding: 20px 20px calc(36px + env(safe-area-inset-bottom, 0px)) 20px; transform: translateY(100%);
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
    .theme-opt.active { border-color: var(--gold-primary); outline: 2px solid var(--gold-primary); outline-offset: 1px; }

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
    .btn-opt-step:hover { border-color: var(--gold-primary); color: var(--gold-primary); }
    .btn-opt-step.active { background: rgba(229, 192, 123, 0.12); border-color: var(--gold-primary); color: var(--gold-primary); }

    .ambient-widget {
      display: flex; align-items: center; justify-content: space-between; padding: 10px 14px;
      border-radius: 10px; background: rgba(0,0,0,0.15); border: 1px solid var(--border-color); margin-top: 10px;
    }

    #liveToast {
      position: fixed; bottom: 74px; left: 50%; transform: translateX(-50%) translateY(30px);
      background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-color);
      font-size: 13px; font-weight: 600; padding: 9px 18px; border-radius: var(--radius-lg);
      box-shadow: 0 4px 16px rgba(0,0,0,0.3); opacity: 0; pointer-events: none;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); z-index: 2000; white-space: nowrap; display: flex; align-items: center; gap: 8px;
    }
    #liveToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    """

def generate_cover_svg(total_ch=81):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#141c2b"/>
      <stop offset="60%" stop-color="#0b0f17"/>
      <stop offset="100%" stop-color="#070a10"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bgGrad)"/>
  <rect x="36" y="36" width="1128" height="558" fill="none" stroke="rgba(229,192,123,0.35)" stroke-width="1.2"/>
  <rect x="44" y="44" width="1112" height="542" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  
  <text x="600" y="125" fill="#e5c07b" font-family="'Be Vietnam Pro', -apple-system, sans-serif" font-size="13" font-weight="600" letter-spacing="4" text-anchor="middle">ĐẠI TRƯỜNG THIÊN THỂ ĐẠO PHÀM NHÂN · ĐỊA CHẤT NON SÔNG 2026</text>
  
  <text x="600" y="260" fill="#e5c07b" font-family="'Lora', 'Georgia', serif" font-size="96" font-weight="700" letter-spacing="12" text-anchor="middle">PHÁ TRỜI</text>
  <text x="600" y="315" fill="#8492a6" font-family="'Lora', 'Georgia', serif" font-size="24" font-weight="400" letter-spacing="6" text-anchor="middle">THỂ ĐẠO PHÀM NHÂN</text>
  
  <text x="600" y="375" fill="#e5c07b" font-size="18" letter-spacing="6" text-anchor="middle">· ✦ ·</text>
  
  <text x="600" y="440" fill="#e2e8f0" font-family="'Lora', 'Georgia', serif" font-size="20" font-style="italic" text-anchor="middle">"Hành trình phàm nhân Thể Đạo dãi dầu sương gió, khám phá bí ẩn địa chất non sông."</text>
  
  <text x="600" y="525" fill="#8492a6" font-family="'Be Vietnam Pro', -apple-system, sans-serif" font-size="13" font-weight="500" letter-spacing="2.5" text-anchor="middle">TÁC GIẢ: AN BÌNH · {total_ch} CHƯƠNG HOÀN THIỆN · ĐỌC ONLINE &amp; OFFLINE</text>
  <text x="600" y="555" fill="#517a8f" font-family="'Be Vietnam Pro', -apple-system, sans-serif" font-size="11.5" letter-spacing="1.5" text-anchor="middle">PHATROI.COM · TOÀN BỘ BẢN QUYỀN ĐƯỢC BẢO LƯU</text>
</svg>"""

def generate_404_html():
    return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Đang chuyển hướng — Phá Trời</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, follow">
  <script>
    (function() {
      var path = window.location.pathname;
      var match = path.match(/(?:chuong|chapter)[-_/]?(\\d+)/i);
      var prefix = (path.indexOf('/pha-troi') === 0) ? '/pha-troi' : '';
      if (match) {
        window.location.replace(prefix + '/chuong-' + match[1] + '/');
      } else {
        window.location.replace(prefix + '/');
      }
    })();
  </script>
</head>
<body style="background:#0b0f17; color:#e2e8f0; font-family:'Be Vietnam Pro', sans-serif; display:flex; align-items:center; justify-content:center; height:100vh; margin:0; text-align:center;">
  <div style="max-width:480px; padding:24px;">
    <div style="font-family:'Lora', serif; font-size:32px; font-weight:700; color:#e5c07b; margin-bottom:12px; letter-spacing:2px;">PHÁ TRỜI</div>
    <p style="color:#8492a6; font-size:15px; line-height:1.6;">Đang kết nối và chuyển hướng đến chương truyện...</p>
  </div>
</body>
</html>"""

def generate_sitemap_xml(chapters_index):
    today_str = datetime.now().strftime("%Y-%m-%d")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{SITE_URL}/</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{SITE_URL}/cam-nang/</loc>',
        f'    <lastmod>{today_str}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.95</priority>',
        '  </url>'
    ]

    # 8 Trang SEO & Lore vệ tinh
    seo_slugs = [
        "phat-troi-la-truyen-gi",
        "truyen-tu-tien-viet-nam-sai-gon",
        "do-thi-tu-chan-la-gi",
        "the-dao",
        "nguyen-minh-an",
        "thap-nhi-tieu",
        "canh-gioi-the-dao",
        "bach-y-than-nu-lam-tich"
    ]
    for slug in seo_slugs:
        lines.append('  <url>')
        lines.append(f'    <loc>{SITE_URL}/{slug}/</loc>')
        lines.append(f'    <lastmod>{today_str}</lastmod>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.9</priority>')
        lines.append('  </url>')

    for ch in chapters_index:
        ch_num = ch["chapter"]
        lines.append('  <url>')
        lines.append(f'    <loc>{SITE_URL}/chuong-{ch_num}/</loc>')
        lines.append(f'    <lastmod>{today_str}</lastmod>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.8</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')
    return "\n".join(lines) + "\n"

def generate_feed_xml(chapters_index, db_summaries=None):
    """Sinh RSS 2.0 Feed chuan cho cac app doc tin (Feedly, NetNewsWire, Telegram Bot)."""
    now_rfc822 = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0700")
    recent_chapters = sorted(chapters_index, key=lambda x: x["chapter"], reverse=True)[:30]
    
    items_xml = []
    for ch in recent_chapters:
        ch_num = ch["chapter"]
        clean_title = ch["title"].replace(f"Chương {ch_num}:", "").strip()
        clean_title = re.sub(r"^Chương\s+\d+:\s*", "", clean_title, flags=re.IGNORECASE)
        link = f"{SITE_URL}/chuong-{ch_num}/"
        
        summary = ""
        if db_summaries and ch_num in db_summaries:
            summary = db_summaries[ch_num]
        if not summary:
            summary = ch.get("excerpt", f"Đọc Phá Trời Chương {ch_num}: {clean_title} tại phatroi.com.")
            
        words = ch.get("word_count", 2500)
        
        items_xml.append(f"""    <item>
      <title><![CDATA[Chương {ch_num}: {clean_title}]]></title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{now_rfc822}</pubDate>
      <description><![CDATA[{summary} (Độ dài: {words:,} từ)]]></description>
      <author>nguyenminhan@phatroi.com (An Bình)</author>
      <category><![CDATA[Thể Đạo phàm nhân]]></category>
    </item>""")
        
    items_str = "\n".join(items_xml)
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Phá Trời — Đại Trường Thiên Thể Đạo Phàm Nhân &amp; Địa Chất Non Sông</title>
    <link>{SITE_URL}/</link>
    <description>Bản thảo chính thức của đại trường thiên tiểu thuyết Phá Trời (tác giả An Bình). Theo dõi chương mới nhất và hành trình Thể Đạo của Nguyễn Minh An.</description>
    <language>vi</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
    <image>
      <url>{SITE_URL}/assets/logo.jpg</url>
      <title>Phá Trời</title>
      <link>{SITE_URL}/</link>
    </image>
{items_str}
  </channel>
</rss>
"""

def generate_robots_txt():
    return f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml
"""

GLOBAL_CAM_NANG_ARTICLES = [
    {
        "slug": "thap-nhi-tieu",
        "badge": "ĐỊA TẦNG & TRẬN PHÁP",
        "title": "Cẩm Nang 12 Cọc Tiêu Thủy Môn Phương Nam",
        "desc": "Hệ thống 12 cọc tiêu viễn cổ nương theo địa tầng bazan và sông ngòi từ Sài Gòn tới Tây Nguyên, khóa rạn nứt đại địa và gắn liền chuỗi di vật khảo sát năm 1996.",
        "read_mins": 8,
        "highlight": True
    },
    {
        "slug": "canh-gioi-the-dao",
        "badge": "THỂ ĐẠO KHỔ TU",
        "title": "Lộ Trình Tu Luyện Thể Đạo Phàm Nhân",
        "desc": "Giải mã 4 cảnh giới Thể Đạo trong Phá Trời: Khí Huyết Chu Thiên, Đoán Cốt, Hoán Huyết, Thần Tạng và cơ chế chiến đấu của Nguyễn Minh An thời mạt pháp.",
        "read_mins": 9,
        "highlight": True
    },
    {
        "slug": "bach-y-than-nu-lam-tich",
        "badge": "HỒ SƠ NHÂN VẬT",
        "title": "Bạch Y Thần Nữ Lâm Tịch — Nữ Kiếm Tiên Viễn Cổ",
        "desc": "Khám phá Lâm Tịch trong Phá Trời: nữ kiếm tiên viễn cổ, Băng Phách Kiếm Ý, Lục Diệp Thanh Liên và mối duyên slow burn cùng Nguyễn Minh An.",
        "read_mins": 9,
        "highlight": True
    },
    {
        "slug": "nguyen-minh-an",
        "badge": "HỒ SƠ NHÂN VẬT",
        "title": "Kỹ Sư Địa Chất Nguyễn Minh An",
        "desc": "Phàm nhân 25 tuổi mang theo búa địa chất, thanh Zil bát giác và gánh vác trách nhiệm đọc dấu vết trong lòng đá để giải mã cuộc khảo sát dang dở của người cha.",
        "read_mins": 6,
        "highlight": False
    },
    {
        "slug": "the-dao",
        "badge": "CỐT TỦY HỆ THỐNG",
        "title": "Bản Chất Thể Đạo: Khổ Tu Phàm Nhân",
        "desc": "Phân tích nguyên lý thể xác làm đỉnh lô, tinh huyết làm than lửa. Sự đối lập triệt để giữa khổ tu thực chiến và con đường tu chân linh căn truyền thống.",
        "read_mins": 7,
        "highlight": False
    },
    {
        "slug": "phat-troi-la-truyen-gi",
        "badge": "TỔNG QUAN TÁC PHẨM",
        "title": "Phá Trời Là Truyện Gì? Cẩm Nang Toàn Diện",
        "desc": "Tổng quan đại trường thiên đô thị tu chân Sài Gòn 2026: bối cảnh địa tầng non sông, phong cách Thể Đạo và triết lý sáng tác thuần túy khoa học thực nghiệm.",
        "read_mins": 7,
        "highlight": False
    },
    {
        "slug": "truyen-tu-tien-viet-nam-sai-gon",
        "badge": "TIỂU LUẬN BẢN ĐỊA",
        "title": "Tiên Hiệp Bản Địa Sài Gòn: Khi Cổ Giới Thức Giấc",
        "desc": "Khám phá vì sao Phá Trời cắm rễ vào thực địa sông Sài Gòn, bán đảo Thanh Đa, kênh Nhiêu Lộc thay vì bối cảnh tiên hiệp cổ trang xa lạ.",
        "read_mins": 8,
        "highlight": False
    },
    {
        "slug": "do-thi-tu-chan-la-gi",
        "badge": "NGHIÊN CỨU THỂ LOẠI",
        "title": "Giải Mã Thể Loại Đô Thị Tu Chân Hiện Đại",
        "desc": "Phân tích sự va chạm giữa nhịp sống công nghiệp hiện đại thế kỷ 21 và sức mạnh tu hành cổ xưa ẩn giấu dưới lớp bê tông đô thị.",
        "read_mins": 7,
        "highlight": False
    }
]

def generate_cam_nang_hub_html(chapters_index, total_words):
    total_ch = len(chapters_index)
    latest_ch = chapters_index[-1] if chapters_index else None
    latest_num = latest_ch["chapter"] if latest_ch else total_ch

    cards_html = []
    for art in GLOBAL_CAM_NANG_ARTICLES:
        feat_cls = " is-featured" if art.get("highlight") else ""
        cards_html.append(f"""
          <a href="/{art['slug']}/" class="home-article-card{feat_cls}">
            <div class="article-card-header">
              <span class="article-card-badge">{art['badge']}</span>
              <span class="article-card-time">{art['read_mins']} phút đọc</span>
            </div>
            <h3 class="article-card-title">{art['title']}</h3>
            <p class="article-card-desc">{art['desc']}</p>
            <div class="article-card-footer">
              <span class="article-card-author">Tác giả: An Bình</span>
              <span class="article-card-action">Khám phá chuyên đề →</span>
            </div>
          </a>
        """)
    grid_html = "".join(cards_html)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>Cẩm Nang &amp; Hồ Sơ Chuyên Đề Tiểu Thuyết Phá Trời | An Bình</title>
  
  <meta name="title" content="Cẩm Nang &amp; Hồ Sơ Chuyên Đề Tiểu Thuyết Phá Trời | An Bình">
  <meta name="description" content="Khám phá toàn bộ hồ sơ chuyên đề Phá Trời: cẩm nang 12 cọc tiêu thủy môn bazan, lộ trình Thể Đạo phàm nhân, hồ sơ Lâm Tịch, Nguyễn Minh An và địa chất non sông.">
  <meta name="keywords" content="Phá Trời cẩm nang, 12 cọc tiêu thủy môn, lộ trình Thể Đạo, Lâm Tịch, Nguyễn Minh An, địa chất Việt Nam, An Bình">
  <meta name="author" content="An Bình">
  
  <link rel="canonical" href="{SITE_URL}/cam-nang/">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE_URL}/cam-nang/">
  <meta property="og:title" content="Cẩm Nang &amp; Hồ Sơ Chuyên Đề Tiểu Thuyết Phá Trời | An Bình">
  <meta property="og:description" content="Hồ sơ 12 cọc tiêu thủy môn, lộ trình Thể Đạo và địa tầng non sông Việt Nam trong Phá Trời.">
  <meta property="og:image" content="{SITE_URL}/assets/cover_vertical.jpg">

  <link rel="alternate" type="application/rss+xml" title="Phá Trời — RSS Feed" href="{SITE_URL}/feed.xml">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/assets/logo.webp" type="image/webp">
  <link rel="apple-touch-icon" href="/assets/logo.webp">
  <meta name="theme-color" content="#07090e">

  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_MEASUREMENT_ID}', {{
      page_title: 'Cẩm Nang &amp; Hồ Sơ Chuyên Đề | Phá Trời',
      page_path: '/cam-nang/'
    }});
  </script>

  <!-- Anti-FOUC Theme -->
  <script>
    (function() {{
      try {{
        var t = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
        document.documentElement.className = t;
      }} catch(e) {{}}
    }})();
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/assets/home.css?v={ASSET_VERSION}">
  <link rel="stylesheet" href="/assets/seo.css?v={ASSET_VERSION}">
</head>
<body class="theme-peaceful-dark is-hub">

  <div id="progressBarContainer"><div id="progressBar"></div></div>

  <!-- HEADER -->
  <header id="topHeader">
    <div class="header-left">
      <a href="/" class="btn-brand" title="Trang Chủ Phá Trời">
        <picture>
          <source srcset="/assets/logo.webp" type="image/webp">
          <img src="/assets/logo.jpg" class="nav-logo" alt="Phá Trời">
        </picture>
        <span class="nav-brand-text">PHÁ TRỜI</span>
        <span class="nav-live-badge"><span class="dot-live"></span> {total_ch} CHƯƠNG</span>
      </a>
    </div>

    <div class="header-center">
      <span class="header-title">Cẩm Nang &amp; Hồ Sơ</span>
      <p class="header-sub">{total_ch} chương • An Bình</p>
    </div>

    <div class="header-right">
      <a href="/" class="btn-top-nav" style="text-decoration:none; padding:6px 14px; font-size:12.5px;">
        <span>Trang Chủ</span>
      </a>
      <a href="/chuong-1/" class="btn-top-nav next" style="text-decoration:none; padding:6px 14px; font-size:12.5px;">
        <span>Đọc Chương 1 →</span>
      </a>
      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Nhanh Sáng / Tối (T)" aria-label="Chuyển giao diện sáng tối">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>
    </div>
  </header>

  <!-- HUB CONTENT -->
  <main class="home-container" style="max-width: 1060px; padding-top: 28px;">
    <!-- Breadcrumb -->
    <nav class="breadcrumb-nav" aria-label="Breadcrumb" style="margin-bottom: 24px; font-size: 13px; color: var(--text-muted); display: flex; align-items: center; gap: 8px;">
      <a href="/" style="color: inherit; text-decoration: none;">Trang Chủ</a>
      <span style="opacity: 0.4;">/</span>
      <span style="color: var(--gold-primary); font-weight: 600;">Cẩm Nang &amp; Hồ Sơ Chuyên Đề</span>
    </nav>

    <!-- Hub Header -->
    <header style="text-align: center; margin-bottom: 40px; padding: 20px 0 32px 0; border-bottom: 1px solid var(--border-color);">
      <div style="font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--gold-primary); margin-bottom: 10px;">
        ❖ BẢN NGUYÊN TƯ LIỆU &amp; KHẢO SÁT NON SÔNG
      </div>
      <h1 style="font-family: 'Lora', 'Georgia', serif; font-size: clamp(28px, 5vw, 42px); font-weight: 700; color: var(--gold-primary); margin-bottom: 14px; line-height: 1.25;">
        CẨM NANG &amp; HỒ SƠ CHUYÊN ĐỀ
      </h1>
      <p style="max-width: 720px; margin: 0 auto 20px auto; font-size: 14.5px; line-height: 1.7; color: var(--text-muted);">
        Tổng hợp toàn bộ hồ sơ địa tầng non sông, cọc tiêu trấn thủy viễn cổ, lộ trình tu luyện Thể Đạo phàm nhân và ghi chép nhân vật trong đại trường thiên <em>Phá Trời</em> do tác giả <strong>An Bình</strong> biên soạn.
      </p>
      <div style="display: inline-flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-muted); background: var(--card-bg); padding: 6px 18px; border-radius: 20px; border: 1px solid var(--border-color);">
        <span class="dot-live"></span>
        <span>8 Chuyên đề độc bản · Đồng bộ canon 100% · Cập nhật liên tục</span>
      </div>
    </header>

    <!-- Articles Grid -->
    <section>
      <div class="home-articles-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));">
        {grid_html}
      </div>
    </section>

    <!-- Call To Action Box -->
    <section class="cta-box" style="margin-top: 48px; text-align: center;">
      <h3 style="font-family:'Lora', serif; font-size:20px; color:var(--gold-primary); margin-bottom:8px;">Dấn Thân Vào Đại Phong Ấn Non Sông</h3>
      <p style="font-size:14px; color:var(--text-muted); margin-bottom:20px; max-width:620px; margin-left:auto; margin-right:auto;">
        Đồng hành cùng kỹ sư địa chất Nguyễn Minh An trên con đường Thể Đạo phàm nhân dãi dầu sương gió, phá vỡ xiềng xích càn khôn.
      </p>
      <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
        <a href="/chuong-1/" class="continue-btn" style="background:var(--gold-primary); color:#0b0f17; border-color:var(--gold-primary); font-weight:700;">Bắt Đầu Đọc — Chương 1 →</a>
        <a href="/chuong-{latest_num}/" class="continue-btn">Đọc Chương Mới Nhất ({latest_num}) →</a>
      </div>
    </section>

    <!-- Site Footer -->
    <footer class="site-footer">
      <div class="footer-top-grid">
        <div class="footer-col footer-col-brand">
          <div class="footer-brand-header">
            <picture>
              <source srcset="/assets/logo.webp" type="image/webp">
              <img src="/assets/logo.jpg" class="footer-logo" alt="Phá Trời">
            </picture>
            <div>
              <div class="footer-title">PHÁ TRỜI</div>
              <div class="footer-tagline">Đại Trường Thiên Thể Đạo Phàm Nhân</div>
            </div>
          </div>
          <p class="footer-summary">
            Tác phẩm văn học đô thị tu chân kết hợp khảo sát địa chất non sông Việt Nam của tác giả <strong>An Bình</strong>. Phàm nhân không hệ thống, lấy da thịt khổ tu phá vỡ xiềng xích càn khôn.
          </p>
          <div class="footer-live-status">
            <span class="dot-live"></span> Đang sáng tác đều đặn · {total_ch} chương ({total_words:,} từ)
          </div>
        </div>

        <div class="footer-col">
          <div class="footer-col-title">CẨM NANG &amp; HỒ SƠ</div>
          <ul class="footer-links">
            <li><a href="/cam-nang/" style="color:var(--gold-primary); font-weight:600;">✦ Xem Toàn Bộ Cẩm Nang (8) →</a></li>
            <li><a href="/thap-nhi-tieu/">✦ Cẩm Nang 12 Cọc Tiêu Thủy Môn</a></li>
            <li><a href="/canh-gioi-the-dao/">✦ Lộ Trình Tu Luyện Thể Đạo</a></li>
            <li><a href="/bach-y-than-nu-lam-tich/">✦ Hồ Sơ Lâm Tịch (Bạch Y Thần Nữ)</a></li>
            <li><a href="/nguyen-minh-an/">✦ Hồ Sơ Kỹ Sư Nguyễn Minh An</a></li>
            <li><a href="/the-dao/">✦ Bản Chất Thể Đạo Phàm Nhân</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <div class="footer-col-title">TỔNG QUAN TÁC PHẨM</div>
          <ul class="footer-links">
            <li><a href="/phat-troi-la-truyen-gi/">✦ Phá Trời Là Truyện Gì?</a></li>
            <li><a href="/truyen-tu-tien-viet-nam-sai-gon/">✦ Tiên Hiệp Bản Địa Sài Gòn</a></li>
            <li><a href="/do-thi-tu-chan-la-gi/">✦ Giải Mã Thể Loại Đô Thị Tu Chân</a></li>
            <li><a href="/chuong-1/">✦ Đọc Từ Đầu: Chương 1</a></li>
            <li><a href="/chuong-{latest_num}/">✦ Chương Mới Nhất ({latest_num})</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <div class="footer-col-title">TIỆN ÍCH &amp; KẾT NỐI</div>
          <ul class="footer-links">
            <li><a href="/feed.xml" target="_blank" rel="noopener">✦ Nguồn Tin RSS 2.0 Feed</a></li>
            <li><a href="/sitemap.xml" target="_blank" rel="noopener">✦ Sơ Đồ Trang (Sitemap)</a></li>
            <li><a href="/#sectionToc">✦ Mục Lục {total_ch} Chương</a></li>
            <li><span style="color:var(--text-muted); font-size:12px;">✦ Hỗ trợ PWA đọc Offline 24/7</span></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom-bar">
        <div class="footer-copy">
          Phát hành độc quyền tại <strong>phatroi.com</strong> • Bản quyền nội dung thuộc về tác giả <strong>An Bình</strong> © 2026. Mọi quyền được bảo lưu.
        </div>
        <div class="footer-badge-note">
          0% Linh Căn · 0% Hệ Thống · 100% Khổ Tu Phàm Nhân
        </div>
      </div>
    </footer>
  </main>

  <script>
    const btnTheme = document.getElementById('btnQuickTheme');
    if (btnTheme) {{
      btnTheme.onclick = () => {{
        const htmlEl = document.documentElement;
        const cur = htmlEl.className;
        const next = (cur === 'theme-peaceful-dark' || cur === 'theme-saigon-night' || !cur) ? 'theme-gentle-light' : 'theme-peaceful-dark';
        htmlEl.className = next;
        try {{ localStorage.setItem('pha_troi_theme', next); }} catch(e) {{}}
      }};
    }}
  </script>
</body>
</html>"""

def generate_home_html(chapters_index, total_words, codex_items=None):
    total_ch = len(chapters_index)
    shared_css = get_shared_css()
    codex_items = codex_items or get_codex_items()
    codex_json = json.dumps(codex_items, ensure_ascii=False)
    chapters_json = json.dumps(chapters_index, ensure_ascii=False)

    # Latest chapter info (Phase 4)
    latest_ch = chapters_index[-1] if chapters_index else None
    latest_num = latest_ch["chapter"] if latest_ch else total_ch
    latest_title = latest_ch["title"].replace(f"Chương {latest_num}:", "").strip() if latest_ch else ""
    latest_title = re.sub(r"^Chương\s+\d+:\s*", "", latest_title, flags=re.IGNORECASE)
    latest_words = latest_ch.get("word_count", 0) if latest_ch else 0
    latest_read_mins = max(1, round(latest_words / 300))
    latest_date = datetime.now().strftime("%d/%m/%Y")

    # Pre-rendered static chapter cards for crawler SEO discovery
    static_cards = []
    for ch in chapters_index:
        c_title = re.sub(r"^Chương\s+\d+:\s*", "", ch["title"], flags=re.IGNORECASE)
        loc_str = f"<span>· {ch['location'].split(',')[0]}</span>" if ch.get("location") else ""
        static_cards.append(f"""
          <a href="/chuong-{ch['chapter']}/" class="home-ch-card">
            <div class="home-ch-info">
              <div class="home-ch-meta-top">
                <span>HỒI {ch.get('arc', 1)} · CHƯƠNG {ch['chapter']}</span>
              </div>
              <div class="home-ch-title">{c_title}</div>
              <div class="home-ch-meta-bottom">
                <span>{ch['word_count']:,} từ</span>
                {loc_str}
              </div>
            </div>
            <div class="home-ch-arrow">→</div>
          </a>
        """)
    static_grid_html = "".join(static_cards)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="google-site-verification" content="495lr0EokjP3LLADeovb1t_ecOikpcbgyO_mW9m8e00">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>Phá Trời — Đại Trường Thiên Thể Đạo Phàm Nhân & Địa Chất Non Sông | An Bình</title>
  
  <meta name="title" content="Phá Trời — Đại Trường Thiên Thể Đạo Phàm Nhân & Địa Chất Non Sông | An Bình">
  <meta name="description" content="Đọc tiểu thuyết Phá Trời của tác giả An Bình. Hành trình Thể Đạo phàm nhân dãi dầu sương gió, khám phá bí ẩn địa chất non sông và phong ấn cổ xưa nghìn năm của đất Việt. Đọc miễn phí 24/7.">
  <meta name="keywords" content="Phá Trời, tiểu thuyết Thể Đạo, địa chất Việt Nam, Thể Đạo phàm nhân, Nguyễn Minh An, Lâm Tịch, tác giả An Bình, phatroi.com">
  <meta name="author" content="An Bình">
  
  <link rel="canonical" href="{SITE_URL}/">
  <meta property="og:type" content="book">
  <meta property="og:url" content="{SITE_URL}/">
  <meta property="og:title" content="Phá Trời — Đại Trường Thiên Thể Đạo Phàm Nhân & Địa Chất Non Sông | An Bình">
  <meta property="og:description" content="Đọc tiểu thuyết Phá Trời của tác giả An Bình. Hành trình Thể Đạo phàm nhân dãi dầu sương gió, khám phá bí ẩn địa chất non sông và phong ấn cổ xưa nghìn năm của đất Việt. Đọc miễn phí 24/7.">
  <meta property="og:image" content="{SITE_URL}/assets/cover_vertical.jpg">
  <meta property="og:image:width" content="682">
  <meta property="og:image:height" content="1024">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Phá Trời — Đại Trường Thiên Thể Đạo Phàm Nhân & Địa Chất Non Sông | An Bình">
  <meta name="twitter:description" content="Đọc tiểu thuyết Phá Trời của tác giả An Bình. Hành trình Thể Đạo phàm nhân dãi dầu sương gió, khám phá bí ẩn địa chất non sông và phong ấn cổ xưa nghìn năm của đất Việt. Đọc miễn phí 24/7.">
  <meta name="twitter:image" content="{SITE_URL}/assets/tieu-thuyet-pha-troi-do-thi-tu-chan-sai-gon-huyen-ao.jpg">

  <link rel="alternate" type="application/rss+xml" title="Phá Trời — RSS Feed" href="{SITE_URL}/feed.xml">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/assets/logo.webp" type="image/webp">
  <link rel="apple-touch-icon" href="/assets/logo.webp">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Phá Trời">
  <meta name="theme-color" content="#07090e">

  <!-- Google Analytics 4 (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_MEASUREMENT_ID}', {{
      page_title: 'Phá Trời — Tiểu Thuyết Đô Thị Tu Chân TP.HCM | An Bình',
      page_path: '/'
    }});
  </script>

  <!-- Anti-FOUC Early Theme Execution (Phase 1) -->
  <script>
    (function() {{
      try {{
        var t = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
        document.documentElement.className = t;
        var s = localStorage.getItem('pha_troi_font_size');
        if (s) document.documentElement.style.setProperty('--font-size', s + 'px');
        var w = localStorage.getItem('pha_troi_reader_width');
        if (w) document.documentElement.style.setProperty('--reader-max-width', w + 'px');
        var lh = localStorage.getItem('pha_troi_line_height');
        if (lh) document.documentElement.style.setProperty('--reader-line-height', lh);
        var f = localStorage.getItem('pha_troi_font_family');
        if (f === 'serif') {{
          document.documentElement.style.setProperty('--font-family', "'Lora', 'Georgia', serif");
        }}
      }} catch(e) {{}}
    }})();
  </script>

  <!-- Structured Data JSON-LD (WebSite, Book & Organization) (Phase 8) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebSite",
        "@id": "{SITE_URL}/#website",
        "url": "{SITE_URL}/",
        "name": "Phá Trời",
        "alternateName": ["Phá Trời Novel", "Pha Troi Novel"],
        "description": "Đại trường thiên tiểu thuyết Thể Đạo phàm nhân kết hợp địa chất non sông Việt Nam của tác giả An Bình.",
        "inLanguage": "vi",
        "publisher": {{
          "@id": "{SITE_URL}/#organization"
        }}
      }},
      {{
        "@type": "Organization",
        "@id": "{SITE_URL}/#organization",
        "name": "Phá Trời",
        "url": "{SITE_URL}/",
        "logo": {{
          "@type": "ImageObject",
          "url": "{SITE_URL}/assets/logo.webp"
        }}
      }},
      {{
        "@type": "Book",
        "@id": "{SITE_URL}/#book",
        "name": "Phá Trời",
        "author": {{
          "@type": "Person",
          "name": "An Bình",
          "url": "{SITE_URL}/"
        }},
        "publisher": {{
          "@id": "{SITE_URL}/#organization"
        }},
        "url": "{SITE_URL}/",
        "genre": ["Tiểu thuyết Thể Đạo", "Phiêu lưu mạo hiểm", "Địa chất", "Huyền huyễn"],
        "inLanguage": "vi",
        "numberOfPages": {total_ch},
        "description": "Hành trình Thể Đạo phàm nhân dãi dầu sương gió, khám phá bí ẩn địa chất non sông và phong ấn cổ xưa nghìn năm của đất Việt. Không hệ thống, khổ tu thực chiến."
      }}
    ]
  }}
  </script>

  <link rel="preload" as="image" href="/assets/tieu-thuyet-pha-troi-do-thi-tu-chan-sai-gon-huyen-ao.webp" type="image/webp">
  <link rel="preload" as="image" href="/assets/cover_vertical.webp" type="image/webp" media="(max-width: 768px)">
  <link rel="preload" as="image" href="/assets/logo.webp" type="image/webp">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/assets/home.css?v={ASSET_VERSION}">
</head>
<body class="theme-peaceful-dark is-home">

  <div id="progressBarContainer"><div id="progressBar"></div></div>

  <!-- HEADER -->
  <header id="topHeader">
    <div class="header-left">
      <a href="./" class="btn-brand" title="Trang Chủ Phá Trời">
        <picture>
          <source srcset="/assets/logo.webp" type="image/webp">
          <img src="/assets/logo.jpg" class="nav-logo" alt="Phá Trời">
        </picture>
        <span class="nav-brand-text">PHÁ TRỜI</span>
        <span class="nav-live-badge"><span class="dot-live"></span> {total_ch} CHƯƠNG</span>
      </a>
      <a href="/cam-nang/" class="nav-header-pill" title="Cẩm Nang & Chuyên Đề">
        <span>❖ CẨM NANG</span>
      </a>
    </div>

    <div class="header-center">
      <span class="header-title" id="headerTitle">Phá Trời</span>
      <p class="header-sub" id="headerSub">{total_ch} chương • An Bình</p>
    </div>

    <div class="header-right">
      <button class="btn-icon" id="btnMenu" title="Mục Lục Chương (M)" aria-label="Mục lục chương">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>

      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Nhanh Sáng / Tối (T)" aria-label="Chuyển giao diện sáng tối">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg id="iconSun" style="display:none;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button class="btn-icon" id="btnSettings" title="Cài Đặt Đọc Truyện" aria-label="Cài đặt giao diện đọc truyện">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
      </button>
    </div>
  </header>

  <!-- HOME VIEW -->
  <div id="homeView">
    <!-- HERO TITLEPAGE (LITERARY FRONTISPIECE & TITLE BLOCK) -->
    <section class="hero-titlepage">
      <div class="hero-titlepage-bg" aria-hidden="true"></div>
      <div class="hero-titlepage-overlay" aria-hidden="true"></div>
      <div class="titlepage-container">
        <!-- Book Cover Frontispiece -->
        <div class="titlepage-cover-frame">
          <picture>
            <source srcset="/assets/cover_vertical.webp" type="image/webp">
            <img src="/assets/cover_vertical.jpg" alt="Bìa tiểu thuyết Phá Trời" class="titlepage-cover-img" fetchpriority="high">
          </picture>
        </div>

        <!-- Typographic Title Block -->
        <div class="titlepage-meta-block">
          <div class="titlepage-imprint">ĐẠI TRƯỜNG THIÊN THỂ ĐẠO PHÀM NHÂN & ĐỊA CHẤT NON SÔNG</div>
          <h1 class="titlepage-title">PHÁ TRỜI</h1>
          <div class="titlepage-sub">ĐẠI TRƯỜNG THIÊN THỂ ĐẠO PHÀM NHÂN</div>
          <div class="titlepage-author">Tác giả: <em>An Bình</em></div>
          
          <div class="titlepage-ornament" aria-hidden="true"></div>

          <!-- Classical Epigraph / Đề từ -->
          <div class="titlepage-epigraph">
            <p class="epigraph-quote">“Sông Sài Gòn chảy qua ngàn năm dâu bể, dưới lớp phù sa ngầm là phong ấn đại địa hai triệu năm chưa từng thức giấc.”</p>
            <p class="epigraph-premise">Phàm nhân không linh căn, không hệ thống — lấy từng tấc da thịt Thể Đạo khổ tu phá vỡ vạn trùng xiềng xích càn khôn.</p>
          </div>

          <!-- Bibliographic Colophon Line -->
          <div class="titlepage-colophon">
            <span><strong>{total_ch}</strong> chương</span>
            <span class="col-sep">·</span>
            <span><strong>{total_words:,}</strong> từ</span>
            <span class="col-sep">·</span>
            <span>Quyển I–II</span>
            <span class="col-sep">·</span>
            <span class="col-status">Đang sáng tác đều đặn</span>
          </div>

          <!-- Dignified Action Buttons -->
          <div class="titlepage-actions">
            <a href="/chuong-1/" class="btn-titlepage-read" id="btnHeroReadPrimary">
              <span id="heroPrimaryText">Bắt Đầu Đọc — Chương 1</span>
              <span>→</span>
            </a>
            <a href="#sectionToc" class="btn-titlepage-toc" id="btnHeroTocScroll">
              <span>Mục Lục ({total_ch} Chương) ↓</span>
            </a>
            <a href="/cam-nang/" class="btn-titlepage-toc" style="border-color: rgba(229, 192, 123, 0.45); color: var(--gold-primary);">
              <span>Cẩm Nang & Hồ Sơ ❖</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Scroll Hint Indicator (Phase 13 Cinematic Scroll) -->
      <a href="#sectionContinue" class="hero-scroll-hint" id="heroScrollHint" aria-label="Cuộn xuống khám phá tác phẩm">
        <span class="scroll-hint-label">Khám phá</span>
        <svg class="scroll-hint-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </a>
    </section>

    <!-- HOME BODY CONTENT -->
    <div class="home-container">
      <!-- SECTION 2: WELCOME & RESUME READING -->
      <div id="sectionContinue">
        <div class="continue-card welcome-mode" id="continueReadingCard">
          <div class="continue-left">
            <picture>
              <source srcset="/assets/logo.webp" type="image/webp">
              <img src="/assets/logo.jpg" class="continue-thumb" alt="Phá Trời">
            </picture>
            <div class="continue-info">
              <div class="continue-pill" id="contPill">HÀNH TRÌNH BẮT ĐẦU</div>
              <div class="continue-chapter-name" id="contChName">Bạn chưa từng đọc Phá Trời? Bắt đầu từ Chương 1</div>
              <div class="continue-progress-meta" id="contChMeta">Dấn thân vào đại phong ấn sông ngầm Sài Gòn 2.5 triệu năm cùng Minh An</div>
            </div>
          </div>
          <a href="/chuong-1/" class="continue-btn" id="btnContinueJump">Bắt Đầu Đọc Chương 1 →</a>
        </div>

        <!-- SECTION 2B: LATEST CHAPTER HIGHLIGHT (PHASE 4) -->
        <div class="latest-chapter-banner" id="latestChapterBanner">
          <div style="display:flex; align-items:center; gap:14px; min-width:0; flex:1;">
            <span style="flex-shrink:0; font-size:11px; font-weight:600; letter-spacing:1px; padding:3px 8px; border:1px solid var(--border-color); border-radius:4px; color:var(--gold-primary);">MỚI XUẤT BẢN</span>
            <div style="min-width:0; flex:1;">
              <div style="font-size:11px; font-weight:600; color:var(--gold-primary); text-transform:uppercase; letter-spacing:1px;">Chương {latest_num} Vừa Cập Nhật</div>
              <div style="font-size:15px; font-weight:600; color:var(--text-color); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Chương {latest_num}: {latest_title}</div>
              <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">{latest_words:,} từ · ~{latest_read_mins} phút đọc · Cập nhật ngày {latest_date}</div>
            </div>
          </div>
          <a href="/chuong-{latest_num}/" class="continue-btn" style="flex-shrink:0;">Đọc Ngay →</a>
        </div>
      </div>

      <!-- SECTION 3: TABLE OF CONTENTS (PHASE 3) -->
      <div id="sectionToc">
        <div class="section-title-wrap">
          <h2 class="section-title">MỤC LỤC TÁC PHẨM ({total_ch} CHƯƠNG)</h2>
          <div class="home-search-box">
            <svg class="home-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" class="home-search-input" id="inputHomeSearch" placeholder="Tìm số chương, tiêu đề hoặc địa danh...">
          </div>
        </div>

        <!-- TOC Progress Summary (Phase 3) -->
        <div class="toc-progress-summary" id="homeTocProgressSummary" style="border-radius:6px; margin-bottom:16px; border:1px solid var(--border-color); padding:10px 14px; background:var(--card-bg);">
          <div class="toc-progress-text" style="font-size:12.5px;">
            <span>Tiến độ đọc toàn bộ:</span>
            <strong id="homeTocProgressText">Đã đọc 0 / {total_ch} chương (0%)</strong>
          </div>
          <div class="toc-progress-track" style="height:3px; border-radius:2px; background:var(--border-subtle); margin-top:6px;">
            <div class="toc-progress-fill" id="homeTocProgressFill" style="width: 0%; height:100%; background:var(--gold-primary); border-radius:2px;"></div>
          </div>
        </div>

        <div class="home-toc-filter-row">
          <div class="home-tabs">
            <button class="home-tab-btn active" data-home-filter="all">Tất Cả ({total_ch})</button>
            <button class="home-tab-btn" data-home-filter="arc1">Hồi 1 (1–46)</button>
            <button class="home-tab-btn" data-home-filter="arc2">Hồi 2 (47–{total_ch}+)</button>
          </div>
          <div style="font-size:12px; color:var(--text-muted);">
            Tổng cộng: <strong style="color:var(--text-color);">{total_words:,}</strong> từ bản thảo
          </div>
        </div>

        <div class="home-toc-grid" id="homeTocGrid">
          {static_grid_html}
        </div>
      </div>

      <!-- SECTION 4: ENCYCLOPEDIA / CODEX PREVIEW (PHASE 6) -->
      <div id="sectionCodexPreview">
        <div class="section-title-wrap">
          <div>
            <h2 class="section-title">CODEX PHÁ TRỜI — HỒ SƠ & BẢN THẢO THẾ GIỚI</h2>
            <div style="font-size:12.5px; color:var(--text-muted); margin-top:4px;">
              Hồ sơ nhân vật, cổ vật và đại địa phong ấn đô thị tu chân. Mở khóa theo tiến độ đọc.
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:10px;">
            <span class="codex-progress-pill" id="homeCodexProgressPill">Đã khám phá 0 / {len(codex_items)} mục</span>
            <button class="btn-hero-outline" id="btnViewAllCodex" style="padding:6px 14px; font-size:12px; border:1px solid var(--border-color);">Mở Bách Khoa →</button>
          </div>
        </div>
        <div class="home-codex-grid" id="homeCodexGrid">
          <!-- Populated dynamically based on reading progress -->
        </div>
      </div>

      <!-- SECTION 5: FOOTER (LITERARY EDITORIAL COLOPHON) -->
      <footer class="site-footer">
        <div class="footer-top-grid">
          <!-- Col 1: Brand & Premise -->
          <div class="footer-col footer-col-brand">
            <div class="footer-brand-header">
              <picture>
                <source srcset="/assets/logo.webp" type="image/webp">
                <img src="/assets/logo.jpg" class="footer-logo" alt="Phá Trời">
              </picture>
              <div>
                <div class="footer-title">PHÁ TRỜI</div>
                <div class="footer-tagline">Đại Trường Thiên Thể Đạo Phàm Nhân</div>
              </div>
            </div>
            <p class="footer-summary">
              Tác phẩm văn học đô thị tu chân kết hợp khảo sát địa chất non sông Việt Nam của tác giả <strong>An Bình</strong>. Phàm nhân không hệ thống, lấy da thịt khổ tu phá vỡ xiềng xích càn khôn.
            </p>
            <div class="footer-live-status">
              <span class="dot-live"></span> Đang sáng tác đều đặn · {total_ch} chương ({total_words:,} từ)
            </div>
          </div>

          <!-- Col 2: Cẩm Nang Địa Tầng & Lore -->
          <div class="footer-col">
            <div class="footer-col-title">CẨM NANG & HỒ SƠ</div>
            <ul class="footer-links">
              <li><a href="/cam-nang/" style="color:var(--gold-primary); font-weight:600;">✦ Xem Toàn Bộ Cẩm Nang (8) →</a></li>
              <li><a href="/thap-nhi-tieu/">✦ Cẩm Nang 12 Cọc Tiêu Thủy Môn</a></li>
              <li><a href="/canh-gioi-the-dao/">✦ Lộ Trình Tu Luyện Thể Đạo</a></li>
              <li><a href="/bach-y-than-nu-lam-tich/">✦ Hồ Sơ Lâm Tịch (Bạch Y Thần Nữ)</a></li>
              <li><a href="/nguyen-minh-an/">✦ Hồ Sơ Kỹ Sư Nguyễn Minh An</a></li>
              <li><a href="/the-dao/">✦ Bản Chất Thể Đạo Phàm Nhân</a></li>
            </ul>
          </div>

          <!-- Col 3: Khám Phá & Luận Đề -->
          <div class="footer-col">
            <div class="footer-col-title">TỔNG QUAN TÁC PHẨM</div>
            <ul class="footer-links">
              <li><a href="/phat-troi-la-truyen-gi/">✦ Phá Trời Là Truyện Gì?</a></li>
              <li><a href="/truyen-tu-tien-viet-nam-sai-gon/">✦ Tiên Hiệp Bản Địa Sài Gòn</a></li>
              <li><a href="/do-thi-tu-chan-la-gi/">✦ Giải Mã Thể Loại Đô Thị Tu Chân</a></li>
              <li><a href="/chuong-1/">✦ Đọc Từ Đầu: Chương 1</a></li>
              <li><a href="/chuong-{latest_num}/">✦ Chương Mới Nhất ({latest_num})</a></li>
            </ul>
          </div>

          <!-- Col 4: Công Cụ & Đọc Truyện -->
          <div class="footer-col">
            <div class="footer-col-title">TIỆN ÍCH & KẾT NỐI</div>
            <ul class="footer-links">
              <li><a href="/feed.xml" target="_blank" rel="noopener">✦ Nguồn Tin RSS 2.0 Feed</a></li>
              <li><a href="/sitemap.xml" target="_blank" rel="noopener">✦ Sơ Đồ Trang (Sitemap)</a></li>
              <li><a href="#sectionToc">✦ Mục Lục {total_ch} Chương</a></li>
              <li><span style="color:var(--text-muted); font-size:12px;">✦ Hỗ trợ PWA đọc Offline 24/7</span></li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom-bar">
          <div class="footer-copy">
            Phát hành độc quyền tại <strong>phatroi.com</strong> • Bản quyền nội dung thuộc về tác giả <strong>An Bình</strong> © 2026. Mọi quyền được bảo lưu.
          </div>
          <div class="footer-badge-note">
            0% Linh Căn · 0% Hệ Thống · 100% Khổ Tu Phàm Nhân
          </div>
        </div>
      </footer>
    </div>
  </div>

  <!-- MODAL OVERLAY -->
  <div class="modal-overlay" id="modalOverlay"></div>

  <!-- TOC DRAWER (PHASE 3) -->
  <aside class="drawer drawer-left" id="drawerToc" aria-label="Mục lục chương">
    <div class="drawer-header">
      <h2 class="drawer-title">MỤC LỤC TIỂU THUYẾT</h2>
      <button class="btn-icon" id="btnCloseToc" aria-label="Đóng mục lục">✕</button>
    </div>
    <div class="toc-progress-summary">
      <div class="toc-progress-text">
        <span>Tiến độ đọc:</span>
        <strong id="drawerTocProgressText">Đã đọc 0 / {total_ch} chương</strong>
      </div>
      <div class="toc-progress-track">
        <div class="toc-progress-fill" id="drawerTocProgressFill" style="width: 0%;"></div>
      </div>
    </div>
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" data-filter="all">Tất Cả (<span id="tocTotalCount">{total_ch}</span>)</button>
      <button class="drawer-tab-btn" data-filter="arc1">Hồi 1 (1–46)</button>
      <button class="drawer-tab-btn" data-filter="arc2">Hồi 2 (47–{total_ch}+)</button>
    </div>
    <div class="drawer-search">
      <input type="text" id="inputTocSearch" class="search-input" placeholder="Tìm số chương, tiêu đề hoặc địa danh...">
    </div>
    <div class="drawer-body" id="tocDrawerList"></div>
    <div class="drawer-footer-nav">
      <a href="/thap-nhi-tieu/" class="drawer-guide-link">✦ 12 Cọc Tiêu Thủy Môn</a>
      <a href="/canh-gioi-the-dao/" class="drawer-guide-link">✦ Lộ Trình Thể Đạo</a>
      <a href="/feed.xml" class="drawer-guide-link" target="_blank" rel="noopener">✦ Nguồn Tin RSS Feed</a>
    </div>
  </aside>

  <!-- CODEX DRAWER (PHASE 6) -->
  <aside class="drawer drawer-right" id="drawerCodex" aria-label="Codex Bách khoa thế giới">
    <div class="drawer-header">
      <div>
        <h2 class="drawer-title">CODEX PHÁ TRỜI</h2>
        <div style="font-size:11px; color:var(--text-muted); margin-top:2px;" id="drawerCodexProgressLabel">Đã khám phá 0 / {len(codex_items)} mục</div>
      </div>
      <button class="btn-icon" id="btnCloseCodex" aria-label="Đóng Codex">✕</button>
    </div>
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" id="tabCodexChar" data-codex="char">Nhân Vật</button>
      <button class="drawer-tab-btn" id="tabCodexItem" data-codex="item">Vũ Khí</button>
      <button class="drawer-tab-btn" id="tabCodexArtifact" data-codex="artifact">Cổ Vật</button>
      <button class="drawer-tab-btn" id="tabCodexSkill" data-codex="skill">Công Pháp</button>
      <button class="drawer-tab-btn" id="tabCodexLotus" data-codex="lotus">Thức Hải</button>
    </div>
    <div class="drawer-body" id="codexDrawerBody"></div>
  </aside>

  <!-- SETTINGS BOTTOM SHEET (PHASE 1 & PHASE 7) -->
  <aside class="sheet-bottom" id="settingsSheet" aria-label="Cài đặt đọc truyện">
    <div class="sheet-handle"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <h3 style="font-size:16px; font-weight:700; color:var(--gold-primary); margin:0;">TÙY CHỈNH ĐỌC TRUYỆN</h3>
      <button class="btn-icon" id="btnCloseSettings" style="width:32px; height:32px;" aria-label="Đóng cài đặt">✕</button>
    </div>
    <div class="setting-group">
      <div class="setting-label">Chủ Đề Giao Diện</div>
      <div class="theme-grid">
        <div class="theme-opt active" data-theme="theme-saigon-night" style="background:#0b0f17; color:#e2e8f0;">Đêm Sài Gòn</div>
        <div class="theme-opt" data-theme="theme-warm-dark" style="background:#121110; color:#e6dfd5;">Trầm Ấm</div>
        <div class="theme-opt" data-theme="theme-sepia" style="background:#f1e8d0; color:#3b2d1d;">Sepia Cổ Điển</div>
        <div class="theme-opt" data-theme="theme-gentle-light" style="background:#f7f5f0; color:#24221f;">Giấy Sáng</div>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Cỡ Chữ Đọc</div>
      <div class="stepper-ctrl">
        <button class="btn-step" id="btnFontDec" aria-label="Giảm kích thước chữ">A-</button>
        <span class="stepper-val" id="fontSizeVal">19px</span>
        <button class="btn-step" id="btnFontInc" aria-label="Tăng kích thước chữ">A+</button>
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
        <button class="btn-icon" id="btnSheetAudioToggle" style="background:var(--card-bg);" aria-label="Bật tắt âm thanh mưa">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
        </button>
        <input type="range" id="audioVolume" min="0" max="1" step="0.05" value="0.25" style="flex:1; margin:0 12px; accent-color:var(--accent-primary);" aria-label="Âm lượng mưa">
        <span id="audioVolVal" style="font-size:12px; color:var(--text-muted); width:32px;">25%</span>
      </div>
    </div>
    <div style="margin-top:16px;">
      <button id="btnCacheAll" style="width:100%; padding:13px; border-radius:12px; background:var(--accent-primary); color:#ffffff; font-weight:700; border:none; cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          <span id="cacheAllText">Tải Toàn Bộ {total_ch} Chương Để Đọc Offline</span>
        </div>
        <span id="cacheSubText" style="font-size:11px; font-weight:400; opacity:0.85;">{total_ch} chương · {total_words:,} từ • Có thể đọc khi không có mạng</span>
      </button>
    </div>
  </aside>

  <div id="liveToast"><span class="dot-live"></span><span id="toastMsg">Thông báo</span></div>

    <script>
    window.HOME_CONFIG = {{
      totalCh: {total_ch},
      totalWords: "{total_words:,}",
      chapters: {chapters_json}
    }};
  </script>
  <script defer src="/assets/home.js?v={ASSET_VERSION}"></script>
</body>
</html>"""

def generate_chapter_html(ch_info, chapters_index, total_words, codex_items=None, db_summaries=None):
    ch_num = ch_info["chapter"]
    codex_items = codex_items or get_codex_items()
    codex_json = json.dumps(codex_items, ensure_ascii=False)
    clean_title = ch_info["title"].replace(f"Chương {ch_num}:", "").strip()
    clean_title = re.sub(r"^Chương\s+\d+:\s*", "", clean_title, flags=re.IGNORECASE)
    vol = ch_info.get("volume", 1)
    arc = ch_info.get("arc", 1)
    words = ch_info.get("word_count", 2500)
    read_mins = max(1, round(words / 300))
    total_ch = len(chapters_index)
    shared_css = get_shared_css()

    # Tiêu chuẩn SEO Title (48-60 ký tự) & Description (145-158 ký tự) chuẩn Google SERP
    db_sum = db_summaries.get(ch_num, "") if db_summaries else ""
    title_seo = optimize_seo_title(ch_num, clean_title, ch_info.get("custom_title", ""))
    desc_seo = optimize_seo_description(
        ch_num=ch_num,
        clean_title=clean_title,
        custom_desc=ch_info.get("custom_desc", ""),
        db_summary=db_sum,
        plain_text=ch_info.get("plain_text", ch_info.get("excerpt", ""))
    )

    title_seo_json = json.dumps(title_seo, ensure_ascii=False)
    desc_seo_json = json.dumps(desc_seo, ensure_ascii=False)

    prev_url = f"/chuong-{ch_num - 1}/" if ch_num > 1 else "javascript:void(0)"
    prev_dis = "disabled" if ch_num <= 1 else ""
    next_url = f"/chuong-{ch_num + 1}/" if ch_num < total_ch else "javascript:void(0)"
    next_dis = "disabled" if ch_num >= total_ch else ""

    next_ch_info = chapters_index[ch_num] if ch_num < total_ch else None
    if next_ch_info:
        next_ch_title = next_ch_info["title"].replace(f"Chương {ch_num + 1}:", "").strip()
        next_ch_title = re.sub(r"^Chương\s+\d+:\s*", "", next_ch_title, flags=re.IGNORECASE)
        next_vol = next_ch_info.get("volume", 1)
        next_arc = next_ch_info.get("arc", 1)
        next_words = next_ch_info.get("word_count", 2500)
        next_read_mins = max(1, round(next_words / 300))
        chapter_end_html = f"""
      <section class="chapter-end-colophon" id="chapterEndColophon">
        <div class="chapter-end-dinkus">· ✦ ·</div>
        <div class="chapter-end-meta">
          <div class="chapter-end-status">KẾT THÚC CHƯƠNG {ch_num}</div>
          <h3 class="chapter-end-next-title">Chương {ch_num + 1}: {next_ch_title}</h3>
          <p class="chapter-end-next-meta">Quyển {next_vol} · Hồi {next_arc} · {next_words:,} từ · Khoảng {next_read_mins} phút đọc</p>
        </div>
        <nav class="chapter-end-nav" aria-label="Điều hướng chương">
          <a href="{prev_url}" class="btn-chapter-nav prev {prev_dis}" id="footerPrevBtn" aria-label="Chương trước">
            <span>← Chương Trước</span>
          </a>
          <a href="/" class="btn-chapter-nav toc" id="btnFooterToc" aria-label="Mục lục tác phẩm">
            <span>Mục Lục ({total_ch})</span>
          </a>
          <a href="/chuong-{ch_num + 1}/" class="btn-chapter-nav next" id="footerNextBtn" aria-label="Đọc tiếp chương {ch_num + 1}">
            <span>Chương {ch_num + 1} →</span>
          </a>
        </nav>
      </section>
        """
    else:
        chapter_end_html = f"""
      <section class="chapter-end-colophon" id="chapterEndColophon">
        <div class="chapter-end-dinkus">· ✦ ·</div>
        <div class="chapter-end-meta">
          <div class="chapter-end-status">KẾT THÚC CHƯƠNG {ch_num} · CHƯƠNG MỚI NHẤT</div>
          <h3 class="chapter-end-next-title">Bạn đã đọc đến chương mới nhất!</h3>
          <p class="chapter-end-next-meta">Tác giả An Bình đang tiếp tục sáng tác. Bản thảo sẽ được tự động cập nhật ngay khi hoàn thành.</p>
        </div>
        <nav class="chapter-end-nav" aria-label="Điều hướng chương">
          <a href="{prev_url}" class="btn-chapter-nav prev {prev_dis}" id="footerPrevBtn" aria-label="Chương trước">
            <span>← Chương Trước</span>
          </a>
          <a href="/" class="btn-chapter-nav toc" id="btnFooterToc" aria-label="Mục lục tác phẩm">
            <span>Mục Lục ({total_ch})</span>
          </a>
          <button type="button" class="btn-chapter-nav next" id="btnCardCodex" aria-label="Khám phá Codex">
            <span>Khám Phá Codex</span>
          </button>
        </nav>
      </section>
        """

    toc_items_html = []
    for c in chapters_index:
        active_cls = "active" if c["chapter"] == ch_num else ""
        c_title = c["title"].replace(f"Chương {c['chapter']}:", "").strip()
        c_title = re.sub(r"^Chương\s+\d+:\s*", "", c_title, flags=re.IGNORECASE)
        toc_items_html.append(f"""
          <a href="/chuong-{c['chapter']}/" class="toc-item {active_cls}">
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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="google-site-verification" content="495lr0EokjP3LLADeovb1t_ecOikpcbgyO_mW9m8e00">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>{title_seo}</title>
  
  <meta name="title" content="{title_seo}">
  <meta name="description" content="{desc_seo}">
  <meta name="keywords" content="Phá Trời Chương {ch_num}, {clean_title}, đọc Phá Trời, tiểu thuyết Thể Đạo, Thể Đạo phàm nhân, Nguyễn Minh An, tác giả An Bình, phatroi.com">
  <meta name="author" content="An Bình">
  
  <link rel="canonical" href="{SITE_URL}/chuong-{ch_num}/">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE_URL}/chuong-{ch_num}/">
  <meta property="og:title" content="{title_seo}">
  <meta property="og:description" content="{desc_seo}">
  <meta property="og:image" content="{SITE_URL}/assets/cover_vertical.jpg">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title_seo}">
  <meta name="twitter:description" content="{desc_seo}">
  <meta name="twitter:image" content="{SITE_URL}/assets/hero_horizontal.jpg">

  <link rel="alternate" type="application/rss+xml" title="Phá Trời — RSS Feed" href="{SITE_URL}/feed.xml">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/assets/logo.webp" type="image/webp">
  <link rel="apple-touch-icon" href="/assets/logo.webp">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Phá Trời">
  <meta name="theme-color" content="#07090e">

  <!-- Google Analytics 4 (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_MEASUREMENT_ID}', {{
      page_title: {title_seo_json},
      page_path: '/chuong-{ch_num}/'
    }});
    gtag('event', 'view_chapter', {{
      chapter_number: {ch_num},
      chapter_title: {json.dumps(clean_title)},
      words: {words}
    }});
    if ({ch_num} === 1) {{
      gtag('event', 'start_chapter_1');
    }}
    if ({ch_num} === 3) {{
      gtag('event', 'reach_chapter_3');
    }}
  </script>

  <!-- Anti-FOUC Early Theme Execution (Phase 1) -->
  <script>
    (function() {{
      try {{
        var t = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
        document.documentElement.className = t;
        var s = localStorage.getItem('pha_troi_font_size');
        if (s) document.documentElement.style.setProperty('--font-size', s + 'px');
        var w = localStorage.getItem('pha_troi_reader_width');
        if (w) document.documentElement.style.setProperty('--reader-max-width', w + 'px');
        var lh = localStorage.getItem('pha_troi_line_height');
        if (lh) document.documentElement.style.setProperty('--reader-line-height', lh);
        var f = localStorage.getItem('pha_troi_font_family');
        if (f === 'serif') {{
          document.documentElement.style.setProperty('--font-family', "'Lora', 'Georgia', serif");
        }}
      }} catch(e) {{}}
    }})();
  </script>

  <!-- Structured Data JSON-LD (Article, Breadcrumbs & WebSite Graph) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebSite",
        "@id": "{SITE_URL}/#website",
        "url": "{SITE_URL}/",
        "name": "Phá Trời",
        "description": "Đại trường thiên tiểu thuyết Thể Đạo phàm nhân & Địa chất non sông."
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{SITE_URL}/chuong-{ch_num}/#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Trang Chủ",
            "item": "{SITE_URL}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Quyển {vol} · Hồi {arc}",
            "item": "{SITE_URL}/#hoi-{arc}"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "Chương {ch_num}: {clean_title}",
            "item": "{SITE_URL}/chuong-{ch_num}/"
          }}
        ]
      }},
      {{
        "@type": "Article",
        "@id": "{SITE_URL}/chuong-{ch_num}/#article",
        "isPartOf": {{
          "@type": "Book",
          "@id": "{SITE_URL}/#book",
          "name": "Phá Trời",
          "url": "{SITE_URL}/"
        }},
        "headline": {title_seo_json},
        "name": {title_seo_json},
        "description": {desc_seo_json},
        "url": "{SITE_URL}/chuong-{ch_num}/",
        "mainEntityOfPage": "{SITE_URL}/chuong-{ch_num}/",
        "inLanguage": "vi-VN",
        "wordCount": {words},
        "author": {{
          "@type": "Person",
          "name": "An Bình",
          "url": "{SITE_URL}/"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "Phá Trời",
          "url": "{SITE_URL}/",
          "logo": {{
            "@type": "ImageObject",
            "url": "{SITE_URL}/assets/logo.webp"
          }}
        }},
        "image": {{
          "@type": "ImageObject",
          "url": "{SITE_URL}/assets/cover_vertical.jpg"
        }}
      }}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/assets/reader.css?v={ASSET_VERSION}">
</head>
<body class="theme-peaceful-dark is-chapter">

  <div id="progressBarContainer"><div id="progressBar"></div></div>

  <!-- HEADER (PHASE 1 & PHASE 5) -->
  <header id="topHeader">
    <div class="header-left">
      <a href="/" class="btn-brand" title="Về Trang Chủ Phá Trời (H)">
        <picture>
          <source srcset="/assets/logo.webp" type="image/webp">
          <img src="/assets/logo.jpg" class="nav-logo" alt="Phá Trời">
        </picture>
        <span class="nav-brand-text">PHÁ TRỜI</span>
        <span class="nav-live-badge"><span class="dot-live"></span> {total_ch} CHƯƠNG</span>
      </a>
    </div>

    <div class="header-center">
      <span class="header-title">Chương {ch_num}: {clean_title}</span>
      <p class="header-sub">Quyển {vol} · Hồi {arc} · {words:,} từ <span class="reader-progress-badge" id="readProgressPct">0%</span></p>
    </div>

    <div class="header-right">
      <button class="btn-icon" id="btnShare" title="Chia Sẻ Chương Này (S)" aria-label="Chia sẻ chương này">
        <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
      </button>

      <a href="/" class="btn-nav-home-pill" title="Trở về Trang Chủ">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>
        <span>Trang Chủ</span>
      </a>

      <button class="btn-icon" id="btnMenu" title="Mục Lục Chương (M)" aria-label="Mục lục chương">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      
      <button class="btn-icon header-desktop-only" id="btnCodex" title="Codex Phá Trời — Bách Khoa Thế Giới (C)" aria-label="Codex Bách khoa">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
      </button>

      <button class="btn-icon header-desktop-only" id="btnAmbient" title="Âm thanh Mưa Đêm Sài Gòn (Thư giãn)" aria-label="Bật tắt âm thanh mưa">
        <svg id="iconAudioOff" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"></path><path d="M16 14v6"></path><path d="M8 14v6"></path><path d="M12 16v6"></path></svg>
        <svg id="iconAudioOn" style="display:none; color:var(--accent-primary);" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 5L6 9H2v6h4l5 4V5z"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
      </button>

      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Nhanh Sáng / Tối (T)" aria-label="Chuyển giao diện sáng tối">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg id="iconSun" style="display:none;" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>

      <button class="btn-icon header-desktop-only" id="btnAudioReader" title="Nghe Đọc Tự Nhiên (P)" aria-label="Bật nghe đọc">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
      </button>

      <button class="btn-icon header-desktop-only" id="btnQuoteStudio" title="Tạo Thẻ Ảnh Trích Dẫn (Q)" aria-label="Tạo thẻ ảnh trích dẫn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
      </button>

      <button class="btn-icon" id="btnSettings" title="Cài Đặt Đọc Truyện" aria-label="Cài đặt giao diện đọc">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>
      </button>
    </div>
  </header>

  <!-- CHAPTER READER CONTENT -->
  <div class="app-layout">
    <!-- Desktop Persistent Sidebar -->
    <aside class="desktop-toc-sidebar" aria-label="Danh mục chương máy tính">
      <div style="font-size:13px; font-weight:700; color:var(--gold-primary); margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
        <span>DANH MỤC CHƯƠNG</span>
        <span>{total_ch} chương</span>
      </div>
      <div>{toc_list_rendered}</div>
    </aside>

    <!-- Main Reader Content -->
    <main class="main-reader">
      <div class="btn-back-home-wrap">
        <a href="/" class="btn-back-home" title="Trở về Trang Chủ Phá Trời">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
          <span>Trang Chủ</span>
        </a>

        <!-- Top Chapter Navigation -->
        <div class="top-chapter-nav" aria-label="Điều hướng chương đầu trang">
          <a href="{prev_url}" class="btn-top-nav prev {prev_dis}" id="topPrevBtn" aria-label="Chương trước" title="Chương trước">
            <span>← Trước</span>
          </a>
          <span class="top-nav-progress">Chương {ch_num}/{total_ch}</span>
          <a href="{next_url}" class="btn-top-nav next {next_dis}" id="topNextBtn" aria-label="Chương tiếp theo" title="Chương tiếp theo">
            <span>Sau →</span>
          </a>
        </div>
      </div>

      <section class="chapter-hero">
        <div class="chapter-vol-arc">❖ QUYỂN {vol} · HỒI {arc} ❖</div>
        <h1 class="chapter-main-title">Chương {ch_num}: {clean_title}</h1>
        <div class="chapter-hero-meta">
          <span>{words:,} từ</span>
          <span class="meta-sep">·</span>
          <span>Khoảng {read_mins} phút đọc</span>
          {f'<span class="meta-sep">·</span><span>{ch_info["location"]}</span>' if ch_info.get("location") else ""}
        </div>
      </section>

      <!-- Editorial Action Row (Audio & Quote) -->
      <div class="reader-editorial-bar" id="readerEditorialBar">
        <button type="button" id="btnQuickPlayAudio" class="editorial-btn" title="Nghe đọc tự nhiên toàn bộ chương này">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
          <span>Nghe Đọc Tự Nhiên</span>
        </button>
        <span class="editorial-divider">·</span>
        <button type="button" id="btnQuickQuoteStudio" class="editorial-btn" title="Tạo thẻ ảnh trích dẫn chia sẻ">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
          <span>Tạo Thẻ Trích Dẫn</span>
        </button>
      </div>

      <article class="novel-body" id="novelContent">
        {ch_info["html"]}
      </article>

      <!-- Chapter Related Lore CTA Block -->
      <section class="chapter-lore-cta">
        <div class="chapter-lore-cta-title">
          <span>❖ CẨM NANG & HỒ SƠ CHUYÊN ĐỀ</span>
        </div>
        <p class="chapter-lore-cta-desc">
          Khám phá hệ thống cọc tiêu trấn thủy bazan, lộ trình Thể Đạo và ghi chép nhân vật trong Phá Trời:
        </p>
        <div class="chapter-lore-grid">
          <a href="/thap-nhi-tieu/" class="lore-cta-link">
            <div class="lore-cta-link-title">✦ 12 Cọc Tiêu Thủy Môn</div>
            <div class="lore-cta-link-desc">Hệ thống 12 cọc tiêu bazan viễn cổ từ Sài Gòn tới Tây Nguyên và chuỗi di vật 1996.</div>
          </a>
          <a href="/canh-gioi-the-dao/" class="lore-cta-link">
            <div class="lore-cta-link-title">✦ Lộ Trình Thể Đạo</div>
            <div class="lore-cta-link-desc">Bốn cảnh giới nhục thân: Chu Thiên, Đoán Cốt, Hoán Huyết và Thần Tạng.</div>
          </a>
          <a href="/bach-y-than-nu-lam-tich/" class="lore-cta-link">
            <div class="lore-cta-link-title">✦ Kiếm Tiên Lâm Tịch</div>
            <div class="lore-cta-link-desc">Bạch Y Thần Nữ ngự trên đài sen Lục Diệp Thanh Liên cùng Băng Phách Kiếm Ý.</div>
          </a>
          <a href="/nguyen-minh-an/" class="lore-cta-link">
            <div class="lore-cta-link-title">✦ Kỹ Sư Nguyễn Minh An</div>
            <div class="lore-cta-link-desc">Phàm nhân 25 tuổi, chiếc búa địa chất và trách nhiệm đọc dấu vết trong lòng đá.</div>
          </a>
        </div>
        <div class="chapter-lore-footer">
          <span>Tác giả An Bình · Phát hành độc quyền tại phatroi.com</span>
          <button onclick="shareChapter()" style="background:transparent; border:1px solid var(--border-color); color:var(--gold-primary); padding:5px 12px; border-radius:4px; font-size:12px; cursor:pointer; font-weight:600;">
            🔗 Chia Sẻ Chương {ch_num}
          </button>
        </div>
      </section>

      <!-- End of Chapter Colophon & Navigation (Phase 3) -->
      {chapter_end_html}
    </main>
  </div>

  <!-- Mobile Bottom Floating Nav (Phase 1, 5, 9) -->
  <nav class="bottom-bar" aria-label="Thanh điều hướng dưới mobile">
    <a href="/" class="btn-bottom-item">
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

  <!-- TOC DRAWER (PHASE 3) -->
  <aside class="drawer drawer-left" id="drawerToc" aria-label="Mục lục chương">
    <div class="drawer-header">
      <h2 class="drawer-title">MỤC LỤC TIỂU THUYẾT</h2>
      <button class="btn-icon" id="btnCloseToc" aria-label="Đóng mục lục">✕</button>
    </div>
    <div class="drawer-search">
      <input type="text" id="inputTocSearch" class="search-input" placeholder="Tìm số chương hoặc từ khóa...">
    </div>
    <div class="drawer-body" id="tocDrawerList"></div>
  </aside>

  <!-- CODEX DRAWER (PHASE 6) -->
  <aside class="drawer drawer-right" id="drawerCodex" aria-label="Codex Bách khoa thế giới">
    <div class="drawer-header">
      <h2 class="drawer-title">CODEX PHÁ TRỜI</h2>
      <button class="btn-icon" id="btnCloseCodex" aria-label="Đóng Codex">✕</button>
    </div>
    <div class="drawer-tabs">
      <button class="drawer-tab-btn active" id="tabCodexChar" data-codex="char">Nhân Vật</button>
      <button class="drawer-tab-btn" id="tabCodexItem" data-codex="item">Vũ Khí</button>
      <button class="drawer-tab-btn" id="tabCodexArtifact" data-codex="artifact">Cổ Vật</button>
      <button class="drawer-tab-btn" id="tabCodexSkill" data-codex="skill">Công Pháp</button>
      <button class="drawer-tab-btn" id="tabCodexLotus" data-codex="lotus">Thức Hải</button>
    </div>
    <div class="drawer-body" id="codexDrawerBody"></div>
  </aside>

  <!-- SETTINGS BOTTOM SHEET -->
  <aside class="sheet-bottom" id="settingsSheet" aria-label="Cài đặt đọc truyện">
    <div class="sheet-handle"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
      <h3 style="font-size:16px; font-weight:700; color:var(--gold-primary); margin:0;">TÙY CHỈNH ĐỌC TRUYỆN</h3>
      <button class="btn-icon" id="btnCloseSettings" style="width:32px; height:32px;" aria-label="Đóng cài đặt">✕</button>
    </div>
    <div class="setting-group">
      <div class="setting-label">Chủ Đề Giao Diện</div>
      <div class="theme-grid">
        <div class="theme-opt active" data-theme="theme-saigon-night" style="background:#0b0f17; color:#e2e8f0;">Đêm Sài Gòn</div>
        <div class="theme-opt" data-theme="theme-warm-dark" style="background:#121110; color:#e6dfd5;">Trầm Ấm</div>
        <div class="theme-opt" data-theme="theme-sepia" style="background:#f1e8d0; color:#3b2d1d;">Sepia Cổ Điển</div>
        <div class="theme-opt" data-theme="theme-gentle-light" style="background:#f7f5f0; color:#24221f;">Giấy Sáng</div>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">Cỡ Chữ Đọc</div>
      <div class="stepper-ctrl">
        <button class="btn-step" id="btnFontDec" aria-label="Giảm kích thước chữ">A-</button>
        <span class="stepper-val" id="fontSizeVal">19px</span>
        <button class="btn-step" id="btnFontInc" aria-label="Tăng kích thước chữ">A+</button>
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
        <button class="btn-icon" id="btnSheetAudioToggle" style="background:var(--card-bg);" aria-label="Bật tắt âm thanh mưa">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
        </button>
        <input type="range" id="audioVolume" min="0" max="1" step="0.05" value="0.25" style="flex:1; margin:0 12px; accent-color:var(--accent-primary);" aria-label="Âm lượng mưa">
        <span id="audioVolVal" style="font-size:12px; color:var(--text-muted); width:32px;">25%</span>
      </div>
    </div>
  </aside>

  <div id="liveToast"><span class="dot-live"></span><span id="toastMsg">Thông báo</span></div>

    <script>
    window.CHAPTER_CONFIG = {{
      chNum: {ch_num},
      cleanTitle: {json.dumps(clean_title)},
      totalCh: {total_ch},
      siteUrl: "{SITE_URL}"
    }};
  </script>
  <script defer src="/assets/reader.js?v={ASSET_VERSION}"></script>
</body>
</html>"""

def generate_sw(total_ch):
    sw_ver = f"pha-troi-v{total_ch}-{int(time.time())}"
    return f"""// Service Worker {sw_ver} cho Web Reader Phá Trời
const CACHE_NAME = '{sw_ver}';
const ASSETS_TO_CACHE = [
  '/',
  '/manifest.json',
  '/icon.svg',
  '/cover.svg',
  '/data/chapters.json',
  '/data/codex.json',
  '/assets/reader.css',
  '/assets/reader.js',
  '/assets/home.css',
  '/assets/home.js',
  '/assets/seo.css',
  '/assets/logo.webp',
  '/assets/cover_vertical.webp',
  '/assets/hero_horizontal.webp',
  '/assets/tieu-thuyet-pha-troi-do-thi-tu-chan-sai-gon-huyen-ao.webp'
];

self.addEventListener('install', (e) => {{
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
}});

self.addEventListener('activate', (e) => {{
  e.waitUntil(
    caches.keys().then((keys) => {{
      return Promise.all(
        keys.map((key) => {{
          if (key !== CACHE_NAME) return caches.delete(key);
        }})
      );
    }})
  );
  self.clients.claim();
}});

self.addEventListener('fetch', (e) => {{
  const url = new URL(e.request.url);

  // 1. Đối với HTML pages (Navigate / Document) và data/chapters.json:
  // CHIẾN LƯỢC: NETWORK-FIRST (Luôn lấy mới nhất trên mạng, chỉ dùng cache khi offline)
  if (e.request.mode === 'navigate' || e.request.destination === 'document' || url.pathname.includes('/data/')) {{
    e.respondWith(
      fetch(e.request)
        .then((networkResponse) => {{
          if (networkResponse && networkResponse.status === 200) {{
            const resClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
          }}
          return networkResponse;
        }})
        .catch(() => {{
          return caches.match(e.request).then((cached) => cached || caches.match('/'));
        }})
    );
    return;
  }}

  // 2. Đối với hình ảnh và static assets: Stale-While-Revalidate
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {{
      const fetchPromise = fetch(e.request).then((networkResponse) => {{
        if (networkResponse && networkResponse.status === 200) {{
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
        }}
        return networkResponse;
      }}).catch(() => null);

      return cachedResponse || fetchPromise;
    }})
  );
}});
"""

def build():
    print(f"[*] Bat dau bien dich Web App tinh Pha Troi v2.5 (12 Phase Upgrade) tai: {DIST_DIR}")
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

    now_iso = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S+07:00")
    index_data = {
        "title": "Phá Trời",
        "author": "An Bình",
        "total": len(chapters_index),
        "total_words": total_words,
        "updated_at": now_iso,
        "chapters": chapters_index
    }
    with open(os.path.join(data_dir, "chapters.json"), "w", encoding="utf-8") as out:
        json.dump(index_data, out, ensure_ascii=False, indent=1)

    # 1b. Export Codex JSON for client/offline access
    codex_items = get_codex_items()
    with open(os.path.join(data_dir, "codex.json"), "w", encoding="utf-8") as out:
        json.dump(codex_items, out, ensure_ascii=False, indent=1)
    print(f"  [+] Exported {len(codex_items)} codex items to dist/data/codex.json")

    # 2. Copy static assets to dist/assets
    src_assets = os.path.join(STATIC_SRC_DIR, "assets")
    dst_assets = os.path.join(DIST_DIR, "assets")
    if os.path.exists(src_assets):
        if os.path.exists(dst_assets):
            shutil.rmtree(dst_assets)
        shutil.copytree(src_assets, dst_assets)
        print(f"  [+] Copied assets to {dst_assets}")

    # 3. Generate root index.html (Homepage)
    home_html = generate_home_html(chapters_index, total_words, codex_items)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as out:
        out.write(home_html)
    print("  [+] Generated dist/index.html")

    # 4. Generate Clean Slug Directory for each chapter: dist/chuong-X/index.html
    db_summaries = get_db_chapter_summaries()
    for ch_info in parsed_chapters:
        ch_slug_dir = os.path.join(DIST_DIR, f"chuong-{ch_info['chapter']}")
        os.makedirs(ch_slug_dir, exist_ok=True)
        ch_html = generate_chapter_html(ch_info, chapters_index, total_words, codex_items, db_summaries)
        with open(os.path.join(ch_slug_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(ch_html)
    print(f"  [+] Generated {len(parsed_chapters)} Clean Slug chapter pages: dist/chuong-X/index.html")

    # 4b. Generate SEO & Lore Satellite Pages
    shared_css = get_shared_css()
    for article in SEO_PAGES:
        art_slug_dir = os.path.join(DIST_DIR, article["slug"])
        os.makedirs(art_slug_dir, exist_ok=True)
        art_html = render_seo_page_html(article, shared_css, SITE_URL, GA_MEASUREMENT_ID, len(chapters_index))
        with open(os.path.join(art_slug_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(art_html)
    print(f"  [+] Generated {len(SEO_PAGES)} SEO & Lore satellite pages: dist/<slug>/index.html")

    # 4c. Generate /cam-nang/ Dedicated Hub Page (Clean Editorial Slug)
    cam_nang_dir = os.path.join(DIST_DIR, "cam-nang")
    os.makedirs(cam_nang_dir, exist_ok=True)
    with open(os.path.join(cam_nang_dir, "index.html"), "w", encoding="utf-8") as out:
        out.write(generate_cam_nang_hub_html(chapters_index, total_words))
    print("  [+] Generated dist/cam-nang/index.html (Editorial Guides Hub)")

    # 5. Generate 404.html for smart redirection
    with open(os.path.join(DIST_DIR, "404.html"), "w", encoding="utf-8") as out:
        out.write(generate_404_html())
    print("  [+] Generated dist/404.html")

    # 5b. Generate sitemap.xml, feed.xml & robots.txt (SEO Architecture Phase 8)
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as out:
        out.write(generate_sitemap_xml(chapters_index))
    with open(os.path.join(DIST_DIR, "feed.xml"), "w", encoding="utf-8") as out:
        out.write(generate_feed_xml(chapters_index, db_summaries))
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as out:
        out.write(generate_robots_txt())
    print("  [+] Generated dist/sitemap.xml, dist/feed.xml and dist/robots.txt")

    # 5c. Generate CNAME for custom domain
    with open(os.path.join(DIST_DIR, "CNAME"), "w", encoding="utf-8") as out:
        out.write("phatroi.com\n")
    print("  [+] Generated dist/CNAME (phatroi.com)")

    # 5d. Google Search Console HTML verification file
    gsc_file = "google54897adf661cd4b2.html"
    with open(os.path.join(DIST_DIR, gsc_file), "w", encoding="utf-8") as out:
        out.write(f"google-site-verification: {gsc_file}\n")
    print(f"  [+] Generated dist/{gsc_file}")

    # 5e. Bypass Jekyll for instant deployment on GitHub Pages
    with open(os.path.join(DIST_DIR, ".nojekyll"), "w", encoding="utf-8") as out:
        out.write("")
    print("  [+] Generated dist/.nojekyll (Bypass Jekyll)")

    # 6. Generate sw.js
    with open(os.path.join(DIST_DIR, "sw.js"), "w", encoding="utf-8") as out:
        out.write(generate_sw(len(chapters_index)))

    # 7. Generate cover.svg
    cover_svg_content = generate_cover_svg(len(chapters_index))
    with open(os.path.join(DIST_DIR, "cover.svg"), "w", encoding="utf-8") as out:
        out.write(cover_svg_content)

    # 8. Generate manifest.json
    manifest_data = {
        "name": "Phá Trời — Tiểu Thuyết Đô Thị Tu Chân",
        "short_name": "Phá Trời",
        "description": "Ứng dụng đọc tiểu thuyết trọn bộ thời gian thực cho Phá Trời",
        "start_url": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#07090e",
        "theme_color": "#07090e",
        "icons": [
            {
                "src": "/assets/logo.webp",
                "sizes": "512x512",
                "type": "image/webp",
                "purpose": "any maskable"
            },
            {
                "src": "/icon.svg",
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
