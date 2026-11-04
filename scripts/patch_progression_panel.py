# -*- coding: utf-8 -*-
with open('frontend/src/components/RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add PlayerClassMeta to import
old_import = """  ascendEquipmentTier,
} from '../game/rules';"""

new_import = """  ascendEquipmentTier,
  PlayerClassMeta,
} from '../game/rules';"""

code = code.replace(old_import, new_import, 1)

# 2. Add playerClass and onOpenClassModal to props interface
old_props = """  autoSalvageTiers?: { tierE: boolean; tierD: boolean; tierC: boolean };
  onToggleAutoSalvage?: (tierKey: 'tierE' | 'tierD' | 'tierC') => void;
}"""

new_props = """  autoSalvageTiers?: { tierE: boolean; tierD: boolean; tierC: boolean };
  onToggleAutoSalvage?: (tierKey: 'tierE' | 'tierD' | 'tierC') => void;
  playerClass?: PlayerClassMeta;
  onOpenClassModal?: () => void;
}"""

code = code.replace(old_props, new_props, 1)

# 3. Add to function parameters
old_params = """  autoSalvageTiers = { tierE: false, tierD: false, tierC: false },
  onToggleAutoSalvage,"""

# Let's check how onToggleAutoSalvage is destructured
old_destruct = """  onToggleAutoSalvage,
}) => {"""

new_destruct = """  onToggleAutoSalvage,
  playerClass,
  onOpenClassModal,
}) => {"""

code = code.replace(old_destruct, new_destruct, 1)

# 4. Insert Sect card before Stance selector in tab spirit
target_stance = """            {/* 2. STANCE SELECTOR TABS (Q, W, E, R) */}"""
sect_card = """            {/* 2A. BẢN SẮC CĂN CƠ · HỆ PHÁI ĐÃ CHỌN CARD */}
            {playerClass && (
              <div
                className="p-3 rounded-xl border flex flex-col gap-2.5 transition-all shadow-lg"
                style={{
                  backgroundColor: `${playerClass.color}15`,
                  borderColor: `${playerClass.color}50`,
                }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{playerClass.icon}</span>
                    <div>
                      <h4 className="text-xs font-bold font-tech text-amber-300">
                        {playerClass.name} · {playerClass.sectTitle}
                      </h4>
                      <div className="text-[10px] text-slate-400">
                        {playerClass.role} ({playerClass.guildTitle})
                      </div>
                    </div>
                  </div>
                  {onOpenClassModal && (
                    <button
                      type="button"
                      onClick={onOpenClassModal}
                      className="px-2.5 py-1 rounded-lg text-[10px] font-tech font-bold bg-slate-900/90 hover:bg-slate-800 border border-amber-500/40 text-amber-300 transition-colors cursor-pointer"
                      title="Xem chi tiết 4 kỹ năng hoặc chuyển đổi Hệ Phái"
                    >
                      Đổi Phái ↺
                    </button>
                  )}
                </div>

                {/* 4 Class Skills Q W E R Mini Preview */}
                <div className="grid grid-cols-4 gap-1 font-tech">
                  {(['Q', 'W', 'E', 'R'] as const).map((slotKey) => {
                    const sk = playerClass.skills[slotKey];
                    return (
                      <div
                        key={slotKey}
                        className="p-1.5 rounded-lg bg-slate-950/80 border border-slate-800 flex flex-col items-center text-center gap-0.5"
                      >
                        <span
                          className="w-4 h-4 rounded text-[9px] font-bold flex items-center justify-center"
                          style={{ backgroundColor: playerClass.color, color: '#05070F' }}
                        >
                          {slotKey}
                        </span>
                        <span className="text-[9px] font-semibold text-slate-200 truncate w-full">
                          {sk.name}
                        </span>
                        <span className="text-[8px] text-cyan-400">
                          {slotKey === 'Q' ? 'Cấp 1' : slotKey === 'W' ? 'Cấp 40' : slotKey === 'E' ? 'Cấp 100' : 'Cấp 200'}
                        </span>
                      </div>
                    );
                  })}
                </div>

                {/* 2 Sub-Classes Preview */}
                <div className="text-[10px] font-tech text-slate-400 pt-1.5 border-t border-slate-800/80 flex items-center justify-between">
                  <span className="text-purple-300">① {playerClass.subClasses.a.name}</span>
                  <span>·</span>
                  <span className="text-emerald-300">② {playerClass.subClasses.b.name}</span>
                  <span className="text-[9px] text-slate-500">(Mở Cấp 120)</span>
                </div>
              </div>
            )}

            {/* 2. STANCE SELECTOR TABS (Q, W, E, R) */}"""

code = code.replace(target_stance, sect_card, 1)

with open('frontend/src/components/RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("RightProgressionPanel patched successfully!")
