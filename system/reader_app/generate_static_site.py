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
DIST_DIR = os.path.join(BASE_DIR, "system", "reader_app", "dist")

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

def generate_html(chapters_index, total_words):
    return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Phá Trời — Đọc Truyện</title>
  <link rel="manifest" href="./manifest.json">
  <link rel="icon" href="./icon.svg" type="image/svg+xml">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Phá Trời">
  <meta name="theme-color" content="#0d0e12">
  <style>
    :root {
      --bg-color: #0d0e12;
      --text-color: #d1d5db;
      --header-bg: rgba(13, 14, 18, 0.92);
      --card-bg: #16181f;
      --border-color: #242735;
      --accent-color: #e53e3e;
      --gold-color: #d4af37;
      --font-family: -apple-system, BlinkMacSystemFont, "Bookerly", "Georgia", "Palatino", serif;
      --font-size: 19px;
      --line-height: 1.82;
      --max-width: 680px;
    }

    body.theme-oled {
      --bg-color: #000000;
      --text-color: #c9cdd4;
      --header-bg: rgba(0, 0, 0, 0.96);
      --card-bg: #0d0e11;
      --border-color: #1a1c24;
      --accent-color: #f87171;
      --gold-color: #eab308;
    }

    body.theme-sepia {
      --bg-color: #fbf0d9;
      --text-color: #3b2d1d;
      --header-bg: rgba(251, 240, 217, 0.96);
      --card-bg: #f3e5c8;
      --border-color: #e2d2b0;
      --accent-color: #8b0000;
      --gold-color: #8c6d1f;
    }

    body.theme-light {
      --bg-color: #ffffff;
      --text-color: #1a1a1a;
      --header-bg: rgba(255, 255, 255, 0.96);
      --card-bg: #f4f5f7;
      --border-color: #e2e8f0;
      --accent-color: #c53030;
      --gold-color: #97741d;
    }

    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    html, body {
      margin: 0; padding: 0;
      background-color: var(--bg-color);
      color: var(--text-color);
      font-family: var(--font-family);
      font-size: var(--font-size);
      line-height: var(--line-height);
      min-height: 100vh;
      transition: background-color 0.25s ease, color 0.25s ease;
      overflow-x: hidden;
    }

    /* HEADER */
    header {
      position: fixed; top: 0; left: 0; right: 0; height: 54px;
      background: var(--header-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 14px; z-index: 100;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    header.hidden { transform: translateY(-100%); }

    .btn-icon {
      background: none; border: none; color: var(--text-color);
      font-size: 20px; padding: 8px; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      border-radius: 8px;
    }
    .header-title {
      font-size: 15px; font-weight: 600; color: var(--gold-color);
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      max-width: 58%; text-align: center;
    }
    .live-status {
      display: flex; align-items: center; gap: 5px; font-size: 11px; color: #10b981;
    }
    .live-dot {
      width: 7px; height: 7px; border-radius: 50%; background: #10b981;
      box-shadow: 0 0 8px #10b981;
    }
    .live-dot.offline { background: #3b82f6; box-shadow: 0 0 8px #3b82f6; }

    /* CONTENT */
    main {
      max-width: var(--max-width); margin: 0 auto;
      padding: 72px 18px 90px 18px;
    }
    .chapter-heading {
      text-align: center; margin-bottom: 26px;
    }
    .chapter-meta {
      font-size: 12px; color: var(--gold-color); opacity: 0.85; margin-bottom: 8px;
      text-transform: uppercase; letter-spacing: 1px; font-weight: 600;
    }
    .chapter-title-main {
      font-size: 1.55em; font-weight: 800; color: var(--accent-color);
      line-height: 1.35; margin: 0 0 16px 0;
    }
    .novel-body p {
      text-indent: 1.6em; margin-top: 0; margin-bottom: 0.85em;
      text-align: justify; word-break: break-word;
    }
    .novel-body strong { font-weight: 700; }
    .novel-body em { font-style: italic; }
    .novel-body hr {
      border: none; border-top: 1px dashed var(--border-color);
      margin: 2em auto; width: 60%;
    }

    /* FOOTER NAV */
    footer {
      position: fixed; bottom: 0; left: 0; right: 0; height: 54px;
      background: var(--header-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-top: 1px solid var(--border-color);
      display: flex; align-items: center; justify-content: space-around;
      padding: 0 16px; z-index: 100;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    footer.hidden { transform: translateY(100%); }

    .nav-btn {
      background: var(--card-bg); border: 1px solid var(--border-color);
      color: var(--text-color); font-size: 14px; font-weight: 600;
      padding: 7px 18px; border-radius: 20px; cursor: pointer;
      display: flex; align-items: center; gap: 6px;
    }
    .nav-btn:disabled { opacity: 0.35; cursor: not-allowed; }

    /* TOAST ALERT */
    .toast {
      position: fixed; top: 68px; left: 50%; transform: translateX(-50%) translateY(-30px);
      background: var(--accent-color); color: #ffffff;
      padding: 10px 20px; border-radius: 25px; font-size: 13px; font-weight: 600;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4); z-index: 200;
      opacity: 0; pointer-events: none; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); pointer-events: auto; }

    /* DRAWER MENU / TOC */
    .drawer-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.6);
      z-index: 150; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
    }
    .drawer-overlay.open { opacity: 1; pointer-events: auto; }

    .drawer {
      position: fixed; top: 0; bottom: 0; left: 0; width: 85%; max-width: 360px;
      background: var(--bg-color); z-index: 160;
      transform: translateX(-100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex; flex-direction: column; border-right: 1px solid var(--border-color);
    }
    .drawer.open { transform: translateX(0); }

    .drawer-header {
      padding: 16px 18px; border-bottom: 1px solid var(--border-color);
      display: flex; justify-content: space-between; align-items: center;
    }
    .drawer-title { font-size: 17px; font-weight: 700; color: var(--gold-color); }
    .drawer-list {
      flex: 1; overflow-y: auto; padding: 10px 0; -webkit-overflow-scrolling: touch;
    }
    .drawer-item {
      padding: 12px 18px; display: flex; align-items: center; justify-content: space-between;
      border-bottom: 1px solid rgba(255,255,255,0.03); cursor: pointer;
      font-size: 15px;
    }
    .drawer-item:active, .drawer-item.active {
      background: var(--card-bg); color: var(--gold-color); font-weight: 700;
    }
    .drawer-item-title {
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 250px;
    }

    /* BOTTOM SETTINGS SHEET */
    .sheet {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: var(--card-bg); border-top: 1px solid var(--border-color);
      border-top-left-radius: 20px; border-top-right-radius: 20px;
      z-index: 160; transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      padding: 20px 20px 36px 20px; max-width: 500px; margin: 0 auto;
    }
    .sheet.open { transform: translateY(0); }
    .sheet-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; text-align: center; }

    .setting-group { margin-bottom: 16px; }
    .setting-label { font-size: 13px; color: var(--gold-color); margin-bottom: 8px; font-weight: 600; }
    .theme-options { display: flex; gap: 8px; }
    .theme-btn {
      flex: 1; padding: 10px; border-radius: 10px; border: 1px solid var(--border-color);
      text-align: center; font-size: 13px; font-weight: 600; cursor: pointer;
      background: var(--bg-color); color: var(--text-color);
    }
    .theme-btn.active { border-color: var(--accent-color); color: var(--accent-color); }

    .font-control {
      display: flex; align-items: center; justify-content: space-between;
      background: var(--bg-color); border: 1px solid var(--border-color);
      border-radius: 10px; padding: 6px 14px;
    }
    .font-btn { background: none; border: none; font-size: 20px; color: var(--text-color); cursor: pointer; padding: 6px 14px; }

    .btn-offline-sync {
      width: 100%; padding: 12px; border-radius: 12px; background: var(--accent-color);
      color: white; border: none; font-size: 14px; font-weight: 600; cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 10px;
    }

    /* READING PROGRESS */
    .progress-bar {
      position: fixed; top: 54px; left: 0; height: 2.5px;
      background: var(--accent-color); width: 0%; z-index: 101;
      transition: width 0.1s linear;
    }
  </style>
</head>
<body class="theme-oled">

  <div class="progress-bar" id="progressBar"></div>

  <!-- HEADER -->
  <header id="topHeader">
    <button class="btn-icon" id="btnMenu" aria-label="Mục lục">☰</button>
    <div class="header-title" id="headerTitle">Phá Trời</div>
    <div class="live-status" id="statusBadge">
      <span class="live-dot" id="liveDot"></span>
      <span id="statusText">24/7</span>
    </div>
    <button class="btn-icon" id="btnSettings" aria-label="Cài đặt">⚙️</button>
  </header>

  <!-- CONTENT -->
  <main id="mainContainer">
    <div class="chapter-heading">
      <div class="chapter-meta" id="chapterMeta">ĐANG TẢI DỮ LIỆU...</div>
      <h1 class="chapter-title-main" id="chapterTitle">Phá Trời</h1>
    </div>
    <article class="novel-body" id="novelContent">
      <p style="text-align: center; opacity: 0.6;">Đang kết nối tới máy chủ đám mây...</p>
    </article>
  </main>

  <!-- FOOTER NAV -->
  <footer id="bottomFooter">
    <button class="nav-btn" id="btnPrev" disabled>‹ Chap trước</button>
    <button class="nav-btn" id="btnTocSmall">Mục lục</button>
    <button class="nav-btn" id="btnNext">Chap sau ›</button>
  </footer>

  <!-- DRAWER TOC -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <aside class="drawer" id="tocDrawer">
    <div class="drawer-header">
      <div class="drawer-title">Danh Sách Chương</div>
      <button class="btn-icon" id="btnCloseDrawer">✕</button>
    </div>
    <div style="padding: 10px 18px; font-size: 12px; color: var(--gold-color); border-bottom: 1px solid var(--border-color);">
      Tổng số: <strong id="tocTotal">46</strong> chương (118,637 từ)
    </div>
    <div class="drawer-list" id="tocList"></div>
  </aside>

  <!-- SETTINGS SHEET -->
  <div class="sheet" id="settingsSheet">
    <div class="sheet-title">Tùy Chọn Đọc Truyện</div>
    <div class="setting-group">
      <div class="setting-label">GIAO DIỆN NỀN</div>
      <div class="theme-options">
        <div class="theme-btn active" data-theme="theme-oled">OLED Đen</div>
        <div class="theme-btn" data-theme="theme-dark">Xám Đậm</div>
        <div class="theme-btn" data-theme="theme-sepia">Vàng Cát</div>
        <div class="theme-btn" data-theme="theme-light">Sáng</div>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">CỠ CHỮ (<span id="fontSizeVal">19</span>px)</div>
      <div class="font-control">
        <button class="font-btn" id="btnFontDec">A-</button>
        <span style="font-weight:600;">Cỡ chữ</span>
        <button class="font-btn" id="btnFontInc">A+</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">PHÔNG CHỮ</div>
      <div style="display: flex; gap: 8px;">
        <button class="theme-btn" id="btnFontSerif" style="flex:1;">Bookerly (Serif)</button>
        <button class="theme-btn" id="btnFontSans" style="flex:1;">Hiện đại (Sans)</button>
      </div>
    </div>
    <div class="setting-group">
      <div class="setting-label">TẢI TRUYỆN ĐỌC OFFLINE TRÊN ĐIỆN THOẠI</div>
      <button class="btn-offline-sync" id="btnCacheAll">
        <span>📥</span> <span id="cacheAllText">Tải trọn bộ 46 chương đọc khi tắt máy</span>
      </button>
    </div>
  </div>

  <div class="toast" id="liveToast">Đã cập nhật chương mới!</div>

  <script>
    let currentChapter = parseInt(localStorage.getItem('pha_troi_cur_ch') || '1');
    let totalChapters = 46;
    let chaptersData = [];
    let uiVisible = true;

    const topHeader = document.getElementById('topHeader');
    const bottomFooter = document.getElementById('bottomFooter');
    const progressBar = document.getElementById('progressBar');
    const headerTitle = document.getElementById('headerTitle');
    const chapterTitle = document.getElementById('chapterTitle');
    const chapterMeta = document.getElementById('chapterMeta');
    const novelContent = document.getElementById('novelContent');
    const tocList = document.getElementById('tocList');
    const tocTotal = document.getElementById('tocTotal');
    const btnPrev = document.getElementById('btnPrev');
    const btnNext = document.getElementById('btnNext');
    const btnMenu = document.getElementById('btnMenu');
    const btnTocSmall = document.getElementById('btnTocSmall');
    const btnCloseDrawer = document.getElementById('btnCloseDrawer');
    const tocDrawer = document.getElementById('tocDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const btnSettings = document.getElementById('btnSettings');
    const settingsSheet = document.getElementById('settingsSheet');
    const liveToast = document.getElementById('liveToast');
    const liveDot = document.getElementById('liveDot');
    const statusText = document.getElementById('statusText');

    // 1. Tải danh mục chương
    async function loadChaptersIndex(isInitial = false) {
      try {
        const res = await fetch('./data/chapters.json?v=' + Date.now());
        const data = await res.json();
        const prevTotal = totalChapters;
        chaptersData = data.chapters || [];
        totalChapters = chaptersData.length;
        tocTotal.innerText = totalChapters;

        // Render TOC
        tocList.innerHTML = chaptersData.map(ch => `
          <div class="drawer-item ${ch.chapter === currentChapter ? 'active' : ''}" onclick="selectChapter(${ch.chapter})">
            <div class="drawer-item-title">Chương ${ch.chapter}: ${ch.title.replace(/^Chương \\d+:\\s*/i, '')}</div>
            <span style="font-size:11px; opacity:0.6;">${ch.word_count ? ch.word_count.toLocaleString() + ' từ' : ''}</span>
          </div>
        `).join('');

        if (isInitial) {
          if (currentChapter > totalChapters) currentChapter = 1;
          loadChapter(currentChapter);
        } else if (totalChapters > prevTotal) {
          showToast(`✨ Có thêm chương mới! (Tổng: ${totalChapters} chương)`);
        }
      } catch (err) {
        console.warn('Đang đọc ở chế độ Offline:', err);
        statusText.innerText = 'OFFLINE';
        liveDot.classList.add('offline');
        if (isInitial) {
          loadChapter(currentChapter);
        }
      }
    }

    // 2. Tải nội dung chương
    async function loadChapter(num) {
      currentChapter = num;
      localStorage.setItem('pha_troi_cur_ch', num);
      window.scrollTo(0, 0);

      btnPrev.disabled = (currentChapter <= 1);
      btnNext.disabled = (currentChapter >= totalChapters);

      try {
        chapterTitle.innerText = 'Đang tải nội dung...';
        
        // Thử tải từ JSON tĩnh hoặc cache
        const res = await fetch(`./data/chapter_${num}.json`);
        const data = await res.json();

        headerTitle.innerText = `Chương ${data.chapter}: ${data.title.replace(/^Chương \\d+:\\s*/i, '')}`;
        chapterTitle.innerText = data.title;
        chapterMeta.innerText = `QUYỂN ${data.volume || 1} • HỒI ${data.arc || 1} • ${data.word_count ? data.word_count.toLocaleString() + ' TỪ' : ''}`;
        novelContent.innerHTML = data.html;

        // Update active TOC
        document.querySelectorAll('.drawer-item').forEach((el, idx) => {
          el.classList.toggle('active', (idx + 1) === currentChapter);
        });
      } catch (err) {
        novelContent.innerHTML = `<p style="color:#ef4444; text-align:center;">Không thể tải chương ${num}. Vui lòng thử lại hoặc tải offline trong cài đặt.</p>`;
      }
    }

    function selectChapter(num) {
      closeDrawer();
      loadChapter(num);
    }

    // 3. Tiến trình đọc
    window.addEventListener('scroll', () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (height > 0) ? (winScroll / height) * 100 : 0;
      progressBar.style.width = scrolled + '%';
    });

    // 4. Toggle UI khi chạm vào màn hình (distraction-free)
    document.getElementById('mainContainer').addEventListener('click', (e) => {
      if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
        uiVisible = !uiVisible;
        topHeader.classList.toggle('hidden', !uiVisible);
        bottomFooter.classList.toggle('hidden', !uiVisible);
      }
    });

    // Nav buttons
    btnPrev.onclick = () => { if (currentChapter > 1) loadChapter(currentChapter - 1); };
    btnNext.onclick = () => { if (currentChapter < totalChapters) loadChapter(currentChapter + 1); };

    // Drawer
    function openDrawer() { drawerOverlay.classList.add('open'); tocDrawer.classList.add('open'); }
    function closeDrawer() { drawerOverlay.classList.remove('open'); tocDrawer.classList.remove('open'); settingsSheet.classList.remove('open'); }
    btnMenu.onclick = openDrawer;
    btnTocSmall.onclick = openDrawer;
    btnCloseDrawer.onclick = closeDrawer;
    drawerOverlay.onclick = closeDrawer;

    // Settings
    btnSettings.onclick = () => {
      drawerOverlay.classList.add('open');
      settingsSheet.classList.add('open');
    };

    // Themes
    document.querySelectorAll('.theme-btn[data-theme]').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.theme-btn[data-theme]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const theme = btn.dataset.theme;
        document.body.className = theme;
        localStorage.setItem('pha_troi_theme', theme);
      };
    });

    // Font size
    let curFontSize = parseInt(localStorage.getItem('pha_troi_font_size') || '19');
    function updateFontSize(sz) {
      curFontSize = Math.min(Math.max(sz, 15), 28);
      document.documentElement.style.setProperty('--font-size', curFontSize + 'px');
      document.getElementById('fontSizeVal').innerText = curFontSize;
      localStorage.setItem('pha_troi_font_size', curFontSize);
    }
    document.getElementById('btnFontInc').onclick = () => updateFontSize(curFontSize + 1);
    document.getElementById('btnFontDec').onclick = () => updateFontSize(curFontSize - 1);

    // Font Family
    document.getElementById('btnFontSerif').onclick = () => {
      document.documentElement.style.setProperty('--font-family', '-apple-system, BlinkMacSystemFont, "Bookerly", "Georgia", "Palatino", serif');
      localStorage.setItem('pha_troi_font_family', 'serif');
    };
    document.getElementById('btnFontSans').onclick = () => {
      document.documentElement.style.setProperty('--font-family', '-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif');
      localStorage.setItem('pha_troi_font_family', 'sans');
    };

    // Tải toàn bộ để đọc offline
    document.getElementById('btnCacheAll').onclick = async () => {
      const btn = document.getElementById('btnCacheAll');
      const text = document.getElementById('cacheAllText');
      btn.disabled = true;
      text.innerText = "Đang lưu trữ dữ liệu offline...";

      try {
        if ('caches' in window) {
          const cache = await caches.open('pha-troi-v1');
          await cache.addAll(['./', './index.html', './manifest.json', './icon.svg', './data/chapters.json']);
          
          for (let i = 1; i <= totalChapters; i++) {
            text.innerText = `Đang tải: ${i}/${totalChapters} chương...`;
            await cache.add(`./data/chapter_${i}.json`);
          }
          text.innerText = `✅ Đã lưu toàn bộ ${totalChapters} chương offline!`;
          showToast(`Đã lưu toàn bộ ${totalChapters} chương vào máy. Tắt Wi-Fi vẫn đọc tốt!`);
        } else {
          text.innerText = "Trình duyệt không hỗ trợ Cache API";
        }
      } catch (err) {
        text.innerText = "Lỗi khi tải offline. Thử lại sau.";
        console.error(err);
      } finally {
        setTimeout(() => {
          btn.disabled = false;
          text.innerText = "Tải lại trọn bộ offline";
        }, 5000);
      }
    };

    function showToast(msg) {
      liveToast.innerText = msg;
      liveToast.classList.add('show');
      setTimeout(() => liveToast.classList.remove('show'), 4000);
    }

    // Init theme
    const savedTheme = localStorage.getItem('pha_troi_theme') || 'theme-oled';
    document.body.className = savedTheme;
    document.querySelectorAll('.theme-btn[data-theme]').forEach(b => b.classList.toggle('active', b.dataset.theme === savedTheme));
    updateFontSize(curFontSize);

    // Initial load
    loadChaptersIndex(true);

    // Service Worker registration
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('./sw.js').catch(console.error);
    }
  </script>
</body>
</html>
"""

def generate_sw():
    return """const CACHE_NAME = 'pha-troi-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
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
  // Stale-while-revalidate for data and assets
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

    # 1. Parse all chapters
    files = sorted([f for f in os.listdir(MANUSCRIPT_DIR) if f.endswith(".md") and f.startswith("ch_")])
    chapters_index = []
    total_words = 0
    for f in files:
        path = os.path.join(MANUSCRIPT_DIR, f)
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

    # 4. Generate manifest.json
    manifest_data = {
        "name": "Phá Trời — Tiểu Thuyết Đô Thị",
        "short_name": "Phá Trời",
        "description": "Ứng dụng đọc truyện trọn bộ thời gian thực cho Phá Trời",
        "start_url": "./index.html",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#000000",
        "theme_color": "#000000",
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

    # 5. Copy icon.svg
    src_icon = os.path.join(BASE_DIR, "system", "reader_app", "static", "icon.svg")
    dst_icon = os.path.join(DIST_DIR, "icon.svg")
    shutil.copy2(src_icon, dst_icon)

    print(f"[Build Complete] 46 chuong ({total_words:,} tu) -> {DIST_DIR}")
    return len(chapters_index), total_words

if __name__ == "__main__":
    build()
