# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Update arsenalArtAssets.ts to use relative './assets/...'
with open(r'frontend\src\game\arsenalArtAssets.ts', 'r', encoding='utf-8') as f:
    art_code = f.read()

art_code = art_code.replace("'/assets/", "'./assets/")
with open(r'frontend\src\game\arsenalArtAssets.ts', 'w', encoding='utf-8') as f:
    f.write(art_code)
print("[+] arsenalArtAssets.ts paths converted to relative './assets/...'")

# 2. Update RightProgressionPanel.tsx to use relative './assets/...'
with open(r'frontend\src\components\RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    panel_code = f.read()

panel_code = panel_code.replace("'/assets/", "'./assets/")
panel_code = panel_code.replace('"/assets/', '"./assets/')

with open(r'frontend\src\components\RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(panel_code)
print("[+] RightProgressionPanel.tsx paths converted to relative './assets/...'")

# 3. Mount board header plaque, corner brackets, and close seal in App.tsx
with open(r'frontend\src\App.tsx', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Replace the drawer section in App.tsx
old_drawer_start = "      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG - CELESTIAL STELE BOARD */}"
new_drawer_block = """      {/* 5. SLIDE-OUT DRAWER 2 (RIGHT): NÂNG CẤP, THẦN HỒN & BẢNG VÀNG - CELESTIAL STELE BOARD */}
      <div
        className={`fixed inset-y-0 right-0 z-40 w-full sm:w-[420px] md:w-[460px] border-l-2 border-amber-500/70 shadow-[-16px_0_50px_rgba(245,158,11,0.3)] transform transition-transform duration-300 ease-in-out flex flex-col pt-safe pb-safe select-none ${
          rightPanelOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
        style={{
          backgroundImage: "linear-gradient(to bottom, rgba(8, 11, 20, 0.94), rgba(5, 7, 14, 0.97)), url('./assets/art/ui/arsenal/board_forge_texture.webp')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* 4 Corner Antique Dragon Filigree Brackets */}
        <div className="absolute top-0 left-0 w-11 h-11 pointer-events-none z-30 opacity-90 drop-shadow">
          <img
            src="./assets/art/ui/arsenal/board_corner_bracket.webp"
            alt=""
            className="w-full h-full object-contain"
          />
        </div>
        <div className="absolute top-0 right-0 w-11 h-11 pointer-events-none z-30 opacity-90 drop-shadow">
          <img
            src="./assets/art/ui/arsenal/board_corner_bracket.webp"
            alt=""
            className="w-full h-full object-contain -scale-x-100"
          />
        </div>
        <div className="absolute bottom-0 left-0 w-11 h-11 pointer-events-none z-30 opacity-90 drop-shadow">
          <img
            src="./assets/art/ui/arsenal/board_corner_bracket.webp"
            alt=""
            className="w-full h-full object-contain -scale-y-100"
          />
        </div>
        <div className="absolute bottom-0 right-0 w-11 h-11 pointer-events-none z-30 opacity-90 drop-shadow">
          <img
            src="./assets/art/ui/arsenal/board_corner_bracket.webp"
            alt=""
            className="w-full h-full object-contain -scale-x-100 -scale-y-100"
          />
        </div>

        {/* Sculpted Celestial Plaque Header Banner */}
        <div className="relative pt-3 pb-2.5 px-3 border-b-2 border-amber-500/50 bg-gradient-to-b from-[#141C33]/90 via-[#0B1020]/95 to-[#070A14] shadow-xl flex items-center justify-between shrink-0 overflow-hidden">
          {/* Ornate Plaque Arch Frame Banner across Header */}
          <div className="absolute inset-0 flex items-center justify-center opacity-40 pointer-events-none">
            <img
              src="./assets/art/ui/arsenal/board_header_plaque.webp"
              alt=""
              className="w-full h-full object-cover scale-110"
            />
          </div>

          <div className="flex items-center gap-2.5 relative z-10 pl-2">
            <div className="w-9 h-9 rounded-xl bg-black/95 border-2 border-amber-400/80 p-1 flex items-center justify-center shadow-lg shadow-amber-500/20 relative group">
              <img
                src="./assets/art/items/item_hammer_celestial.webp"
                alt="Thần Chùy"
                className="w-full h-full object-contain drop-shadow group-hover:scale-110 transition-transform"
              />
            </div>
            <div>
              <div className="text-amber-300 font-tech font-extrabold text-sm sm:text-base tracking-wider flex items-center gap-1.5 drop-shadow-[0_2px_8px_rgba(245,158,11,0.5)]">
                <span>LÒ RÈN, VŨ KHÍ & KỸ PHÁP</span>
              </div>
              <div className="text-[9.5px] text-amber-400 font-tech tracking-widest uppercase flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping inline-block" />
                <span>THIÊN CỔ BẢN MỆNH BẢNG · MMORPG</span>
              </div>
            </div>
          </div>

          {/* Antique Daoist Jade Bagua Seal Close Button */}
          <button
            type="button"
            onClick={() => setRightPanelOpen(false)}
            title="Đóng Bảng Thần Khí [ESC]"
            className="w-9 h-9 rounded-full border-2 border-amber-400/70 hover:border-amber-300 bg-black/90 hover:bg-amber-950 p-1 flex items-center justify-center shadow-[0_0_12px_rgba(245,158,11,0.4)] transition-all hover:scale-110 active:scale-90 cursor-pointer relative z-10 mr-1 group"
          >
            <img
              src="./assets/art/ui/arsenal/board_close_seal.webp"
              alt="Đóng"
              className="w-full h-full object-contain drop-shadow group-hover:rotate-90 transition-transform duration-300"
            />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2.5 py-2.5 space-y-2">"""

# Find the start of the drawer block in App.tsx and replace until RightProgressionPanel
import re

pattern = re.compile(
    r"\{\/\* 5\. SLIDE-OUT DRAWER 2 \(RIGHT\):.*?\n.*?<div className=\"flex-1 overflow-y-auto.*?>",
    re.DOTALL
)

if pattern.search(app_code):
    app_code = pattern.sub(new_drawer_block.strip(), app_code, count=1)
    with open(r'frontend\src\App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("[+] App.tsx Header Plaque and Drawer Frame successfully mounted!")
else:
    print("[-] App.tsx pattern not found, checking fallback...")
