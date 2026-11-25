# -*- coding: utf-8 -*-
import os

# 1. Update TopBossHeader.tsx
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    tbh = f.read()

# Add furnaceOverheatTimeLeft to interface
tbh = tbh.replace(
    "  serverFurnaceHeat?: number; // 0 - 10,000°C\n",
    "  serverFurnaceHeat?: number; // 0 - 10,000°C\n  furnaceOverheatTimeLeft?: number; // >0 means Overheated (Chiêu R)\n"
)

# Add furnaceOverheatTimeLeft to component props destructuring
tbh = tbh.replace(
    "  serverFurnaceHeat = 1500,\n",
    "  serverFurnaceHeat = 1500,\n  furnaceOverheatTimeLeft = 0,\n"
)

# Replace Mobile Row 3 Lò & Đe display
old_mobile_row3 = """          <span className="flex items-center gap-1">
            <img src={HEADER_ICON_ASSETS.furnaceHeat} alt="Lò" className="w-3 h-3 object-contain shrink-0" />
            Lò: <b className="text-amber-300">{serverFurnaceHeat}°C</b>
          </span>
          <span className="flex items-center gap-1">
            <img src={HEADER_ICON_ASSETS.greatAnvil} alt="Đe" className="w-3 h-3 object-contain shrink-0" />
            Đe: <b className="text-emerald-300">{serverAnvilHp}</b>/10k
          </span>"""

new_mobile_row3 = """          <span className="flex items-center gap-1">
            <img src={HEADER_ICON_ASSETS.furnaceHeat} alt="Lò" className="w-3 h-3 object-contain shrink-0" />
            Lò: <b className="text-amber-300">{serverFurnaceHeat}°C</b>
            {furnaceOverheatTimeLeft > 0 ? (
              <span className="text-[8px] font-bold text-red-400 animate-pulse">🔥({Math.ceil(furnaceOverheatTimeLeft)}s)</span>
            ) : serverFurnaceHeat >= vaultMeltingThreshold ? (
              <span className="text-[8px] font-bold text-emerald-400">🔥</span>
            ) : (
              <span className="text-[8px] font-bold text-cyan-400">❄️</span>
            )}
          </span>
          <span className="flex items-center gap-1" title="Độ bền Đại Đe Thần (HP)">
            <img src={HEADER_ICON_ASSETS.greatAnvil} alt="Đe" className="w-3 h-3 object-contain shrink-0" />
            Độ Bền Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{Math.round((serverAnvilHp / serverAnvilMaxHp) * 100)}%</b>
          </span>"""

if old_mobile_row3 in tbh:
    tbh = tbh.replace(old_mobile_row3, new_mobile_row3, 1)
    print("Patched TopBossHeader mobile row 3.")
else:
    print("Warning: old_mobile_row3 not found in TopBossHeader!")

# Replace Desktop Meter 2 (Lò) & Meter 3 (Đe)
old_desktop_meters = """            {/* Meter 2: Đại Hỏa Hẩu */}
            <div className="flex items-center gap-1 shrink-0" title="Đại Hỏa Hẩu Toàn Server: Cần vượt ngưỡng để vòm trời nung chảy!">
              <img
                src={HEADER_ICON_ASSETS.furnaceHeat}
                alt="Hỏa Hẩu"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#F97316] shrink-0"
              />
              <span className="whitespace-nowrap">
                Lò: <b className="text-amber-300">{serverFurnaceHeat.toLocaleString('en-US')}°C</b>
              </span>
              {serverFurnaceHeat >= vaultMeltingThreshold ? (
                <span className="px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[8px] font-bold shrink-0">
                  🔥 Nung
                </span>
              ) : (
                <span className="px-1 py-0.2 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-[8px] font-semibold shrink-0" title={`Cần đạt ${vaultMeltingThreshold}°C`}>
                  ❄️ Đông
                </span>
              )}
            </div>

            {/* Meter 3: Độ Bền Đại Đe */}
            <div className="flex items-center gap-1 shrink-0" title="Độ Bền Đại Đe Thần Server (10,000 HP). Vỡ đe = Toàn server thất bại (Wipe) và Boss hồi 15% HP!">
              <img
                src={HEADER_ICON_ASSETS.greatAnvil}
                alt="Đại Đe"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#10B981] shrink-0"
              />
              <span className="whitespace-nowrap">
                Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{serverAnvilHp.toLocaleString('en-US')}</b>/10k
              </span>
            </div>"""

new_desktop_meters = """            {/* Meter 2: Đại Hỏa Hẩu */}
            <div className="flex items-center gap-1 shrink-0" title="Đại Hỏa Hẩu Toàn Server: Cần vượt ngưỡng để vòm trời nung chảy!">
              <img
                src={HEADER_ICON_ASSETS.furnaceHeat}
                alt="Hỏa Hẩu"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#F97316] shrink-0"
              />
              <span className="whitespace-nowrap">
                Lò: <b className="text-amber-300">{serverFurnaceHeat.toLocaleString('en-US')}°C</b>
              </span>
              {furnaceOverheatTimeLeft > 0 ? (
                <span className="px-1.5 py-0.2 rounded bg-red-500/25 text-red-300 border border-red-500/40 text-[8px] font-bold shrink-0 animate-pulse" title="Trạng thái Quá Nhiệt duy trì từ Chiêu R">
                  🔥 Quá Nhiệt ({Math.ceil(furnaceOverheatTimeLeft)}s)
                </span>
              ) : serverFurnaceHeat >= vaultMeltingThreshold ? (
                <span className="px-1 py-0.2 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[8px] font-bold shrink-0">
                  🔥 Nung
                </span>
              ) : (
                <span className="px-1 py-0.2 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-[8px] font-semibold shrink-0" title={`Cần đạt ${vaultMeltingThreshold}°C`}>
                  ❄️ Đông
                </span>
              )}
            </div>

            {/* Meter 3: Độ Bền Đại Đe */}
            <div className="flex items-center gap-1.5 shrink-0" title={`Độ Bền Đại Đe Thần: ${serverAnvilHp.toLocaleString('en-US')}/${serverAnvilMaxHp.toLocaleString('en-US')} HP (${Math.round((serverAnvilHp / serverAnvilMaxHp) * 100)}%). Vỡ đe = Toàn server thất bại (Wipe)!`}>
              <img
                src={HEADER_ICON_ASSETS.greatAnvil}
                alt="Đại Đe"
                className="w-3.5 h-3.5 object-contain filter drop-shadow-[0_0_4px_#10B981] shrink-0"
              />
              <div className="flex items-center gap-1.5">
                <span className="whitespace-nowrap">
                  Độ Bền Đe: <b className={`${serverAnvilHp < 2500 ? 'text-red-400 font-extrabold animate-pulse' : serverAnvilHp < 5000 ? 'text-amber-300' : 'text-emerald-300'}`}>{Math.round((serverAnvilHp / serverAnvilMaxHp) * 100)}%</b>
                </span>
                <div className="w-10 h-1.5 rounded-full bg-slate-900 border border-slate-700 overflow-hidden hidden sm:block">
                  <div
                    className={`h-full transition-all duration-300 ${serverAnvilHp < 2500 ? 'bg-red-500' : serverAnvilHp < 5000 ? 'bg-amber-400' : 'bg-emerald-400'}`}
                    style={{ width: `${Math.min(100, Math.max(0, (serverAnvilHp / serverAnvilMaxHp) * 100))}%` }}
                  />
                </div>
              </div>
            </div>"""

if old_desktop_meters in tbh:
    tbh = tbh.replace(old_desktop_meters, new_desktop_meters, 1)
    print("Patched TopBossHeader desktop meters.")
else:
    print("Warning: old_desktop_meters not found in TopBossHeader!")

with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
    f.write(tbh)

# 2. Update App.tsx
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Add furnaceOverheatTimeLeft state
target_app_state = """  const [skillCooldowns, setSkillCooldowns] = useState<{ W: number; E: number; R: number }>({
    W: 0,
    E: 0,
    R: 0,
  });"""

repl_app_state = """  const [skillCooldowns, setSkillCooldowns] = useState<{ W: number; E: number; R: number }>({
    W: 0,
    E: 0,
    R: 0,
  });
  const [furnaceOverheatTimeLeft, setFurnaceOverheatTimeLeft] = useState<number>(0);"""

app = app.replace(target_app_state, repl_app_state, 1)

# Decrement furnaceOverheatTimeLeft in cooldown timer
target_timer = """        return {
          W: Math.max(0, Number((prev.W - 0.2).toFixed(1))),
          E: Math.max(0, Number((prev.E - 0.2).toFixed(1))),
          R: Math.max(0, Number((prev.R - 0.2).toFixed(1))),
        };
      });
    }, 200);"""

repl_timer = """        return {
          W: Math.max(0, Number((prev.W - 0.2).toFixed(1))),
          E: Math.max(0, Number((prev.E - 0.2).toFixed(1))),
          R: Math.max(0, Number((prev.R - 0.2).toFixed(1))),
        };
      });
      setFurnaceOverheatTimeLeft((prev) => Math.max(0, Number((prev - 0.2).toFixed(1))));
    }, 200);"""

app = app.replace(target_timer, repl_timer, 1)

# Update World Raid Furnace Cooling Loop (lines 1438-1444)
old_furnace_loop = """      // 2C. World Raid: Global Server Furnace vs Celestial Chill
      const chillDelta = vault.serverChillPerSec * 0.5;
      const melterCount = Math.max(1, Math.round(activeForgersCount * 0.25));
      const melterHeat = melterCount * (2.2 + Math.random() * 1.2) * 0.5;
      const netServerHeat = melterHeat + chillDelta;
      setServerFurnaceHeat((prev) => Math.max(0, Math.min(10000, Math.round(prev + netServerHeat))));"""

new_furnace_loop = """      // 2C. World Raid: Dynamic Furnace Heat Decay & Overheat Preservation
      setServerFurnaceHeat((prev) => {
        // If Chiêu R Overheat is active, preserve furnace heat (no decay)
        if (furnaceOverheatTimeLeft > 0) {
          return prev;
        }
        
        // Ambient natural floor temperature (e.g. 600°C for Tier 1)
        const ambientFloor = Math.round(vault.meltingThreshold * 0.4);
        if (prev <= ambientFloor) {
          return Math.max(ambientFloor, prev);
        }
        
        // Dynamic natural cooling per 0.5s tick when idling/AFK:
        // - Above 3,000°C: cools by -35°C/tick (-70°C/s)
        // - Above melting threshold: cools by -20°C/tick (-40°C/s)
        // - Normal range down to ambient: cools by -10°C/tick (-20°C/s)
        let decayAmount = 10;
        if (prev > 3000) {
          decayAmount = 35;
        } else if (prev > vault.meltingThreshold) {
          decayAmount = 20;
        }
        return Math.max(ambientFloor, prev - decayAmount);
      });"""

if old_furnace_loop in app:
    app = app.replace(old_furnace_loop, new_furnace_loop, 1)
    print("Patched furnace cooling loop in App.tsx.")
else:
    print("Warning: old_furnace_loop not found in App.tsx!")

# Update Chiêu R phái Hỏa (lines 2606-2613)
old_fire_ult = """        } else if (cls.id === 'fire') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 15);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          setServerFurnaceHeat(10000);
          canvasHandleRef.current?.spawnCombatText('☀️ HỎA NGỤC ĐỒNG QUY!', `MẶT TRỜI RỰC CHÁY: -${ultDmg} DMG`, '#FF4D00', '#FFD700', true);
          appendCombatLog(`☀️ [HỎA NGỤC ĐỒNG QUY] Đại chiêu thức thứ 4! Lò Rèn bốc cháy ngút trời, khóa cứng Đại Hỏa Hẩu 10,000°C!`, 'gold');"""

new_fire_ult = """        } else if (cls.id === 'fire') {
          soundEngine.playGlobalBurstFanfare();
          const ultDmg = Math.round(basePower * 15);
          setBossHp((hp) => Math.max(0, hp - ultDmg));
          setPlayerTotalDamage((prev) => prev + ultDmg);
          setServerFurnaceHeat((prev) => Math.min(10000, prev + 2000));
          setFurnaceOverheatTimeLeft(15);
          canvasHandleRef.current?.spawnCombatText('☀️ HỎA NGỤC ĐỒNG QUY!', `MẶT TRỜI RỰC CHÁY: -${ultDmg} DMG · +2,000°C · QUÁ NHIỆT 15S`, '#FF4D00', '#FFD700', true);
          appendCombatLog(`☀️ [HỎA NGỤC ĐỒNG QUY] Đại chiêu thức thứ 4! Lò Rèn bốc cháy ngút trời: Bơm +2,000°C và duy trì trạng thái Quá Nhiệt trong 15 giây!`, 'gold');"""

if old_fire_ult in app:
    app = app.replace(old_fire_ult, new_fire_ult, 1)
    print("Patched Chiêu R Fire in App.tsx.")
else:
    print("Warning: old_fire_ult not found in App.tsx!")

# Pass furnaceOverheatTimeLeft to TopBossHeader in App.tsx
old_tbh_call = """        serverFurnaceHeat={serverFurnaceHeat}
        vaultMeltingThreshold={currentVault.meltingThreshold}"""

new_tbh_call = """        serverFurnaceHeat={serverFurnaceHeat}
        furnaceOverheatTimeLeft={furnaceOverheatTimeLeft}
        vaultMeltingThreshold={currentVault.meltingThreshold}"""

if old_tbh_call in app:
    app = app.replace(old_tbh_call, new_tbh_call, 1)
    print("Passed furnaceOverheatTimeLeft to TopBossHeader.")
else:
    print("Warning: old_tbh_call not found in App.tsx!")

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("Balance patch successfully applied to TopBossHeader.tsx and App.tsx!")
