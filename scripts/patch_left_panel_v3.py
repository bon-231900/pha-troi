# -*- coding: utf-8 -*-
"""
Script to apply Stance Weaving and Balance Patch v3.0 to LeftTacticalPanel.tsx
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'd:\tieu-thuyet\frontend\src\components\LeftTacticalPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add stanceWeave to LeftTacticalPanelProps
old_props = """  guildHearths?: Record<string, { level: number; exp: number }>;
  onDonateHearth?: (guildId: string, amount: number) => void;
  linhThach?: number;
}"""

new_props = """  guildHearths?: Record<string, { level: number; exp: number }>;
  onDonateHearth?: (guildId: string, amount: number) => void;
  linhThach?: number;
  stanceWeave?: { previousStance: StanceKey; timeLeftSec: number } | null;
}"""

c = c.replace(old_props, new_props)

# 2. Destructure stanceWeave
old_destruct = """  guildHearths = {},
  onDonateHearth,
  linhThach = 0,
}) => {"""

new_destruct = """  guildHearths = {},
  onDonateHearth,
  linhThach = 0,
  stanceWeave,
}) => {"""

c = c.replace(old_destruct, new_destruct)

# 3. Add Stance Weaving Banner in Tactical Tab
old_stance_card = """            <div className="p-2.5 rounded-lg bg-[#111625] border border-slate-800/80 mb-2.5">
              <div className="text-[11px] text-slate-400 mb-0.5">Thế Búa Đang Vận Dụng</div>"""

new_stance_card = """            {stanceWeave && (
              <div className="mb-2.5 p-2 rounded-lg bg-amber-500/15 border border-amber-400/40 flex items-center justify-between animate-pulse">
                <div className="flex items-center gap-1.5">
                  <span className="text-amber-300 font-bold text-xs">✦ CHUYỂN THẾ:</span>
                  <span className="text-[11px] text-amber-100">Kế thừa 50% uy lực [{stanceWeave.previousStance}]</span>
                </div>
                <span className="px-2 py-0.5 rounded-full bg-amber-400 text-slate-950 font-bold text-xs font-mono">
                  {stanceWeave.timeLeftSec}s
                </span>
              </div>
            )}

            <div className="p-2.5 rounded-lg bg-[#111625] border border-slate-800/80 mb-2.5">
              <div className="text-[11px] text-slate-400 mb-0.5">Thế Búa Đang Vận Dụng</div>"""

c = c.replace(old_stance_card, new_stance_card)

with open(r'd:\tieu-thuyet\frontend\src\components\LeftTacticalPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("LeftTacticalPanel.tsx đã được nâng cấp Stance Weaving thành công!")
