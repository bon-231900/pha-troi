# -*- coding: utf-8 -*-
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Patch ClassSkillBar.tsx: remove "Đổi Phái" button
with open('frontend/src/components/ClassSkillBar.tsx', 'r', encoding='utf-8') as f:
    bar_code = f.read()

old_button = """        {onOpenClassSelect && (
          <button
            type="button"
            onClick={onOpenClassSelect}
            className="text-[9px] text-cyan-400 hover:text-cyan-300 hover:underline cursor-pointer ml-2 whitespace-nowrap"
            title="Đổi hệ phái hoặc khởi tạo lại căn cơ"
          >
            Đổi Phái
          </button>
        )}"""

if old_button in bar_code:
    bar_code = bar_code.replace(old_button, "")
    with open('frontend/src/components/ClassSkillBar.tsx', 'w', encoding='utf-8') as f:
        f.write(bar_code)
    print("1. Removed Doi Phai from ClassSkillBar.tsx")
else:
    print("1. ClassSkillBar already patched")

# 2. Patch TopBossHeader.tsx: turn class button into static non-clickable badge
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    header_code = f.read()

old_header_btn = """        {/* Player Class / Sect Commitment Badge */}
        {playerClass && (
          <button
            type="button"
            onClick={onOpenClassModal}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-tech font-bold shadow-md border cursor-pointer transition-all hover:scale-105 active:scale-95 ${playerClass.badgeBg}`}
            title={`${playerClass.name} - ${playerClass.sectTitle} (Nhấn để xem kỹ năng hoặc đổi phái)`}
          >
            <span>{playerClass.icon}</span>
            <span className="hidden md:inline font-bold">{playerClass.name}</span>
          </button>
        )}"""

new_header_badge = """        {/* Player Class / Sect Commitment Badge (Co dinh can co - Khong cho doi phai) */}
        {playerClass && (
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-tech font-bold shadow-md border select-none ${playerClass.badgeBg}`}
            title={`Hệ Phái: ${playerClass.name} - ${playerClass.sectTitle} (Độc Nhất Căn Cơ)`}
          >
            <span>{playerClass.icon}</span>
            <span className="hidden md:inline font-bold">{playerClass.name}</span>
          </div>
        )}"""

if old_header_btn in header_code:
    header_code = header_code.replace(old_header_btn, new_header_badge)
    with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
        f.write(header_code)
    print("2. Changed class button to static badge in TopBossHeader.tsx")
else:
    print("2. TopBossHeader already patched")

# 3. Patch RightProgressionPanel.tsx: remove "Đổi Phái ↺" button
with open('frontend/src/components/RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    panel_code = f.read()

old_panel_btn = """                  {onOpenClassModal && (
                    <button
                      type="button"
                      onClick={onOpenClassModal}
                      className="px-2.5 py-1 rounded-lg text-[10px] font-tech font-bold bg-slate-900/90 hover:bg-slate-800 border border-amber-500/40 text-amber-300 transition-colors cursor-pointer"
                      title="Xem chi tiết 4 kỹ năng hoặc chuyển đổi Hệ Phái"
                    >
                      Đổi Phái ↺
                    </button>
                  )}"""

new_panel_tag = """                  <span className="px-2 py-0.5 rounded text-[10px] font-tech font-bold bg-slate-900/90 border border-amber-500/30 text-amber-300/90 select-none">
                    Độc Nhất Căn Cơ
                  </span>"""

if old_panel_btn in panel_code:
    panel_code = panel_code.replace(old_panel_btn, new_panel_tag)
    with open('frontend/src/components/RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
        f.write(panel_code)
    print("3. Removed Doi Phai from RightProgressionPanel.tsx")
else:
    print("3. RightProgressionPanel already patched")

# 4. Patch App.tsx: ensure modal only opens if !playerClassId
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_code = f.read()

old_app_modal = """      {/* 4. Character Creation & Single-Class Commitment Modal */}
      {(showClassModal || (!playerClassId && gameState === 'playing')) && (
        <CharacterCreationModal
          currentClassId={playerClassId}
          currentName={playerName}
          isInitialCreation={!playerClassId}
          onConfirm={handleCommitClass}
          onCancel={() => setShowClassModal(false)}
        />
      )}"""

new_app_modal = """      {/* 4. Character Creation & Single-Class Commitment Modal (Chỉ xuất hiện khi chưa chọn phái) */}
      {(!playerClassId && gameState === 'playing') && (
        <CharacterCreationModal
          currentClassId={playerClassId}
          currentName={playerName}
          isInitialCreation={true}
          onConfirm={handleCommitClass}
        />
      )}"""

if old_app_modal in app_code:
    app_code = app_code.replace(old_app_modal, new_app_modal)
    with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("4. Locked CharacterCreationModal strictly to new characters in App.tsx")
else:
    print("4. App.tsx already patched")

print("All Doi Phai elements successfully purged!")
