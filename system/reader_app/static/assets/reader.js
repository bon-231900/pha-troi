/**
 * Phá Trời — Web Reader Client Script (reader.js)
 * Tối ưu hóa hiệu năng, SEO Clean Slugs, PWA offline, Theme & Reading Controls
 */
(function() {
  const CFG = window.CHAPTER_CONFIG || {};
  const CH_NUM = parseInt(CFG.chNum || 1, 10);
  const CLEAN_TITLE = CFG.cleanTitle || '';
  const TOTAL_CH = parseInt(CFG.totalCh || 81, 10);
  const SITE_URL = CFG.siteUrl || 'https://phatroi.com';

  // Early reset if freshly navigating from another chapter to avoid browser scroll jump
  try {
    if (sessionStorage.getItem('pha_troi_nav_fresh') === '1') {
      if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual';
      }
      window.scrollTo(0, 0);
    }
  } catch(e) {}

    // Efficient Single-DOM TOC Sync (Reduces chapter HTML size by 12KB)
    function ensureDrawerToc() {
      const drawerList = document.getElementById('tocDrawerList');
      const sidebarList = document.querySelector('.desktop-toc-sidebar .toc-list-content') || document.querySelector('.desktop-toc-sidebar > div:last-child');
      if (drawerList && sidebarList && drawerList.children.length === 0) {
        drawerList.innerHTML = sidebarList.innerHTML;
      }
    }

// Accent-Insensitive Vietnamese normalizer (Phase 3)
    function normalizeVi(str) {
      return (str || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/đ/g, 'd')
        .replace(/Đ/g, 'D')
        .toLowerCase()
        .trim();
    }

    // Unified Reading State (Phase 2)
    function getReadingState() {
      try {
        const raw = localStorage.getItem('pha_troi_reading_state');
        if (raw) return JSON.parse(raw);
      } catch(e) {}
      const oldCh = parseInt(localStorage.getItem('pha_troi_cur_ch') || '0', 10);
      const completed = [];
      if (oldCh > 1) {
        for (let i = 1; i < oldCh; i++) completed.push(i);
      }
      return {
        cur_ch: oldCh || CH_NUM,
        has_started: true,
        completed: completed,
        scroll_pct: 0,
        scroll_y: 0,
        updated_at: Date.now()
      };
    }

    function saveReadingState(state) {
      try {
        localStorage.setItem('pha_troi_reading_state', JSON.stringify(state));
        if (state.cur_ch) localStorage.setItem('pha_troi_cur_ch', String(state.cur_ch));
      } catch(e) {}
    }

    // Update current reading state immediately
    (function initChapterState() {
      const state = getReadingState();
      state.cur_ch = CH_NUM;
      state.has_started = true;
      state.updated_at = Date.now();
      saveReadingState(state);
    })();

    // Scroll Progress Bar, Reading % Indicator & Smart Auto-hide Navigation (Phase 1, 13)
    let lastScrollY = window.scrollY;
    let isBarsHidden = false;
    let scrollSaveTimer = null;
    const topHeader = document.getElementById('topHeader');
    const bottomBar = document.querySelector('.bottom-bar');
    const progressBar = document.getElementById('progressBar');
    const readProgressPct = document.getElementById('readProgressPct');

    function isAnyModalOrDrawerOpen() {
      const tocDrawer = document.getElementById('tocDrawer');
      const settingsModal = document.getElementById('settingsModal');
      const codexDrawer = document.getElementById('codexDrawer');
      return (
        (tocDrawer && tocDrawer.classList.contains('open')) ||
        (settingsModal && settingsModal.classList.contains('open')) ||
        (codexDrawer && codexDrawer.classList.contains('open'))
      );
    }

    function showBars() {
      if (topHeader) {
        topHeader.classList.remove('header-unpinned');
        topHeader.classList.add('header-pinned');
      }
      if (bottomBar) {
        bottomBar.classList.remove('bar-unpinned');
        bottomBar.classList.add('bar-pinned');
      }
      isBarsHidden = false;
    }

    function hideBars() {
      if (isAnyModalOrDrawerOpen()) return;
      if (topHeader) {
        topHeader.classList.remove('header-pinned');
        topHeader.classList.add('header-unpinned');
      }
      if (bottomBar) {
        bottomBar.classList.remove('bar-pinned');
        bottomBar.classList.add('bar-unpinned');
      }
      isBarsHidden = true;
    }

    window.addEventListener('scroll', () => {
      const curY = window.scrollY;
      const totalH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = totalH > 0 ? Math.min(100, Math.max(0, Math.round((curY / totalH) * 100))) : 0;
      
      if (progressBar) progressBar.style.width = pct + '%';
      if (readProgressPct) readProgressPct.innerText = pct + '%';

      // Smart auto-hide with anti-jitter threshold (Headroom pattern)
      if (curY > 80) {
        const diff = curY - lastScrollY;
        if (diff > 14 && !isBarsHidden) {
          hideBars();
        } else if (diff < -10 && isBarsHidden) {
          showBars();
        }
      } else if (isBarsHidden) {
        showBars();
      }
      lastScrollY = curY;

      // Debounce save scroll position (150ms) (Phase 1 & 2)
      clearTimeout(scrollSaveTimer);
      scrollSaveTimer = setTimeout(() => {
        try {
          const scrollKey = 'pha_troi_scroll_ch_' + CH_NUM;
          // Clear legacy buggy global key
          localStorage.removeItem('pha_troi_scroll_CH_NUM');

          // If reading near end (>= 85%), clear scroll memory so returning later starts fresh at top
          if (pct >= 85) {
            localStorage.removeItem(scrollKey);
          } else if (curY > 150) {
            localStorage.setItem(scrollKey, String(curY));
          } else {
            localStorage.removeItem(scrollKey);
          }

          const state = getReadingState();
          state.cur_ch = CH_NUM;
          state.scroll_y = curY;
          state.scroll_pct = pct;
          state.updated_at = Date.now();
          if (!state.completed) state.completed = [];
          if (pct >= 85 && !state.completed.includes(CH_NUM)) {
            state.completed.push(CH_NUM);
            if (typeof gtag === 'function' && !window._chCompletedTracked) {
              window._chCompletedTracked = true;
              gtag('event', 'complete_chapter', {
                chapter_number: CH_NUM,
                chapter_title: CLEAN_TITLE
              });
              if (CH_NUM === 1) gtag('event', 'complete_chapter_1');
              if (CH_NUM === 3) gtag('event', 'read_chapter_3');
            }
          }
          saveReadingState(state);
        } catch(e) {}
      }, 150);
    }, { passive: true });

    // Track chapter click navigation & GA4 Next Chapter Tracking
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (!link) return;
      const href = link.getAttribute('href') || '';
      if (href.includes('chuong-')) {
        try {
          sessionStorage.setItem('pha_troi_nav_fresh', '1');
        } catch(err) {}

        const isNextBtn = link.id === 'topNextBtn' || link.id === 'footerNextBtn' || link.classList.contains('btn-bottom-item') || link.classList.contains('btn-read-next-pulse');
        if (isNextBtn && typeof gtag === 'function') {
          gtag('event', 'click_next_chapter', {
            from_chapter: CH_NUM,
            to_chapter: CH_NUM + 1
          });
        }
      }
    });

    // Scroll Position Restoration on Revisit (Phase 1)
    window.addEventListener('DOMContentLoaded', () => {
      // 1. Dọn dẹp key lỗi cũ nếu còn tồn đọng trong localStorage
      try {
        localStorage.removeItem('pha_troi_scroll_CH_NUM');
      } catch(e) {}

      // 2. Kiểm tra cờ fresh navigation khi người đọc bấm chuyển chương
      let isFreshNav = false;
      try {
        if (sessionStorage.getItem('pha_troi_nav_fresh') === '1') {
          isFreshNav = true;
          sessionStorage.removeItem('pha_troi_nav_fresh');
        }
      } catch(e) {}

      if (isFreshNav || window.location.hash) {
        if ('scrollRestoration' in history) {
          history.scrollRestoration = 'manual';
        }
        if (!window.location.hash) {
          window.scrollTo({ top: 0, behavior: 'instant' });
        }
        return;
      }

      // 3. Chỉ khôi phục vị trí khi mở lại tab hoặc reload trang đang đọc dở
      const scrollKey = 'pha_troi_scroll_ch_' + CH_NUM;
      const savedScroll = parseInt(localStorage.getItem(scrollKey) || '0', 10);
      if (savedScroll > 150) {
        setTimeout(() => {
          if (window.scrollY < 80) {
            window.scrollTo({ top: savedScroll, behavior: 'instant' });
            showToast('📖 Đã khôi phục vị trí đọc gần nhất');
          }
        }, 80);
      }
    });

    // Tap reading text to toggle immersion mode (show/hide bars)
    const novelContent = document.getElementById('novelContent');
    if (novelContent) {
      novelContent.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' || window.getSelection().toString().length > 0) return;
        if (isBarsHidden) {
          showBars();
        } else {
          hideBars();
        }
      });
    }

    // Share Chapter Feature (Phase 5)
    function shareChapter() {
      const canonicalUrl = SITE_URL + '/chuong-' + CH_NUM + '/';
      const shareData = {
        title: 'Phá Trời — Chương ' + CH_NUM + ': ' + CLEAN_TITLE,
        text: 'Đọc Chương ' + CH_NUM + ': ' + CLEAN_TITLE + ' — Tiểu thuyết đô thị tu chân Sài Gòn 2026',
        url: canonicalUrl
      };
      if (navigator.share) {
        navigator.share(shareData).catch(() => {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(canonicalUrl).then(() => {
          showToast('✓ Đã sao chép liên kết Chương ' + CH_NUM);
        }).catch(() => {
          showToast('Liên kết: ' + canonicalUrl);
        });
      } else {
        showToast('Liên kết: ' + canonicalUrl);
      }
    }

    const btnShare = document.getElementById('btnShare');
    if (btnShare) btnShare.onclick = shareChapter;

    // Web Audio Synthesizer (Pink Noise Rain)
    let audioCtx = null, noiseNode = null, gainNode = null, filterNode = null;
    let isRainPlaying = false, rainVolume = 0.25;

    function initAudio() {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    function toggleRainSound() {
      if (isRainPlaying) { stopRainSound(); showToast('🌧️ Đã tắt âm thanh mưa'); }
      else { startRainSound(); showToast('🌧️ Bật âm thanh mưa đêm Sài Gòn (Thư giãn)'); }
      updateAudioIcons();
    }

    function startRainSound() {
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
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
      filterNode.frequency.value = 750;
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
        if (offIcon) offIcon.style.display = 'none';
        if (onIcon) onIcon.style.display = 'inline-block';
      } else {
        if (offIcon) offIcon.style.display = 'inline-block';
        if (onIcon) onIcon.style.display = 'none';
      }
    }

    document.getElementById('btnAmbient').onclick = toggleRainSound;
    document.getElementById('btnSheetAudioToggle').onclick = toggleRainSound;
    document.getElementById('audioVolume').oninput = (e) => {
      rainVolume = parseFloat(e.target.value);
      document.getElementById('audioVolVal').innerText = Math.round(rainVolume * 100) + '%';
      if (gainNode && audioCtx) gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
    };

    // Modals & Drawers
    const modalOverlay = document.getElementById('modalOverlay');
    const drawerToc = document.getElementById('drawerToc');
    const drawerCodex = document.getElementById('drawerCodex');
    const settingsSheet = document.getElementById('settingsSheet');
    const codexDrawerBody = document.getElementById('codexDrawerBody');
    const liveToast = document.getElementById('liveToast');
    const toastMsg = document.getElementById('toastMsg');
    let activeCodexTab = 'char';

    function closeAllDrawers() {
      modalOverlay.classList.remove('open');
      drawerToc.classList.remove('open');
      drawerCodex.classList.remove('open');
      settingsSheet.classList.remove('open');
    }

    function openToc() {
      ensureDrawerToc();
      closeAllDrawers();
      showBars();
      modalOverlay.classList.add('open');
      drawerToc.classList.add('open');
    }

    function openCodex() {
      closeAllDrawers();
      showBars();
      modalOverlay.classList.add('open');
      drawerCodex.classList.add('open');
      renderCodexDrawer(CH_NUM);
    }

    function openSettings() {
      closeAllDrawers();
      showBars();
      modalOverlay.classList.add('open');
      settingsSheet.classList.add('open');
    }

    modalOverlay.onclick = closeAllDrawers;
    document.getElementById('btnMenu').onclick = openToc;
    const btnMobToc = document.getElementById('btnMobileToc');
    if (btnMobToc) btnMobToc.onclick = openToc;
    document.getElementById('btnCloseToc').onclick = closeAllDrawers;

    // End-of-chapter "Về Mục Lục" button (Phase 1)
    const btnFooterToc = document.getElementById('btnFooterToc');
    if (btnFooterToc) btnFooterToc.onclick = openToc;

    document.getElementById('btnCodex').onclick = openCodex;
    document.getElementById('btnCloseCodex').onclick = closeAllDrawers;

    document.getElementById('btnSettings').onclick = openSettings;
    const btnMobSet = document.getElementById('btnMobileSettings');
    if (btnMobSet) btnMobSet.onclick = openSettings;
    document.getElementById('btnCloseSettings').onclick = closeAllDrawers;

    // Accent-Insensitive Filter in Chapter TOC drawer (Phase 3)
    document.getElementById('inputTocSearch').oninput = (e) => {
      ensureDrawerToc();
      const queryNorm = normalizeVi(e.target.value);
      document.querySelectorAll('#tocDrawerList .toc-item').forEach(item => {
        const textNorm = normalizeVi(item.innerText);
        item.style.display = (!queryNorm || textNorm.includes(queryNorm)) ? 'flex' : 'none';
      });
    };

    // Progressive Codex On-Demand Loader (Phase 6 & SEO Optimization)
let CODEX_DATA = null;
async function loadCodexData() {
  if (CODEX_DATA) return CODEX_DATA;
  try {
    const res = await fetch('/data/codex.json');
    CODEX_DATA = await res.json();
  } catch (e) {
    console.warn('[Codex] Could not load codex.json', e);
    CODEX_DATA = [];
  }
  return CODEX_DATA;
}

    // Progressive Codex Drawer & Anti-Spoiler (Phase 6)
    async function renderCodexDrawer(s) {
      const CODEX_DATA = await loadCodexData();
      if (!codexDrawerBody) return;
      const state = getReadingState();
      let maxCh = Math.max(s, state.cur_ch || 1);
      if (state.completed && state.completed.length > 0) {
        maxCh = Math.max(maxCh, Math.max(...state.completed));
      }

      let html = '';
      const filtered = CODEX_DATA.filter(it => it.category === activeCodexTab);
      if (filtered.length === 0) {
        html = '<p style="color:var(--text-muted); font-size:13px; text-align:center; padding:24px 0;">Đang cập nhật thêm mục mới...</p>';
      } else {
        filtered.forEach(it => {
          const isUnlocked = maxCh >= it.unlock_chapter;
          if (isUnlocked) {
            let statsHtml = '';
            if (it.stats) {
              for (const [k, v] of Object.entries(it.stats)) {
                statsHtml += `<div class="codex-stat"><span>${k}</span><span class="codex-stat-val">${v}</span></div>`;
              }
            }
            html += `
              <div class="codex-card">
                <span class="codex-badge">${it.badge}</span>
                <h3 class="codex-title">${it.name}</h3>
                <p class="codex-desc">${it.unlocked_desc}</p>
                ${statsHtml}
              </div>
            `;
          } else {
            html += `
              <div class="codex-card locked">
                <span class="codex-badge locked-badge">🔒 HỒ SƠ ẨN</span>
                <h3 class="codex-title" style="color:var(--text-muted);">${it.hidden_name || '???'}</h3>
                <p class="codex-desc">${it.hidden_desc || 'Hồ sơ chưa thể truy cập.'}</p>
                <div class="codex-unlock-hint">🔒 Đọc đến Chương ${it.unlock_chapter} để mở khóa chi tiết</div>
              </div>
            `;
          }
        });
      }
      codexDrawerBody.innerHTML = html;
    }

    const CODEX_TAB_LIST = ['tabCodexChar', 'tabCodexItem', 'tabCodexArtifact', 'tabCodexSkill', 'tabCodexLotus'];
    CODEX_TAB_LIST.forEach(id => {
      const btn = document.getElementById(id);
      if (btn) btn.onclick = () => {
        CODEX_TAB_LIST.forEach(b => document.getElementById(b)?.classList.remove('active'));
        btn.classList.add('active');
        activeCodexTab = btn.dataset.codex;
        renderCodexDrawer(CH_NUM);
      };
    });

    // Settings Handlers
    const THEMES = ['theme-peaceful-dark', 'theme-saigon-night', 'theme-gentle-light', 'theme-paper', 'theme-oled', 'theme-warm-dark', 'theme-sepia'];
    function setTheme(theme) {
      THEMES.forEach(t => {
        document.documentElement.classList.remove(t);
        document.body.classList.remove(t);
      });
      document.documentElement.classList.add(theme);
      document.body.classList.add(theme);

      let activeThemeKey = theme;
      if (theme === 'theme-peaceful-dark') activeThemeKey = 'theme-saigon-night';
      if (theme === 'theme-oled') activeThemeKey = 'theme-warm-dark';
      if (theme === 'theme-paper') activeThemeKey = 'theme-gentle-light';

      document.querySelectorAll('.theme-opt').forEach(opt => {
        const optTheme = opt.dataset.theme;
        const matches = (optTheme === theme || optTheme === activeThemeKey);
        opt.classList.toggle('active', matches);
      });

      const sunIcon = document.getElementById('iconSun');
      const moonIcon = document.getElementById('iconMoon');
      if (theme === 'theme-gentle-light' || theme === 'theme-paper') {
        if (sunIcon) sunIcon.style.display = 'inline-block';
        if (moonIcon) moonIcon.style.display = 'none';
      } else {
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) moonIcon.style.display = 'inline-block';
      }
      localStorage.setItem('pha_troi_theme', theme);
    }

    document.querySelectorAll('.theme-opt').forEach(opt => {
      opt.onclick = () => {
        setTheme(opt.dataset.theme);
        showToast('🎨 Giao diện: ' + opt.innerText.trim());
      };
    });

    document.getElementById('btnQuickTheme').onclick = () => {
      const isLight = document.body.classList.contains('theme-gentle-light') || document.body.classList.contains('theme-paper');
      const target = isLight ? 'theme-saigon-night' : 'theme-gentle-light';
      setTheme(target);
      showToast(target === 'theme-gentle-light' ? '☀️ Đã bật giao diện Sáng' : '🌙 Đã bật giao diện Tối');
    };

    const savedTheme = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
    setTheme(savedTheme);

    let curFontSize = parseInt(localStorage.getItem('pha_troi_font_size') || '19');
    function applyFontSize(size) {
      curFontSize = Math.max(15, Math.min(26, size));
      document.documentElement.style.setProperty('--font-size', curFontSize + 'px');
      document.getElementById('fontSizeVal').innerText = curFontSize + 'px';
      localStorage.setItem('pha_troi_font_size', curFontSize);
    }
    document.getElementById('btnFontDec').onclick = () => applyFontSize(curFontSize - 1);
    document.getElementById('btnFontInc').onclick = () => applyFontSize(curFontSize + 1);
    applyFontSize(curFontSize);

    function applyReaderWidth(w) {
      document.documentElement.style.setProperty('--reader-max-width', w + 'px');
      localStorage.setItem('pha_troi_reader_width', w);
      document.querySelectorAll('.btn-opt-step[data-opt-width]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.optWidth === String(w));
      });
    }
    document.querySelectorAll('.btn-opt-step[data-opt-width]').forEach(btn => {
      btn.onclick = () => {
        applyReaderWidth(parseInt(btn.dataset.optWidth));
        showToast('📏 Khung đọc: ' + btn.innerText.trim());
      };
    });
    const savedWidth = parseInt(localStorage.getItem('pha_troi_reader_width') || '760');
    applyReaderWidth(savedWidth);

    function applyLineHeight(lh) {
      document.documentElement.style.setProperty('--reader-line-height', lh);
      localStorage.setItem('pha_troi_line_height', lh);
      document.querySelectorAll('.btn-opt-step[data-opt-lh]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.optLh === String(lh));
      });
    }
    document.querySelectorAll('.btn-opt-step[data-opt-lh]').forEach(btn => {
      btn.onclick = () => {
        applyLineHeight(parseFloat(btn.dataset.optLh));
        showToast('📄 Giãn dòng: ' + btn.innerText.trim());
      };
    });
    const savedLh = parseFloat(localStorage.getItem('pha_troi_line_height') || '1.85');
    applyLineHeight(savedLh);

    const FONT_SERIF = "'Lora', 'Georgia', serif";
    const FONT_SANS = "'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif";
    document.getElementById('btnFontSerif').onclick = () => {
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
      localStorage.setItem('pha_troi_font_family', 'serif');
      showToast('📖 Phông Có Chân (Lora)');
    };
    document.getElementById('btnFontSans').onclick = () => {
      document.documentElement.style.setProperty('--font-family', FONT_SANS);
      document.body.style.setProperty('--font-family', FONT_SANS);
      localStorage.setItem('pha_troi_font_family', 'sans');
      showToast('📱 Phông Không Chân (Be Vietnam Pro)');
    };

    const savedFont = localStorage.getItem('pha_troi_font_family');
    if (savedFont === 'serif') {
      document.documentElement.style.setProperty('--font-family', FONT_SERIF);
      document.body.style.setProperty('--font-family', FONT_SERIF);
    }

    // Keyboard navigation (Phase 1 & 5)
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowLeft') {
        const prevBtn = document.querySelector('.desktop-nav-left a');
        if (prevBtn && !prevBtn.classList.contains('disabled')) window.location.href = prevBtn.href;
      } else if (e.key === 'ArrowRight') {
        const nextBtn = document.querySelector('.desktop-nav-right a');
        if (nextBtn && !nextBtn.classList.contains('disabled')) window.location.href = nextBtn.href;
      } else if (e.key.toLowerCase() === 'h') {
        window.location.href = '/';
      } else if (e.key.toLowerCase() === 's') {
        shareChapter();
      } else if (e.key.toLowerCase() === 't') {
        document.getElementById('btnQuickTheme').click();
      } else if (e.key.toLowerCase() === 'm') {
        openToc();
      } else if (e.key.toLowerCase() === 'c') {
        openCodex();
      } else if (e.key === 'Escape') {
        closeAllDrawers();
      }
    });

    function showToast(msg) {
      toastMsg.innerText = msg;
      liveToast.classList.add('show');
      setTimeout(() => liveToast.classList.remove('show'), 2400);
    }

    const btnCardCodex = document.getElementById('btnCardCodex');
    if (btnCardCodex) {
      btnCardCodex.onclick = () => openCodex();
    }

    // Dynamic Next Chapter Resolver (Bảo đảm hiển thị chương mới kể cả khi dính browser cache cũ)
    (function() {
      const curCh = CH_NUM;
      fetch('/data/chapters.json?t=' + Date.now())
        .then(r => r.json())
        .then(data => {
          if (!data || !data.chapters) return;
          const total = data.total || data.chapters.length;

          document.querySelectorAll('.nav-live-badge').forEach(el => {
            el.innerHTML = '<span class="dot-live"></span> ' + total + ' CHƯƠNG';
          });

          if (curCh < total) {
            const nextNum = curCh + 1;
            const nextUrl = '/chuong-' + nextNum + '/';
            const nextCh = data.chapters.find(c => c.chapter === nextNum);

            document.querySelectorAll('.desktop-nav-right a, a.btn-bottom-item:nth-child(4)').forEach(a => {
              a.classList.remove('disabled');
              a.setAttribute('href', nextUrl);
            });

            const fNext = document.getElementById('footerNextBtn');
            if (fNext) {
              fNext.classList.remove('disabled');
              fNext.setAttribute('href', nextUrl);
              const span = fNext.querySelector('span');
              if (span) span.textContent = 'Chương Sau (' + nextNum + ')';
            }

            const card = document.getElementById('nextChapterCard');
            if (card && card.classList.contains('last-chapter-card') && nextCh) {
              const nextTitle = (nextCh.title || '').replace(/^Chương\s+\d+:\s*/i, '');
              const nextWords = (nextCh.word_count || 0).toLocaleString();
              card.className = 'next-chapter-card';
              card.innerHTML = '<div class="next-card-badge">TIẾP NỐI HÀNH TRÌNH</div>' +
                '<div class="next-card-label">CHƯƠNG TIẾP THEO:</div>' +
                '<h3 class="next-card-title">Chương ' + nextNum + ': ' + nextTitle + '</h3>' +
                '<div class="next-card-meta">' +
                  '<span>Quyển ' + (nextCh.volume || 1) + ' • Hồi ' + (nextCh.arc || 1) + '</span>' +
                  '<span>•</span><span>' + nextWords + ' từ</span>' +
                '</div>' +
                '<a href="' + nextUrl + '" class="btn-read-next-pulse">' +
                  '<span>Tiếp Tục Đọc Chương ' + nextNum + ' →</span>' +
                '</a>';
            }
          }
        })
        .catch(() => {});
    })();

    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(reg => reg.update()).catch(() => {});
      });
    }
})();
