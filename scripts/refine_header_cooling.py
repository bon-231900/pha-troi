# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Update TopBossHeader.tsx
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    tbh = f.read()

target_tbh = """          <span className="flex items-center gap-1" title="Độ bền Đại Đe Thần (HP)">
            <img src={HEADER_ICON_ASSETS.greatAnvil} alt="Đe" className="w-3 h-3 object-contain shrink-0" />
            Độ Bền Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{Math.round((serverAnvilHp / serverAnvilMaxHp) * 100)}%</b>
          </span>"""

repl_tbh = """          <span className="flex items-center gap-1 shrink-0" title={`Độ Bền Đại Đe Thần: ${serverAnvilHp.toLocaleString('en-US')}/${serverAnvilMaxHp.toLocaleString('en-US')} HP (${Math.round((serverAnvilHp / serverAnvilMaxHp) * 100)}%). Vỡ đe = Toàn server thất bại (Wipe)!`}>
            <img src={HEADER_ICON_ASSETS.greatAnvil} alt="Đe" className="w-3 h-3 object-contain shrink-0" />
            <span>Độ Bền Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{Math.round((serverAnvilHp / serverAnvilMaxHp) * 100)}%</b></span>
            <div className="w-6 h-1 rounded-full bg-slate-900 border border-slate-700 overflow-hidden shrink-0 hidden xs:block">
              <div
                className={`h-full transition-all duration-300 ${serverAnvilHp < 2500 ? 'bg-red-500' : serverAnvilHp < 5000 ? 'bg-amber-400' : 'bg-emerald-400'}`}
                style={{ width: `${Math.min(100, Math.max(0, (serverAnvilHp / serverAnvilMaxHp) * 100))}%` }}
              />
            </div>
          </span>"""

if target_tbh in tbh:
    tbh = tbh.replace(target_tbh, repl_tbh, 1)
    with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
        f.write(tbh)
    print("Updated TopBossHeader mobile row 3 with mini bar.")
else:
    print("Warning: target_tbh not found in TopBossHeader!")

# 2. Update App.tsx
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Default furnace state on fresh load
app = app.replace(
    "    return 1500;\n  });\n\n  const [serverAnvilHp",
    "    return 600;\n  });\n\n  const [serverAnvilHp",
    1
)

# Reset furnace heat to ambientFloor on vault change
app = app.replace(
    "    setServerFurnaceHeat(vault.meltingThreshold);\n    setServerAnvilHp(10000);",
    "    setServerFurnaceHeat(Math.round(vault.meltingThreshold * 0.4));\n    setServerAnvilHp(10000);",
    1
)

# Enhanced tiered cooling speed
old_cooling = """        let decayAmount = 10;
        if (prev > 3000) {
          decayAmount = 35;
        } else if (prev > vault.meltingThreshold) {
          decayAmount = 20;
        }"""

new_cooling = """        let decayAmount = 10;
        if (prev > 6000) {
          decayAmount = 80;
        } else if (prev > 3000) {
          decayAmount = 40;
        } else if (prev > vault.meltingThreshold) {
          decayAmount = 20;
        }"""

if old_cooling in app:
    app = app.replace(old_cooling, new_cooling, 1)
    print("Enhanced tiered cooling speed in App.tsx.")
else:
    print("Warning: old_cooling not found in App.tsx!")

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("All refinements written successfully!")
