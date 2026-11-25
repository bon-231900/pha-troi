with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add onOpenGuide to interface
target1 = '''  onPause: () => void;
  onTriggerGlobalBurst: () => void;'''
replacement1 = '''  onPause: () => void;
  onOpenGuide?: () => void;
  onTriggerGlobalBurst: () => void;'''

# 2. Add onOpenGuide to destructured props
target2 = '''  onPause,
  onTriggerGlobalBurst,'''
replacement2 = '''  onPause,
  onOpenGuide,
  onTriggerGlobalBurst,'''

# 3. Mobile button next to pause
target3 = '''            <button
              type="button"
              onClick={onPause}
              className="p-1.5 rounded-lg bg-slate-900/90 border border-amber-500/30 text-amber-300 hover:border-amber-400 cursor-pointer active:scale-95 shadow-md"
              title="Tạm Dừng Lò Rèn & Cài Đặt (Đổi Tu Sĩ, Tắt/Bật Âm) [Phím ESC]"
            >
              <img
                src={HEADER_ICON_ASSETS.pauseTalisman}
                alt="Tạm Dừng"
                className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#F59E0B]"
              />
            </button>'''

replacement3 = '''            {onOpenGuide && (
              <button
                type="button"
                onClick={onOpenGuide}
                className="p-1.5 rounded-lg bg-slate-900/90 border border-cyan-500/40 text-cyan-300 hover:border-cyan-400 cursor-pointer active:scale-95 shadow-md"
                title="Cẩm Nang Quy Tắc Rèn Đúc & Chỉ Dẫn [?]"
              >
                <span className="w-4 h-4 flex items-center justify-center font-bold text-xs text-cyan-300">?</span>
              </button>
            )}

            <button
              type="button"
              onClick={onPause}
              className="p-1.5 rounded-lg bg-slate-900/90 border border-amber-500/30 text-amber-300 hover:border-amber-400 cursor-pointer active:scale-95 shadow-md"
              title="Tạm Dừng Lò Rèn & Cài Đặt (Đổi Tu Sĩ, Tắt/Bật Âm) [Phím ESC]"
            >
              <img
                src={HEADER_ICON_ASSETS.pauseTalisman}
                alt="Tạm Dừng"
                className="w-4 h-4 object-contain filter drop-shadow-[0_0_4px_#F59E0B]"
              />
            </button>'''

# 4. Desktop button next to pause
target4 = '''          {/* Pause Modal Trigger Token Button [ESC / P] */}
          <button
            type="button"
            onClick={onPause}'''

replacement4 = '''          {/* Guide Help Trigger Button */}
          {onOpenGuide && (
            <button
              type="button"
              onClick={onOpenGuide}
              className="relative flex items-center gap-1.5 px-3 py-2 rounded-xl select-none cursor-pointer group transition-all hover:brightness-125 active:scale-95 shadow-md overflow-hidden text-xs font-tech font-bold"
              title="Cẩm Nang Quy Tắc Rèn Đúc & Chỉ Dẫn Nhập Môn"
            >
              <img
                src={HEADER_FRAME_ASSETS.tokenIdle}
                alt="Frame"
                className="absolute inset-0 w-full h-full object-fill pointer-events-none drop-shadow"
              />
              <span className="relative z-10 w-4 h-4 flex items-center justify-center font-extrabold text-cyan-300 rounded-full bg-cyan-950/80 border border-cyan-400/60 shadow-[0_0_8px_rgba(6,182,212,0.6)] group-hover:scale-110 transition-transform">
                ?
              </span>
              <span className="relative z-10 text-cyan-200 tracking-wider hidden sm:inline drop-shadow">
                Chỉ Dẫn
              </span>
            </button>
          )}

          {/* Pause Modal Trigger Token Button [ESC / P] */}
          <button
            type="button"
            onClick={onPause}'''

assert target1 in c, 'Target 1 not found'
assert target2 in c, 'Target 2 not found'
assert target3 in c, 'Target 3 not found'
assert target4 in c, 'Target 4 not found'

c = c.replace(target1, replacement1, 1)
c = c.replace(target2, replacement2, 1)
c = c.replace(target3, replacement3, 1)
c = c.replace(target4, replacement4, 1)

with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated TopBossHeader.tsx successfully!')
