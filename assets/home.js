/**
 * Phá Trời — Homepage Client Script (home.js)
 * Tối ưu hóa hiệu năng, PWA offline, Lọc chương, Codex Bách Khoa
 */
(function() {
  const CFG = window.HOME_CONFIG || {};
  const TOTAL_CH = parseInt(CFG.totalCh || 81, 10);
  const TOTAL_WORDS = CFG.totalWords || '238,571';

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

    // Check old hash links or query params and redirect to clean slug
    (function checkLegacyRedirect() {
      const hash = window.location.hash;
      const mHash = hash.match(/#\/chapter\/(\d+)/);
      if (mHash) {
        window.location.replace('/chuong-' + mHash[1] + '/');
        return;
      }
      const params = new URLSearchParams(window.location.search);
      const chParam = params.get('chuong');
      if (chParam) {
        window.location.replace('/chuong-' + chParam + '/');
        return;
      }
    })();

    // Unified Reading State Helper (Phase 2)
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
        cur_ch: oldCh || 1,
        has_started: (oldCh > 0),
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

    let chaptersData = (window.HOME_CONFIG && window.HOME_CONFIG.chapters) || [];
    let totalChapters = TOTAL_CH;
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

    const btnAmb = document.getElementById('btnAmbient');
    if (btnAmb) btnAmb.onclick = toggleRainSound;
    const btnSheetAudio = document.getElementById('btnSheetAudioToggle');
    if (btnSheetAudio) btnSheetAudio.onclick = toggleRainSound;
    const audioVol = document.getElementById('audioVolume');
    if (audioVol) audioVol.oninput = (e) => {
      rainVolume = parseFloat(e.target.value);
      const audioVolVal = document.getElementById('audioVolVal');
      if (audioVolVal) audioVolVal.innerText = Math.round(rainVolume * 100) + '%';
      if (gainNode && audioCtx) gainNode.gain.setValueAtTime(rainVolume, audioCtx.currentTime);
    };

    // Resume Reading & Hero CTA Update (Phase 2 & Phase 4)
    function updateContinueReadingCard() {
      const state = getReadingState();
      const hasHistory = state.has_started;
      const savedCh = state.cur_ch || 1;
      
      const contCard = document.getElementById('continueReadingCard');
      const contPill = document.getElementById('contPill');
      const contEl = document.getElementById('contChName');
      const metaEl = document.getElementById('contChMeta');
      const btnJump = document.getElementById('btnContinueJump');
      const heroPrimary = document.getElementById('btnHeroReadPrimary');
      const heroReadText = document.getElementById('heroPrimaryText');
      const mobileHeroPrimary = document.getElementById('btnMobileHeroReadPrimary');
      const mobileHeroReadText = document.getElementById('mobileHeroPrimaryText');

      if (!hasHistory) {
        if (contCard) contCard.classList.add('welcome-mode');
        if (contPill) contPill.innerText = 'HÀNH TRÌNH KHỞI ĐẦU';
        if (contEl) contEl.innerText = 'Bạn chưa từng đọc Phá Trời? Bắt đầu từ Chương 1';
        if (metaEl) metaEl.innerText = 'Dấn thân vào đại phong ấn sông ngầm Sài Gòn 2.5 triệu năm cùng Minh An';
        if (btnJump) { btnJump.innerText = 'Bắt Đầu Hành Trình →'; btnJump.href = './chuong-1/'; }
        if (heroPrimary) heroPrimary.href = './chuong-1/';
        if (heroReadText) heroReadText.innerText = 'Bắt Đầu Đọc — Chương 1';
        if (mobileHeroPrimary) mobileHeroPrimary.href = './chuong-1/';
        if (mobileHeroReadText) mobileHeroReadText.innerText = 'Bắt Đầu Đọc — Chương 1';
      } else {
        const chInfo = chaptersData.find(c => c.chapter === savedCh) || { title: `Chương ${savedCh}`, arc: 1 };
        const cleanTitle = chInfo.title.replace(/^Chương\s+\d+:\s*/i, '');
        const pct = Math.round((savedCh / totalChapters) * 100);
        const targetUrl = `./chuong-${savedCh}/`;

        if (contCard) contCard.classList.remove('welcome-mode');
        if (contPill) contPill.innerText = 'BẠN ĐANG ĐỌC';
        if (contEl) contEl.innerText = `Chương ${savedCh}: ${cleanTitle}`;
        if (metaEl) metaEl.innerText = `Tiến độ: Chương ${savedCh} / ${totalChapters} (${pct}%) · Hồi ${chInfo.arc || 1}`;
        if (btnJump) { btnJump.innerText = `Tiếp Tục Đọc Chương ${savedCh} →`; btnJump.href = targetUrl; }
        if (heroPrimary) heroPrimary.href = targetUrl;
        if (heroReadText) heroReadText.innerText = `Tiếp Tục Đọc — Chương ${savedCh}`;
        if (mobileHeroPrimary) mobileHeroPrimary.href = targetUrl;
        if (mobileHeroReadText) mobileHeroReadText.innerText = `Tiếp Tục Đọc — Chương ${savedCh}`;
      }

      // Calculate read count
      const readCount = state.completed ? state.completed.length : (hasHistory ? (savedCh > 1 ? savedCh - 1 : 0) : 0);
      const overallPct = Math.round((readCount / totalChapters) * 100);
      
      const hProgText = document.getElementById('homeTocProgressText');
      const hProgFill = document.getElementById('homeTocProgressFill');
      if (hProgText) hProgText.innerText = `Đã đọc ${readCount} / ${totalChapters} chương (${overallPct}%)`;
      if (hProgFill) hProgFill.style.width = overallPct + '%';

      const dProgText = document.getElementById('drawerTocProgressText');
      const dProgFill = document.getElementById('drawerTocProgressFill');
      if (dProgText) dProgText.innerText = `Đã đọc ${readCount} / ${totalChapters} chương (${overallPct}%)`;
      if (dProgFill) dProgFill.style.width = overallPct + '%';

      renderHomeToc();
      renderTOC();
      renderCodexPreview();
      renderCodexDrawer();
    }

    const btnHeroToc = document.getElementById('btnHeroTocScroll');
    if (btnHeroToc) {
      btnHeroToc.onclick = (e) => {
        e.preventDefault();
        document.getElementById('sectionToc').scrollIntoView({ behavior: 'smooth' });
      };
    }
    const btnMobileHeroToc = document.getElementById('btnMobileHeroTocScroll');
    if (btnMobileHeroToc) {
      btnMobileHeroToc.onclick = (e) => {
        e.preventDefault();
        document.getElementById('sectionToc').scrollIntoView({ behavior: 'smooth' });
      };
    }
    const btnHeroCodex = document.getElementById('btnHeroCodexOpen');
    if (btnHeroCodex) btnHeroCodex.onclick = () => openCodex();
    const btnMobileHeroCodex = document.getElementById('btnMobileHeroCodexOpen');
    if (btnMobileHeroCodex) btnMobileHeroCodex.onclick = () => openCodex();
    const btnViewAllCodex = document.getElementById('btnViewAllCodex');
    if (btnViewAllCodex) btnViewAllCodex.onclick = () => openCodex();

    // GA4 Home Tracking
    const heroReadBtn = document.getElementById('btnHeroReadPrimary');
    if (heroReadBtn) {
      heroReadBtn.addEventListener('click', () => {
        if (typeof gtag === 'function') {
          const isContinue = heroReadBtn.innerText.includes('Tiếp Tục');
          gtag('event', isContinue ? 'click_continue_read' : 'click_hero_start_read');
        }
      });
    }
    const contJumpBtn = document.getElementById('btnContinueJump');
    if (contJumpBtn) {
      contJumpBtn.addEventListener('click', () => {
        if (typeof gtag === 'function') {
          gtag('event', 'click_continue_read');
        }
      });
    }

    async function loadChaptersIndex() {
      try {
        const res = await fetch('./data/chapters.json?v=' + Date.now());
        const data = await res.json();
        chaptersData = data.chapters || [];
        totalChapters = chaptersData.length;
        document.getElementById('tocTotalCount').innerText = totalChapters;
        updateContinueReadingCard();
      } catch (err) {
        console.warn('Lỗi đọc dữ liệu chapters.json:', err);
      }
    }

    // TOC Drawer Render (Phase 3)
    function renderTOC() {
      const rawVal = document.getElementById('inputTocSearch').value;
      const searchNorm = normalizeVi(rawVal);
      const state = getReadingState();
      const savedCh = state.cur_ch || 0;
      const completedSet = new Set(state.completed || []);

      const filtered = chaptersData.filter(ch => {
        const titleNorm = normalizeVi(ch.title);
        const locNorm = normalizeVi(ch.location || '');
        const matchSearch = !searchNorm || titleNorm.includes(searchNorm) || locNorm.includes(searchNorm) || String(ch.chapter).includes(searchNorm);
        const arcNum = Number(ch.arc) || 1;
        const matchArc = (activeArcFilter === 'all') ||
                         (activeArcFilter === 'arc1' && arcNum === 1) ||
                         (activeArcFilter === 'arc2' && arcNum === 2);
        return matchSearch && matchArc;
      });

      const renderHtml = filtered.map(ch => {
        let statusBadge = '';
        if (state.has_started) {
          if (ch.chapter === savedCh) {
            statusBadge = '<span class="ch-status-tag current">● Đang đọc</span>';
          } else if (completedSet.has(ch.chapter) || ch.chapter < savedCh) {
            statusBadge = '<span class="ch-status-tag read">✓ Đã đọc</span>';
          } else {
            statusBadge = '<span class="ch-status-tag unread">Chưa đọc</span>';
          }
        }

        return `
          <a href="./chuong-${ch.chapter}/" class="toc-item">
            <div class="toc-info">
              <div class="toc-num">
                <span>Hồi ${ch.arc || 1} · Chương ${ch.chapter}</span>
                ${statusBadge}
              </div>
              <div class="toc-name">${ch.title.replace(/^Chương\s+\d+:\s*/i, '')}</div>
            </div>
            <span class="toc-meta">${ch.word_count ? ch.word_count.toLocaleString() + ' từ' : ''}</span>
          </a>
        `;
      }).join('');

      tocDrawerList.innerHTML = renderHtml || '<p style="text-align:center; color:var(--text-muted); padding:20px;">Không tìm thấy chương nào.</p>';
    }

    document.getElementById('inputTocSearch').oninput = renderTOC;

    document.querySelectorAll('.drawer-tab-btn[data-filter]').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.drawer-tab-btn[data-filter]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeArcFilter = btn.dataset.filter;
        renderTOC();
      };
    });

    // Homepage TOC Grid Render (Phase 3)
    function renderHomeToc() {
      const rawVal = document.getElementById('inputHomeSearch')?.value || '';
      const searchNorm = normalizeVi(rawVal);
      const state = getReadingState();
      const savedCh = state.cur_ch || 0;
      const completedSet = new Set(state.completed || []);

      const filtered = chaptersData.filter(ch => {
        const titleNorm = normalizeVi(ch.title);
        const locNorm = normalizeVi(ch.location || '');
        const matchSearch = !searchNorm || titleNorm.includes(searchNorm) || locNorm.includes(searchNorm) || String(ch.chapter).includes(searchNorm);
        const arcNum = Number(ch.arc) || 1;
        const matchArc = (homeArcFilter === 'all') ||
                         (homeArcFilter === 'arc1' && arcNum === 1) ||
                         (homeArcFilter === 'arc2' && arcNum === 2);
        return matchSearch && matchArc;
      });

      const gridHtml = filtered.map(ch => {
        let statusBadge = '';
        let cardClass = '';
        if (state.has_started) {
          if (ch.chapter === savedCh) {
            statusBadge = '<span class="ch-status-tag current">● Đang đọc</span>';
            cardClass = 'is-current';
          } else if (completedSet.has(ch.chapter) || ch.chapter < savedCh) {
            statusBadge = '<span class="ch-status-tag read">✓ Đã đọc</span>';
            cardClass = 'is-read';
          } else {
            statusBadge = '<span class="ch-status-tag unread">Chưa đọc</span>';
          }
        }

        return `
          <a href="./chuong-${ch.chapter}/" class="home-ch-card ${cardClass}">
            <div class="home-ch-info">
              <div class="home-ch-meta-top">
                <span>HỒI ${ch.arc || 1} · CHƯƠNG ${ch.chapter}</span>
                ${statusBadge}
              </div>
              <div class="home-ch-title">${ch.title.replace(/^Chương\s+\d+:\s*/i, '')}</div>
              <div class="home-ch-meta-bottom">
                <span>${ch.word_count ? ch.word_count.toLocaleString() + ' từ' : ''}</span>
                ${ch.location ? '<span>· ' + ch.location.split(',')[0] + '</span>' : ''}
              </div>
            </div>
            <div class="home-ch-arrow">→</div>
          </a>
        `;
      }).join('');

      if (homeTocGrid) {
        homeTocGrid.innerHTML = gridHtml || '<p style="text-align:center; color:var(--text-muted); grid-column: 1/-1; padding:30px;">Không tìm thấy chương phù hợp.</p>';
      }
    }

    document.getElementById('inputHomeSearch').oninput = renderHomeToc;

    document.querySelectorAll('.home-tab-btn[data-home-filter]').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.home-tab-btn[data-home-filter]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        homeArcFilter = btn.dataset.homeFilter;
        renderHomeToc();
      };
    });

    // Codex Data & Anti-Spoiler Logic (Phase 6)
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

    function getHighestUnlockedChapter() {
      const state = getReadingState();
      let maxCh = state.cur_ch || 1;
      if (state.completed && state.completed.length > 0) {
        maxCh = Math.max(maxCh, Math.max(...state.completed));
      }
      return maxCh;
    }

    async function renderCodexPreview() {
      if (!homeCodexGrid) return;
      const CODEX_DATA = await loadCodexData();
      const maxCh = getHighestUnlockedChapter();
      let unlockedCount = 0;
      CODEX_DATA.forEach(it => {
        if (maxCh >= it.unlock_chapter) unlockedCount++;
      });

      const pillEl = document.getElementById('homeCodexProgressPill');
      if (pillEl) pillEl.innerText = `Đã khám phá ${unlockedCount} / ${CODEX_DATA.length} mục`;

      let html = '';
      const previewItems = CODEX_DATA.slice(0, 6);
      previewItems.forEach(it => {
        const isUnlocked = maxCh >= it.unlock_chapter;
        if (isUnlocked) {
          html += `
            <div class="home-codex-card" onclick="openCodexTab('${it.category}')">
              <span class="home-codex-badge">${it.badge}</span>
              <div class="home-codex-name">${it.name}</div>
              <p class="home-codex-desc">${it.unlocked_desc}</p>
            </div>
          `;
        } else {
          html += `
            <div class="home-codex-card locked" onclick="openCodexTab('${it.category}')">
              <span class="home-codex-badge locked-badge">🔒 HỒ SƠ ẨN</span>
              <div class="home-codex-name" style="color:var(--text-muted);">${it.hidden_name || '???'}</div>
              <p class="home-codex-desc">${it.hidden_desc || 'Mục này chứa thông tin bảo mật. Đọc tiếp để khám phá.'}</p>
              <div class="codex-unlock-hint">🔒 Đọc đến Chương ${it.unlock_chapter} để mở khóa</div>
            </div>
          `;
        }
      });
      homeCodexGrid.innerHTML = html;
    }

    async function renderCodexDrawer() {
      if (!codexDrawerBody) return;
      const CODEX_DATA = await loadCodexData();
      const maxCh = getHighestUnlockedChapter();
      let unlockedCount = 0;
      CODEX_DATA.forEach(it => {
        if (maxCh >= it.unlock_chapter) unlockedCount++;
      });

      const drawerLabel = document.getElementById('drawerCodexProgressLabel');
      if (drawerLabel) drawerLabel.innerText = `Đã khám phá ${unlockedCount} / ${CODEX_DATA.length} mục`;

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
    function openCodexTab(tabName) {
      activeCodexTab = tabName;
      CODEX_TAB_LIST.forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.classList.toggle('active', btn.dataset.codex === tabName);
      });
      openCodex();
    }

    CODEX_TAB_LIST.forEach(id => {
      const btn = document.getElementById(id);
      if (btn) btn.onclick = () => openCodexTab(btn.dataset.codex);
    });

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
      renderTOC();
    }

    function openCodex() {
      closeAllDrawers();
      modalOverlay.classList.add('open');
      drawerCodex.classList.add('open');
      renderCodexDrawer();
    }

    function openSettings() {
      closeAllDrawers();
      modalOverlay.classList.add('open');
      settingsSheet.classList.add('open');
    }

    if (modalOverlay) modalOverlay.onclick = closeAllDrawers;
    const btnMenu = document.getElementById('btnMenu');
    if (btnMenu) btnMenu.onclick = openToc;
    const btnCloseToc = document.getElementById('btnCloseToc');
    if (btnCloseToc) btnCloseToc.onclick = closeAllDrawers;
    const btnCodex = document.getElementById('btnCodex');
    if (btnCodex) btnCodex.onclick = openCodex;
    const btnCloseCodex = document.getElementById('btnCloseCodex');
    if (btnCloseCodex) btnCloseCodex.onclick = closeAllDrawers;
    const btnSettings = document.getElementById('btnSettings');
    if (btnSettings) btnSettings.onclick = openSettings;
    const btnCloseSettings = document.getElementById('btnCloseSettings');
    if (btnCloseSettings) btnCloseSettings.onclick = closeAllDrawers;

    // Reading Settings Handlers (Phase 1)
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

    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key.toLowerCase() === 't') document.getElementById('btnQuickTheme').click();
      else if (e.key.toLowerCase() === 'm') openToc();
      else if (e.key.toLowerCase() === 'c') openCodex();
      else if (e.key === 'Escape') closeAllDrawers();
    });

    function showToast(msg) {
      toastMsg.innerText = msg;
      liveToast.classList.add('show');
      setTimeout(() => liveToast.classList.remove('show'), 2400);
    }

    // Offline Batched Download UX (Phase 7)
    document.getElementById('btnCacheAll').onclick = async () => {
      const btn = document.getElementById('btnCacheAll');
      const text = document.getElementById('cacheAllText');
      const sub = document.getElementById('cacheSubText');
      btn.disabled = true;
      text.innerText = "Đang kết nối lưu trữ...";

      try {
        const urlsToCache = [
          './',
          './index.html',
          './data/chapters.json',
          './data/codex.json',
          './icon.svg',
          './cover.svg',
          './manifest.json',
          './assets/logo.webp',
          './assets/cover_vertical.webp',
          './assets/hero_horizontal.webp',
          './assets/tieu-thuyet-pha-troi-do-thi-tu-chan-sai-gon-huyen-ao.webp'
        ];
        for (let i = 1; i <= totalChapters; i++) {
          urlsToCache.push(`./chuong-${i}/`);
        }

        if ('caches' in window) {
          const cache = await caches.open('pha-troi-vTOTAL_CH-offline');
          let count = 0;
          const chunkSize = 5; // Chunked processing to prevent thread lock
          for (let i = 0; i < urlsToCache.length; i += chunkSize) {
            const chunk = urlsToCache.slice(i, i + chunkSize);
            await Promise.all(chunk.map(async (url) => {
              try {
                const res = await fetch(url);
                if (res.ok) await cache.put(url, res);
                count++;
              } catch (e) {}
            }));
            const pct = Math.round((count / urlsToCache.length) * 100);
            text.innerText = `Đang tải: ${count}/${urlsToCache.length} (${pct}%)...`;
          }
          text.innerText = `✓ Đã tải để đọc offline!`;
          if (sub) sub.innerText = `Trọn bộ ${totalChapters} chương đã sẵn sàng khi mất mạng.`;
          showToast(`✨ Đã tải trọn bộ offline thành công!`);
        } else {
          text.innerText = "Trình duyệt không hỗ trợ Cache Storage";
        }
      } catch (err) {
        text.innerText = "Lỗi khi lưu offline";
      } finally {
        setTimeout(() => {
          btn.disabled = false;
          text.innerText = "Tải Toàn Bộ TOTAL_CH Chương Để Đọc Offline";
          if (sub) sub.innerText = "TOTAL_CH chương · TOTAL_WORDS từ • Có thể đọc khi không có mạng";
        }, 4000);
      }
    };

    // Cinematic Scroll Controller (Parallax & Header Title Reveal) (Phase 13)
    function initCinematicScroll() {
      const heroBg = document.querySelector('.hero-titlepage-bg');
      const heroSection = document.querySelector('.hero-titlepage');
      const coverFrame = document.querySelector('.titlepage-cover-frame');
      const topHeader = document.getElementById('topHeader');
      const scrollHint = document.getElementById('heroScrollHint');
      const titleBlock = document.querySelector('.titlepage-meta-block');

      if (!heroSection || !topHeader) return;

      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      let isTicking = false;
      let heroHeight = heroSection.offsetHeight;

      window.addEventListener('resize', () => {
        heroHeight = heroSection.offsetHeight;
      }, { passive: true });

      function onScroll() {
        const scrollY = window.scrollY || window.pageYOffset;

        // 1. Scroll Hint: Fade out when user starts scrolling
        if (scrollHint) {
          if (scrollY > 20) {
            scrollHint.classList.add('is-hidden');
          } else {
            scrollHint.classList.remove('is-hidden');
          }
        }

        // 2. Parallax Depth: only update when within hero view
        if (scrollY <= heroHeight + 60) {
          if (!prefersReducedMotion && heroBg) {
            const parallaxOffset = Math.round(scrollY * 0.32);
            heroBg.style.transform = `translate3d(0, ${parallaxOffset}px, 0)`;
          }
          if (!prefersReducedMotion && coverFrame) {
            const fadeProgress = Math.min(1, Math.max(0, scrollY / (heroHeight * 0.7)));
            coverFrame.style.opacity = (1 - fadeProgress * 0.4).toFixed(3);
          }
        }

        // 3. Header Title Reveal: Reveal when scrolled past cover/title block
        const triggerThreshold = titleBlock ? (titleBlock.offsetTop + 30) : 250;
        if (scrollY >= triggerThreshold) {
          topHeader.classList.add('scrolled-past-hero');
          document.body.classList.add('scrolled-past-hero');
        } else {
          topHeader.classList.remove('scrolled-past-hero');
          document.body.classList.remove('scrolled-past-hero');
        }

        isTicking = false;
      }

      window.addEventListener('scroll', () => {
        if (!isTicking) {
          window.requestAnimationFrame(onScroll);
          isTicking = true;
        }
      }, { passive: true });

      // Run once on initial load
      onScroll();
    }

    initCinematicScroll();
    loadChaptersIndex();

    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(reg => reg.update()).catch(() => {});
      });
    }
})();
