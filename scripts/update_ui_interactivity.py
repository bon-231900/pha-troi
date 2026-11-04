import os

# 1. Update TopBossHeader.tsx
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    tbh = f.read()

tbh = tbh.replace(
    '  playerClass?: PlayerClassMeta;\n}',
    '  playerClass?: PlayerClassMeta;\n  onSwitchCharacter?: () => void;\n}'
)
tbh = tbh.replace(
    '  playerClass,\n}) => {',
    '  playerClass,\n  onSwitchCharacter,\n}) => {'
)

old_badge = """        {/* Player Class / Sect Commitment Badge (Co dinh can co - Khong cho doi phai) */}
        {playerClass && (
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-tech font-bold shadow-md border select-none ${playerClass.badgeBg}`}
            title={`Hệ Phái: ${playerClass.name} - ${playerClass.sectTitle} (Độc Nhất Căn Cơ)`}
          >
            <span>{playerClass.icon}</span>
            <span className="hidden md:inline font-bold">{playerClass.name}</span>
          </div>
        )}"""

new_badge = """        {/* Player Class / Sect Commitment Badge -> Clickable to Switch Characters (3 Slots) */}
        {playerClass && (
          <button
            type="button"
            onClick={onSwitchCharacter}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-xs font-tech font-bold shadow-lg border cursor-pointer hover:brightness-125 transition-all active:scale-95 ${playerClass.badgeBg}`}
            title="Bấm để Đổi Tu Sĩ / Quản lý 3 Slot & Trải nghiệm Bệ Đá Bát Quái Nện Thử Búa"
          >
            <span>{playerClass.icon}</span>
            <span className="font-bold">{playerClass.name}</span>
            <span className="text-[10px] text-amber-300 ml-1 border-l border-amber-500/40 pl-1.5 font-bold">
              ĐỔI TU SĨ ▾
            </span>
          </button>
        )}"""

tbh = tbh.replace(old_badge, new_badge)

with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
    f.write(tbh)
print("Updated TopBossHeader.tsx")

# 2. Update ClassSkillBar.tsx
with open('frontend/src/components/ClassSkillBar.tsx', 'r', encoding='utf-8') as f:
    csb = f.read()

csb = csb.replace(
    '  onCastSkill: (slotKey: \'W\' | \'E\' | \'R\') => void;\n  hudVisible?: boolean;\n}',
    '  onCastSkill: (slotKey: \'W\' | \'E\' | \'R\') => void;\n  onHeroStrike?: () => void;\n  hudVisible?: boolean;\n}'
)
csb = csb.replace(
    '  onCastSkill,\n  hudVisible = true,\n}) => {',
    '  onCastSkill,\n  onHeroStrike,\n  hudVisible = true,\n}) => {'
)

old_q = """        {/* SKILL [Q]: Core Rhythm Stance (Always active) */}
        <div
          className="relative p-1.5 sm:p-2 rounded-xl bg-slate-900/90 border border-amber-400/80 shadow-md flex flex-col items-center justify-between text-center select-none"
          title={`[Q] ${playerClass.skills.Q.name}: ${playerClass.skills.Q.description}`}
        >
          <div className="w-full flex items-center justify-between text-[9px] font-tech text-amber-300">
            <span className="font-bold bg-amber-400/20 px-1 rounded">Q</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>

          <div className="my-0.5 text-base sm:text-lg">
            {playerClass.skills.Q.icon}
          </div>

          <div className="w-full">
            <div className="text-[10px] sm:text-[11px] font-tech font-bold text-slate-100 truncate">
              {playerClass.skills.Q.name.split(' ')[0]}
            </div>
            <div className="text-[8px] text-emerald-400 font-tech uppercase truncate">
              Gõ Đe
            </div>
          </div>
        </div>"""

new_q = """        {/* SKILL [Q]: Core Rhythm Stance (Clickable button to strike anvil!) */}
        <button
          type="button"
          onClick={onHeroStrike}
          className="relative p-1.5 sm:p-2 rounded-xl bg-slate-900/90 border border-amber-400/80 shadow-md flex flex-col items-center justify-between text-center select-none cursor-pointer hover:border-amber-300 hover:brightness-125 active:scale-95 transition-all"
          title={`[Q] ${playerClass.skills.Q.name}: Bấm hoặc nhấn SPACE để gõ đe`}
        >
          <div className="w-full flex items-center justify-between text-[9px] font-tech text-amber-300">
            <span className="font-bold bg-amber-400/20 px-1 rounded">Q / SPACE</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>

          <div className="my-0.5 text-base sm:text-lg">
            {playerClass.skills.Q.icon}
          </div>

          <div className="w-full">
            <div className="text-[10px] sm:text-[11px] font-tech font-bold text-slate-100 truncate">
              {playerClass.skills.Q.name.split(' ')[0]}
            </div>
            <div className="text-[8px] text-emerald-400 font-tech uppercase truncate font-bold">
              Gõ Đe ⚡
            </div>
          </div>
        </button>"""

csb = csb.replace(old_q, new_q)

with open('frontend/src/components/ClassSkillBar.tsx', 'w', encoding='utf-8') as f:
    f.write(csb)
print("Updated ClassSkillBar.tsx")

# 3. Update App.tsx
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Pass onHeroStrike to ClassSkillBar
app = app.replace(
    '        onCastSkill={handleCastClassSkill}\n        hudVisible={hudVisible}\n      />',
    '        onCastSkill={handleCastClassSkill}\n        onHeroStrike={() => handleHeroStrike(false)}\n        hudVisible={hudVisible}\n      />'
)

# Pass onSwitchCharacter to TopBossHeader
app = app.replace(
    '        playerClass={getPlayerClass(playerClassId || \'thunder\')}\n      />',
    '        playerClass={getPlayerClass(playerClassId || \'thunder\')}\n        onSwitchCharacter={() => setGameState(\'character_select\')}\n      />'
)

# Unlock audio in handleHeroStrike
app = app.replace(
    '  const handleHeroStrike = useCallback(\n    (forceGolden = false) => {\n      if (gameState !== \'playing\') {',
    '  const handleHeroStrike = useCallback(\n    (forceGolden = false) => {\n      soundEngine.unlockAudio();\n      if (gameState !== \'playing\') {'
)

# Add [ĐỔI TU SĨ] button in bottom-right dock next to NỆN BÚA
old_dock = """        {hudVisible && (
          <button
            type="button"
            onClick={() => handleHeroStrike(false)}
            className="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-gradient-to-r from-amber-500/20 via-orange-500/20 to-amber-500/20 hover:from-amber-500/30 hover:to-amber-500/30 border border-amber-500/50 text-xs sm:text-sm font-tech font-bold text-amber-300 tracking-wider shadow-lg hover:border-amber-400 transition-all cursor-pointer active:scale-95 whitespace-nowrap"
          >
            NỆN BÚA [SPACE]
          </button>
        )}"""

new_dock = """        {hudVisible && (
          <>
            <button
              type="button"
              onClick={() => setGameState('character_select')}
              className="px-3 py-2 sm:px-4 sm:py-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-amber-500/40 text-xs sm:text-sm font-tech font-bold text-amber-300 tracking-wider shadow-lg hover:border-amber-400 transition-all cursor-pointer active:scale-95 whitespace-nowrap flex items-center gap-1.5"
              title="Đổi Nhân Vật (3 Slots) & Vào Bệ Đá Bát Quái"
            >
              <span>⚡ ĐỔI TU SĨ (3 SLOTS)</span>
            </button>

            <button
              type="button"
              onClick={() => handleHeroStrike(false)}
              className="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-gradient-to-r from-amber-500/20 via-orange-500/20 to-amber-500/20 hover:from-amber-500/30 hover:to-amber-500/30 border border-amber-500/50 text-xs sm:text-sm font-tech font-bold text-amber-300 tracking-wider shadow-lg hover:border-amber-400 transition-all cursor-pointer active:scale-95 whitespace-nowrap"
            >
              NỆN BÚA [SPACE]
            </button>
          </>
        )}"""

app = app.replace(old_dock, new_dock)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)
print("Updated App.tsx")
