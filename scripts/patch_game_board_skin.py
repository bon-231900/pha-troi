# -*- coding: utf-8 -*-
"""
Script to revamp the board/panel container in App.tsx and RightProgressionPanel.tsx
Transforming it from a web admin drawer into an authentic Xianxia Game Board.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# -------------------------------------------------------------------------
# 1. PATCH App.tsx (Board Shell, 4 Corners, Plaque Header, Jade Seal Close)
# -------------------------------------------------------------------------
APP_FILE = r'frontend\src\App.tsx'

with open(APP_FILE, 'r', encoding='utf-8') as f:
    app_code = f.read()

target_app_drawer = """      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG */}
      <div
        className={`fixed inset-y-0 right-0 z-40 w-full sm:w-[400px] md:w-[440px] bg-slate-950/95 border-l border-amber-500/30 backdrop-blur-xl shadow-2xl transform transition-transform duration-300 ease-in-out flex flex-col pt-safe pb-safe ${
          rightPanelOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/80">
          <div className="flex items-center gap-2 text-amber-300 font-tech font-bold text-sm">
            <Hammer className="w-4 h-4 text-amber-400" />
            <span>LÒ RÈN, VŨ KHÍ & KỸ PHÁP</span>
          </div>
          <button
            type="button"
            onClick={() => setRightPanelOpen(false)}
            className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-100 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">"""

replacement_app_drawer = """      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG - CELESTIAL STELE BOARD */}
      <div
        className={`fixed inset-y-0 right-0 z-40 w-full sm:w-[420px] md:w-[460px] border-l-2 border-amber-500/60 shadow-[-12px_0_40px_rgba(245,158,11,0.25)] transform transition-transform duration-300 ease-in-out flex flex-col pt-safe pb-safe select-none ${
          rightPanelOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
        style={{
          backgroundImage: "linear-gradient(to bottom, rgba(10, 14, 26, 0.96), rgba(6, 8, 16, 0.98)), url('/assets/art/ui/arsenal/board_forge_texture.webp')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* 4 Corner Antique Dragon Filigree Brackets */}
        <img
          src="/assets/art/ui/arsenal/board_corner_bracket.webp"
          alt=""
          className="absolute top-0 left-0 w-9 h-9 pointer-events-none z-20 opacity-85 drop-shadow"
        />
        <img
          src="/assets/art/ui/arsenal/board_corner_bracket.webp"
          alt=""
          className="absolute top-0 right-0 w-9 h-9 pointer-events-none z-20 opacity-85 drop-shadow -scale-x-100"
        />
        <img
          src="/assets/art/ui/arsenal/board_corner_bracket.webp"
          alt=""
          className="absolute bottom-0 left-0 w-9 h-9 pointer-events-none z-20 opacity-85 drop-shadow -scale-y-100"
        />
        <img
          src="/assets/art/ui/arsenal/board_corner_bracket.webp"
          alt=""
          className="absolute bottom-0 right-0 w-9 h-9 pointer-events-none z-20 opacity-85 drop-shadow -scale-x-100 -scale-y-100"
        />

        {/* Sculpted Celestial Plaque Header Banner */}
        <div className="relative px-3.5 py-3 border-b border-amber-500/40 bg-gradient-to-r from-amber-950/60 via-[#0B1020] to-amber-950/60 shadow-lg flex items-center justify-between shrink-0 overflow-hidden">
          {/* Subtle Plaque Backdrop Watermark */}
          <div className="absolute inset-0 flex items-center justify-center opacity-25 pointer-events-none">
            <img
              src="/assets/art/ui/arsenal/board_header_plaque.webp"
              alt=""
              className="h-16 w-auto object-contain max-w-full"
            />
          </div>

          <div className="flex items-center gap-2.5 relative z-10">
            <div className="w-8 h-8 rounded-lg bg-black/90 border border-amber-400/60 p-1 flex items-center justify-center shadow-inner">
              <img src="/assets/art/items/item_hammer_celestial.webp" alt="" className="w-full h-full object-contain drop-shadow" />
            </div>
            <div>
              <div className="text-amber-300 font-tech font-bold text-sm tracking-wider flex items-center gap-1.5 drop-shadow">
                <span>LÒ RÈN, VŨ KHÍ & KỸ PHÁP</span>
              </div>
              <div className="text-[9px] text-amber-400/70 font-tech tracking-widest uppercase">
                THIÊN CỔ BẢN MỆNH BẢNG · MMORPG
              </div>
            </div>
          </div>

          {/* Antique Daoist Jade Bagua Seal Close Button */}
          <button
            type="button"
            onClick={() => setRightPanelOpen(false)}
            title="Đóng Bảng Thần Khí [ESC]"
            className="w-8 h-8 rounded-full border border-amber-500/50 hover:border-amber-400 bg-black/80 hover:bg-amber-950/60 p-0.5 flex items-center justify-center shadow-lg transition-all hover:scale-110 active:scale-95 cursor-pointer relative z-10 group"
          >
            <img
              src="/assets/art/ui/arsenal/board_close_seal.webp"
              alt="Đóng"
              className="w-full h-full object-contain drop-shadow group-hover:rotate-90 transition-transform duration-300"
            />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2 py-2">"""

if target_app_drawer in app_code:
    app_code = app_code.replace(target_app_drawer, replacement_app_drawer)
    with open(APP_FILE, 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("[+] App.tsx Board Shell successfully replaced!")
else:
    print("[-] App.tsx target not found")

# -------------------------------------------------------------------------
# 2. PATCH RightProgressionPanel.tsx (Add Daoist Filigree Dividers)
# -------------------------------------------------------------------------
PANEL_FILE = r'frontend\src\components\RightProgressionPanel.tsx'

with open(PANEL_FILE, 'r', encoding='utf-8') as f:
    panel_code = f.read()

# Replace plain text separator before Ancient Rune Pouch
old_rune_sep = """            {/* 4. TÚI PHÙ THẠCH THƯỢNG CỔ (ANCIENT RUNE GEM POUCH) */}
            <div className="pt-2 border-t border-slate-800 space-y-2">"""

new_rune_sep = """            {/* 4. TÚI PHÙ THẠCH THƯỢNG CỔ (ANCIENT RUNE GEM POUCH) */}
            <div className="pt-1 space-y-2">
              {/* Daoist Filigree Divider */}
              <div className="flex items-center justify-center my-1.5 opacity-85 pointer-events-none">
                <img
                  src="/assets/art/ui/arsenal/board_divider_filigree.webp"
                  alt=""
                  className="w-full max-w-[340px] h-3.5 object-contain"
                />
              </div>"""

if old_rune_sep in panel_code:
    panel_code = panel_code.replace(old_rune_sep, new_rune_sep)
    print("[+] Replaced plain border with Daoist Filigree Divider before Rune Pouch")

# Replace separator before 6 Relics matrix
old_relic_sep = """            {/* 2. LỤC ĐẠI BẢN MỆNH THẦN KHÍ (6 Fixed Equipment Slots) */}
            <div>"""

new_relic_sep = """            {/* 2. LỤC ĐẠI BẢN MỆNH THẦN KHÍ (6 Fixed Equipment Slots) */}
            <div>
              {/* Daoist Filigree Divider */}
              <div className="flex items-center justify-center my-1.5 opacity-85 pointer-events-none">
                <img
                  src="/assets/art/ui/arsenal/board_divider_filigree.webp"
                  alt=""
                  className="w-full max-w-[340px] h-3.5 object-contain"
                />
              </div>"""

if old_relic_sep in panel_code:
    panel_code = panel_code.replace(old_relic_sep, new_relic_sep)
    print("[+] Replaced separator before 6 Relics Matrix")

with open(PANEL_FILE, 'w', encoding='utf-8') as f:
    panel_code = panel_code.replace(old_relic_sep, new_relic_sep)
    f.write(panel_code)

print("[SUCCESS] Board Skinning Script Completed!")
