# -*- coding: utf-8 -*-
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update rules imports
old_rules_import = """  MAX_INVENTORY_SLOTS,
  rollLootDrop,
  getSalvageYield,
  getItemRarityMeta,
  calculateArsenalBonuses,
  checkForgeEquilibrium,
  ForgerRank,
  FORGER_RANKS,
  getForgerRank,"""

new_rules_import = """  MAX_INVENTORY_SLOTS,
  getMaxInventorySlots,
  rollLootDrop,
  openWorldRaidClearChest,
  ascendEquipmentTier,
  getSalvageYield,
  getItemRarityMeta,
  calculateArsenalBonuses,
  checkForgeEquilibrium,
  ForgerRank,
  FORGER_RANKS,
  getForgerRank,"""

if old_rules_import in code:
    code = code.replace(old_rules_import, new_rules_import, 1)
    print("Updated rules import in App.tsx.")
else:
    print("Warning: old_rules_import not found!")

# 2. Add new states after tinhHoa state
target_state = """  const [tinhHoa, setTinhHoa] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tinhHoa === 'number') return parsed.tinhHoa;
      }
    } catch {}
    return 0;
  });"""

new_states = """  const [tinhHoa, setTinhHoa] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.tinhHoa === 'number') return parsed.tinhHoa;
      }
    } catch {}
    return 0;
  });
  const [ironDust, setIronDust] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.ironDust === 'number') return parsed.ironDust;
      }
    } catch {}
    return 0;
  });
  const [celestialStars, setCelestialStars] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.celestialStars === 'number') return parsed.celestialStars;
      }
    } catch {}
    return 0;
  });
  const [anvilPityCount, setAnvilPityCount] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.anvilPityCount === 'number') return parsed.anvilPityCount;
      }
    } catch {}
    return 0;
  });
  const [raidPityCount, setRaidPityCount] = useState<number>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (typeof parsed.raidPityCount === 'number') return parsed.raidPityCount;
      }
    } catch {}
    return 0;
  });
  const [autoSalvageTiers, setAutoSalvageTiers] = useState<{ tierE: boolean; tierD: boolean; tierC: boolean }>(() => {
    try {
      const s = getInitialSaveString();
      if (s) {
        const parsed = JSON.parse(s);
        if (parsed.autoSalvageTiers) return parsed.autoSalvageTiers;
      }
    } catch {}
    return { tierE: false, tierD: false, tierC: false };
  });"""

if target_state in code:
    code = code.replace(target_state, new_states, 1)
    print("Added v3.2 MMORPG progression states.")
else:
    print("Warning: target_state not found!")

# 3. Update loadSaveData
old_load = """      if (typeof parsed.linhThach === 'number') setLinhThach(parsed.linhThach);
      if (typeof parsed.tinhHoa === 'number') setTinhHoa(parsed.tinhHoa);"""

new_load = """      if (typeof parsed.linhThach === 'number') setLinhThach(parsed.linhThach);
      if (typeof parsed.tinhHoa === 'number') setTinhHoa(parsed.tinhHoa);
      if (typeof parsed.ironDust === 'number') setIronDust(parsed.ironDust);
      if (typeof parsed.celestialStars === 'number') setCelestialStars(parsed.celestialStars);
      if (typeof parsed.anvilPityCount === 'number') setAnvilPityCount(parsed.anvilPityCount);
      if (typeof parsed.raidPityCount === 'number') setRaidPityCount(parsed.raidPityCount);
      if (parsed.autoSalvageTiers) setAutoSalvageTiers(parsed.autoSalvageTiers);"""

if old_load in code:
    code = code.replace(old_load, new_load, 1)
    print("Updated loadSaveData.")

# 4. Update resetToFreshCharacter
old_reset = """  const resetToFreshCharacter = useCallback(() => {
    setLinhThach(0);
    setTinhHoa(0);"""

new_reset = """  const resetToFreshCharacter = useCallback(() => {
    setLinhThach(0);
    setTinhHoa(0);
    setIronDust(0);
    setCelestialStars(0);
    setAnvilPityCount(0);
    setRaidPityCount(0);
    setAutoSalvageTiers({ tierE: false, tierD: false, tierC: false });"""

if old_reset in code:
    code = code.replace(old_reset, new_reset, 1)
    print("Updated resetToFreshCharacter.")

# 5. Update save serialization in guestPayload, freshPayload, accountPayload
old_guest_payload = """        const guestPayload = {
          bossHp,
          linhThach,
          tinhHoa,"""

new_guest_payload = """        const guestPayload = {
          bossHp,
          linhThach,
          tinhHoa,
          ironDust,
          celestialStars,
          anvilPityCount,
          raidPityCount,
          autoSalvageTiers,"""

code = code.replace(old_guest_payload, new_guest_payload)

old_fresh_payload = """        const freshPayload = {
          bossHp: BOSS_FLOOR_1_MAX_HP,
          linhThach: 0,
          tinhHoa: 0,"""

new_fresh_payload = """        const freshPayload = {
          bossHp: BOSS_FLOOR_1_MAX_HP,
          linhThach: 0,
          tinhHoa: 0,
          ironDust: 0,
          celestialStars: 0,
          anvilPityCount: 0,
          raidPityCount: 0,
          autoSalvageTiers: { tierE: false, tierD: false, tierC: false },"""

code = code.replace(old_fresh_payload, new_fresh_payload)

old_account_payload = """        const accountPayload = {
          bossHp,
          linhThach,
          tinhHoa,"""

new_account_payload = """        const accountPayload = {
          bossHp,
          linhThach,
          tinhHoa,
          ironDust,
          celestialStars,
          anvilPityCount,
          raidPityCount,
          autoSalvageTiers,"""

code = code.replace(old_account_payload, new_account_payload)

# 6. Update handleSalvageItem and handleQuickSalvage
old_salvage_item = """  const handleSalvageItem = useCallback(
    (item: EquipmentItem) => {
      const yieldReward = getSalvageYield(item);
      setLinhThach((prev) => prev + yieldReward.linhThach);
      if (yieldReward.tinhHoa > 0) {
        setTinhHoa((prev) => prev + yieldReward.tinhHoa);
      }
      if (equippedItems[item.slotKey]?.id === item.id) {
        setEquippedItems((prev) => ({
          ...prev,
          [item.slotKey]: null,
        }));
      } else {
        setInventory((prev) => prev.filter((it) => it.id !== item.id));
      }
      soundEngine.playStanceSwitch('W');
      appendCombatLog(
        `♻️ Phân giải [${item.name}]: Thu được +${yieldReward.linhThach} Linh Thạch${
          yieldReward.tinhHoa > 0 ? `, +${yieldReward.tinhHoa} Tinh Hoa` : ''
        }!`,
        'gold'
      );
    },
    [equippedItems, appendCombatLog]
  );

  const handleQuickSalvage = useCallback(
    (rarities: ItemRarity[]) => {
      const targetItems = inventory.filter((it) => rarities.includes(it.rarity));
      if (targetItems.length === 0) return;

      let totalLT = 0;
      let totalTH = 0;
      targetItems.forEach((it) => {
        const r = getSalvageYield(it);
        totalLT += r.linhThach;
        totalTH += r.tinhHoa;
      });

      setLinhThach((prev) => prev + totalLT);
      if (totalTH > 0) setTinhHoa((prev) => prev + totalTH);

      setInventory((prev) => prev.filter((it) => !rarities.includes(it.rarity)));
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(
        `♻️ [PHÂN GIẢI NHANH] Đã tách ${targetItems.length} món trang bị! Thu được +${totalLT.toLocaleString(
          'en-US'
        )} Linh Thạch${totalTH > 0 ? `, +${totalTH} Tinh Hoa` : ''}!`,
        'cyan'
      );
    },
    [inventory, appendCombatLog]
  );"""

new_salvage_item = """  const handleSalvageItem = useCallback(
    (item: EquipmentItem) => {
      const yieldReward = getSalvageYield(item);
      setLinhThach((prev) => prev + yieldReward.linhThach);
      if (yieldReward.tinhHoa > 0) {
        setTinhHoa((prev) => prev + yieldReward.tinhHoa);
      }
      if (yieldReward.ironDust > 0) {
        setIronDust((prev) => prev + yieldReward.ironDust);
      }
      if (yieldReward.celestialStar > 0) {
        setCelestialStars((prev) => prev + yieldReward.celestialStar);
      }
      if (equippedItems[item.slotKey]?.id === item.id) {
        setEquippedItems((prev) => ({
          ...prev,
          [item.slotKey]: null,
        }));
      } else {
        setInventory((prev) => prev.filter((it) => it.id !== item.id));
      }
      soundEngine.playStanceSwitch('W');
      appendCombatLog(
        `♻️ Phân giải [${item.name}]: Thu được +${yieldReward.ironDust} Bụi Thiết, +${yieldReward.linhThach} Linh Thạch${
          yieldReward.tinhHoa > 0 ? `, +${yieldReward.tinhHoa} Tinh Hoa` : ''
        }${yieldReward.celestialStar > 0 ? `, +${yieldReward.celestialStar} Thiên Tinh` : ''}!`,
        'gold'
      );
    },
    [equippedItems, appendCombatLog]
  );

  const handleQuickSalvage = useCallback(
    (rarities: ItemRarity[]) => {
      const targetItems = inventory.filter((it) => rarities.includes(it.rarity));
      if (targetItems.length === 0) return;

      let totalLT = 0;
      let totalTH = 0;
      let totalDust = 0;
      let totalStars = 0;
      targetItems.forEach((it) => {
        const r = getSalvageYield(it);
        totalLT += r.linhThach;
        totalTH += r.tinhHoa;
        totalDust += r.ironDust;
        totalStars += r.celestialStar;
      });

      setLinhThach((prev) => prev + totalLT);
      if (totalTH > 0) setTinhHoa((prev) => prev + totalTH);
      if (totalDust > 0) setIronDust((prev) => prev + totalDust);
      if (totalStars > 0) setCelestialStars((prev) => prev + totalStars);

      setInventory((prev) => prev.filter((it) => !rarities.includes(it.rarity)));
      soundEngine.playGlobalBurstFanfare();
      appendCombatLog(
        `♻️ [PHÂN GIẢI NHANH] Đã tách ${targetItems.length} món trang bị! Thu được +${totalDust} Bụi Thiết, +${totalLT.toLocaleString(
          'en-US'
        )} Linh Thạch${totalTH > 0 ? `, +${totalTH} Tinh Hoa` : ''}${totalStars > 0 ? `, +${totalStars} Thiên Tinh` : ''}!`,
        'cyan'
      );
    },
    [inventory, appendCombatLog]
  );

  const handleToggleAutoSalvage = useCallback((tierKey: 'tierE' | 'tierD' | 'tierC') => {
    setAutoSalvageTiers((prev) => ({
      ...prev,
      [tierKey]: !prev[tierKey],
    }));
  }, []);

  const handleAscendItem = useCallback(
    (item: EquipmentItem) => {
      if (item.rarity !== 'legendary') return;
      if (ironDust < 1000 || tinhHoa < 10 || celestialStars < 1) {
        appendCombatLog('⚠️ Không đủ nguyên liệu Thăng Bậc (Cần 1,000 Bụi Thiết, 10 Tinh Hoa, 1 Thiên Tinh)!', 'red');
        return;
      }
      setIronDust((d) => d - 1000);
      setTinhHoa((th) => th - 10);
      setCelestialStars((s) => s - 1);

      const ascended = ascendEquipmentTier(item);
      if (equippedItems[item.slotKey]?.id === item.id) {
        setEquippedItems((prev) => ({
          ...prev,
          [item.slotKey]: ascended,
        }));
      } else {
        setInventory((prev) => prev.map((it) => (it.id === item.id ? ascended : it)));
      }
      soundEngine.playGlobalBurstFanfare();
      canvasHandleRef.current?.spawnCombatText(
        '🌟 THẦN THÔNG TIER S!',
        ascended.name,
        '#FF1A53',
        '#FFD700',
        true
      );
      appendCombatLog(
        `🌟 [THĂNG BẬC THẦN KHÍ] Chúc mừng! Trang bị [${item.name}] đã đột phá lên Tier S: [${ascended.name}]!`,
        'gold'
      );
    },
    [ironDust, tinhHoa, celestialStars, equippedItems, appendCombatLog]
  );"""

if old_salvage_item in code:
    code = code.replace(old_salvage_item, new_salvage_item, 1)
    print("Updated salvage handlers and added handleAscendItem.")
else:
    print("Warning: old_salvage_item not found!")

# 7. Update loot drop in handleHeroStrike
old_loot_drop = """        // 9. Procedural ARPG Loot Drop Check
        const droppedItem = rollLootDrop(
          grade,
          outcome.triggeredOverdrive || overdriveActive,
          isShieldBroken
        );
        if (droppedItem) {
          setInventory((prevInv) => {
            if (prevInv.length >= MAX_INVENTORY_SLOTS) {
              appendCombatLog(
                `⚠️ [TÚI ĐỒ ĐẦY] Rơi [${droppedItem.name}] nhưng rương đã kín chỗ (${MAX_INVENTORY_SLOTS}/${MAX_INVENTORY_SLOTS})! Hãy phân giải bớt.`,
                'red'
              );
              return prevInv;
            }
            const rMeta = getItemRarityMeta(droppedItem.rarity);
            soundEngine.playGlobalBurstFanfare();
            canvasHandleRef.current?.spawnCombatText(
              `🎁 RƠI ${rMeta.label.toUpperCase()}!`,
              droppedItem.name,
              rMeta.hex,
              '#FFFFFF',
              true
            );
            appendCombatLog(
              `🎁 [RƠI TRANG BỊ] Bạn vừa nhặt được [${droppedItem.name}] (${rMeta.label})! Đã chuyển vào Túi Đồ.`,
              droppedItem.rarity === 'mythic' || droppedItem.rarity === 'legendary' ? 'gold' : 'cyan'
            );
            return [droppedItem, ...prevInv];
          });
        }"""

new_loot_drop = """        // 9. Procedural ARPG Loot Drop Check with MMORPG Drop Table & Dual Pity
        const dropResult = rollLootDrop({
          grade,
          isOverdrive: outcome.triggeredOverdrive || overdriveActive,
          isShieldBreak: isShieldBroken,
          magicFindPct: arsenalBonuses.magicFindPct,
          vaultFloorId: currentVaultId,
          anvilPityCount,
        });

        if (dropResult.newPityCount !== anvilPityCount) {
          setAnvilPityCount(dropResult.newPityCount);
        }

        if (dropResult.item) {
          const droppedItem = dropResult.item;
          const rMeta = getItemRarityMeta(droppedItem.rarity);

          // Auto-salvage check
          const shouldAutoSalvage =
            (droppedItem.rarity === 'common' && autoSalvageTiers.tierE) ||
            (droppedItem.rarity === 'uncommon' && autoSalvageTiers.tierD) ||
            (droppedItem.rarity === 'rare' && autoSalvageTiers.tierC);

          if (shouldAutoSalvage) {
            const salvage = getSalvageYield(droppedItem);
            setLinhThach((lt) => lt + salvage.linhThach);
            setIronDust((d) => d + salvage.ironDust);
            if (salvage.tinhHoa > 0) setTinhHoa((th) => th + salvage.tinhHoa);
            appendCombatLog(
              `⚡ [TỰ ĐỘNG NUNG] Rơi [${droppedItem.name}] [Tier ${rMeta.tier}] -> Tự nung ra +${salvage.ironDust} Bụi Thiết, +${salvage.linhThach} LT!`,
              'cyan'
            );
          } else {
            const currentCapacity = getMaxInventorySlots(forgerRank.tier);
            setInventory((prevInv) => {
              if (prevInv.length >= currentCapacity) {
                appendCombatLog(
                  `⚠️ [TÚI ĐỒ ĐẦY] Rơi [${droppedItem.name}] nhưng rương đã kín chỗ (${currentCapacity}/${currentCapacity})! Hãy phân giải bớt.`,
                  'red'
                );
                return prevInv;
              }
              soundEngine.playGlobalBurstFanfare();
              canvasHandleRef.current?.spawnCombatText(
                `🎁 RƠI TIER ${rMeta.tier}!`,
                droppedItem.name,
                rMeta.hex,
                '#FFFFFF',
                true
              );
              appendCombatLog(
                `🎁 [RƠI TRANG BỊ] Bạn vừa nhặt được [${droppedItem.name}] [Tier ${rMeta.tier} - ${rMeta.label}]! Đã chuyển vào Túi Đồ.`,
                droppedItem.rarity === 'mythic' || droppedItem.rarity === 'legendary' ? 'gold' : 'cyan'
              );
              return [droppedItem, ...prevInv];
            });
          }
        }"""

if old_loot_drop in code:
    code = code.replace(old_loot_drop, new_loot_drop, 1)
    print("Updated rollLootDrop in handleHeroStrike.")
else:
    print("Warning: old_loot_drop not found!")

# 8. Update RightProgressionPanel props invocation
old_render_panel = """          <RightProgressionPanel
            equippedItems={equippedItems}
            inventory={inventory}
            upgrades={upgrades}
            spiritNodes={spiritNodes}
            stanceSkills={stanceSkills}
            forgerRank={forgerRank}
            playerTotalDamage={playerTotalDamage}
            burnStacks={burnStacks}
            linhThach={linhThach}
            tinhHoa={tinhHoa}
            tier2Unlocked={tier2Unlocked}
            leaderboard={leaderboard}
            mobileDrawerOpen={rightPanelOpen}
            onCloseMobileDrawer={() => setRightPanelOpen(false)}
            onBuyUpgrade={handleBuyUpgrade}
            onUnlockSpiritNode={handleUnlockSpiritNode}
            onUnlockStanceSkill={handleUnlockStanceSkill}
            onEquipItem={handleEquipItem}
            onUnequipItem={handleUnequipItem}
            onSalvageItem={handleSalvageItem}
            onQuickSalvage={handleQuickSalvage}
            onQuenchItem={handleQuenchItem}
          />"""

new_render_panel = """          <RightProgressionPanel
            equippedItems={equippedItems}
            inventory={inventory}
            upgrades={upgrades}
            spiritNodes={spiritNodes}
            stanceSkills={stanceSkills}
            forgerRank={forgerRank}
            playerTotalDamage={playerTotalDamage}
            burnStacks={burnStacks}
            linhThach={linhThach}
            tinhHoa={tinhHoa}
            ironDust={ironDust}
            celestialStars={celestialStars}
            anvilPityCount={anvilPityCount}
            raidPityCount={raidPityCount}
            autoSalvageTiers={autoSalvageTiers}
            tier2Unlocked={tier2Unlocked}
            leaderboard={leaderboard}
            mobileDrawerOpen={rightPanelOpen}
            onCloseMobileDrawer={() => setRightPanelOpen(false)}
            onBuyUpgrade={handleBuyUpgrade}
            onUnlockSpiritNode={handleUnlockSpiritNode}
            onUnlockStanceSkill={handleUnlockStanceSkill}
            onEquipItem={handleEquipItem}
            onUnequipItem={handleUnequipItem}
            onSalvageItem={handleSalvageItem}
            onQuickSalvage={handleQuickSalvage}
            onQuenchItem={handleQuenchItem}
            onAscendItem={handleAscendItem}
            onToggleAutoSalvage={handleToggleAutoSalvage}
          />"""

if old_render_panel in code:
    code = code.replace(old_render_panel, new_render_panel, 1)
    print("Updated RightProgressionPanel props call in App.tsx.")
else:
    print("Warning: old_render_panel not found!")

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch App.tsx completed successfully!")
