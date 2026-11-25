# -*- coding: utf-8 -*-
import os

# 1. Update CharacterCreationModal.tsx
with open('frontend/src/components/CharacterCreationModal.tsx', 'r', encoding='utf-8') as f:
    ccm = f.read()

# Replace import
ccm = ccm.replace(
    """  CHARACTER_SKINS,
  SECT_DEFAULT_SKIN,
  CharacterSkinMeta,""",
    """  CHARACTER_SKINS,
  SECT_DEFAULT_SKIN,
  AVAILABLE_CHARACTER_SKINS,
  getSkinOrDefault,
  CharacterSkinMeta,"""
)

# Update selectedSkinId default
ccm = ccm.replace(
    """  const [selectedSkinId, setSelectedSkinId] = useState<string>(() => {
    if (currentSkinId && CHARACTER_SKINS[currentSkinId]) return currentSkinId;
    return SECT_DEFAULT_SKIN[currentClassId || 'thunder'] || 'skin_thunder_robe';
  });""",
    """  const [selectedSkinId, setSelectedSkinId] = useState<string>(() => {
    return getSkinOrDefault(currentSkinId, currentClassId || 'thunder').id;
  });"""
)

# Update handleSelectClass
ccm = ccm.replace(
    """  const handleSelectClass = (cId: PlayerClassId) => {
    setSelectedClassId(cId);
    setSelectedSkinId(SECT_DEFAULT_SKIN[cId] || 'skin_default');""",
    """  const handleSelectClass = (cId: PlayerClassId) => {
    setSelectedClassId(cId);
    setSelectedSkinId(getSkinOrDefault(undefined, cId).id);"""
)

# Replace Outfit selector UI section
old_outfits_section = """            {/* Sect Outfits & Robe Selector */}
            <div className=\"p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col gap-2\">
              <div className=\"flex items-center justify-between text-xs font-tech\">
                <span className=\"text-amber-300 font-bold uppercase tracking-wider flex items-center gap-1.5\">
                  <Sparkles className=\"w-3.5 h-3.5 text-amber-400\" />
                  <span>Y PHỤC MÔN PHÁI (5 BỘ ĐỒ ĐỘC BẢN):</span>
                </span>
                <span className=\"text-[11px] text-slate-400\">
                  Đang chọn: <b className=\"text-amber-300\">{CHARACTER_SKINS[selectedSkinId]?.name || 'Phục Trang'}</b>
                </span>
              </div>

              {/* 5 Outfit Cards Row */}
              <div className=\"grid grid-cols-4 sm:grid-cols-8 gap-1.5\">
                {Object.values(CHARACTER_SKINS).map((sk) => {
                  const isSelected = selectedSkinId === sk.id;
                  const isSectMatch = sk.sectId === selectedClassId;
                  return (
                    <button
                      key={sk.id}
                      type="button"
                      onClick={() => handleSelectSkin(sk.id)}
                      className={`relative rounded-xl border p-1 text-center cursor-pointer transition-all flex flex-col items-center gap-1 group ${
                        isSelected
                          ? 'bg-slate-800/90 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-105 z-10'
                          : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                      }`}
                      title={`${sk.name} · ${sk.sectTitle}\\n${sk.description}`}
                    >
                      {/* Sect Recommended Tag */}
                      {isSectMatch && (
                        <div className=\"absolute -top-1.5 -right-1 px-1 py-0.2 rounded-full bg-amber-500 text-slate-950 text-[7px] font-bold z-20 shadow\">
                          CHUẨN
                        </div>
                      )}

                      {/* Outfit Card Image */}
                      <div className=\"w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50\">
                        <img
                          src={`${import.meta.env.BASE_URL || './'}${sk.cardPath}`}
                          alt={sk.name}
                          className=\"w-full h-full object-cover group-hover:scale-110 transition-transform duration-300\"
                        />
                        <div className=\"absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none\" />
                        <span className=\"absolute bottom-0.5 right-1 text-[11px]\">{sk.icon}</span>
                      </div>

                      {/* Outfit Short Name */}
                      <span className={`text-[9px] font-tech font-bold leading-tight truncate w-full ${
                        isSelected ? 'text-amber-300' : 'text-slate-300'
                      }`}>
                        {sk.name.replace('Phàm Nhân ', '').replace('Cửu Tiêu ', '').replace('Hắc Diệm ', '').replace('Bất Chu ', '').replace('Thanh Mộc ', '').replace('Thái Cổ ', '').replace('Phần Thiên ', '').replace('Bích Lạc ', '')}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Lore / Description Line */}
              <div className=\"text-[10px] font-tech text-slate-400 italic bg-slate-950/60 py-1 px-2 rounded-lg border border-slate-800/60 truncate\">
                ✨ {CHARACTER_SKINS[selectedSkinId]?.description || ''}
              </div>
            </div>"""

new_outfits_section = """            {/* Sect Outfits & Robe Selector */}
            <div className=\"p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col gap-2\">
              <div className=\"flex items-center justify-between text-xs font-tech\">
                <span className=\"text-amber-300 font-bold uppercase tracking-wider flex items-center gap-1.5\">
                  <Sparkles className=\"w-3.5 h-3.5 text-amber-400\" />
                  <span>TRANG PHỤC THẦN KHÍ (CHUYỂN ĐỘNG VUNG CHÙY RÈN):</span>
                </span>
                <span className=\"text-[11px] text-slate-400\">
                  Đang chọn: <b className=\"text-amber-300\">{CHARACTER_SKINS[selectedSkinId]?.name || 'Phục Trang'}</b>
                </span>
              </div>

              {/* Verified Outfit Cards Row */}
              <div className=\"grid grid-cols-2 gap-2.5 max-w-sm mx-auto w-full\">
                {AVAILABLE_CHARACTER_SKINS.map((sk) => {
                  const isSelected = selectedSkinId === sk.id;
                  const isSectMatch = sk.sectId === selectedClassId;
                  return (
                    <button
                      key={sk.id}
                      type="button"
                      onClick={() => handleSelectSkin(sk.id)}
                      className={`relative rounded-xl border p-2 text-center cursor-pointer transition-all flex flex-col items-center gap-1.5 group ${
                        isSelected
                          ? 'bg-slate-800/90 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-[1.02] z-10'
                          : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                      }`}
                      title={`${sk.name} · ${sk.sectTitle}\\n${sk.description}`}
                    >
                      {/* Sect Recommended Tag */}
                      {isSectMatch ? (
                        <div className=\"absolute -top-1.5 -right-1 px-1.5 py-0.5 rounded-full bg-amber-500 text-slate-950 text-[8px] font-bold z-20 shadow\">
                          CHUẨN HỆ
                        </div>
                      ) : sk.sectId === 'neutral' ? (
                        <div className=\"absolute -top-1.5 -right-1 px-1.5 py-0.5 rounded-full bg-slate-600 text-slate-100 text-[8px] font-bold z-20 shadow\">
                          TOÀN HỆ
                        </div>
                      ) : null}

                      {/* Outfit Card Image */}
                      <div className=\"w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50\">
                        <img
                          src={`${import.meta.env.BASE_URL || './'}${sk.cardPath}`}
                          alt={sk.name}
                          className=\"w-full h-full object-cover group-hover:scale-105 transition-transform duration-300\"
                        />
                        <div className=\"absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none\" />
                        <span className=\"absolute bottom-1 right-1.5 text-xs\">{sk.icon}</span>
                      </div>

                      {/* Outfit Name & Details */}
                      <span className={`text-[11px] font-tech font-bold leading-tight truncate w-full ${
                        isSelected ? 'text-amber-300' : 'text-slate-200'
                      }`}>
                        {sk.name}
                      </span>
                      <span className=\"text-[9px] text-slate-400 font-tech truncate w-full\">
                        {sk.sectTitle.split('·')[0].trim()}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* Lore / Description Line */}
              <div className=\"text-[10px] font-tech text-slate-400 italic bg-slate-950/60 py-1 px-2.5 rounded-lg border border-slate-800/60 truncate\">
                ✨ {CHARACTER_SKINS[selectedSkinId]?.description || ''}
              </div>
            </div>"""

if old_outfits_section in ccm:
    ccm = ccm.replace(old_outfits_section, new_outfits_section, 1)
    print("Patched CharacterCreationModal outfits section.")
else:
    print("Warning: old_outfits_section not found in CharacterCreationModal!")

with open('frontend/src/components/CharacterCreationModal.tsx', 'w', encoding='utf-8') as f:
    f.write(ccm)

# 2. Update StatusModal.tsx
with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    sm = f.read()

sm = sm.replace(
    "import { PlayerClassMeta, CHARACTER_SKINS } from '../game/rules';",
    "import { PlayerClassMeta, CHARACTER_SKINS, AVAILABLE_CHARACTER_SKINS, getSkinOrDefault } from '../game/rules';"
)

old_sm_wardrobe = """                  <div className=\"grid grid-cols-4 sm:grid-cols-8 gap-1.5\">
                    {Object.values(CHARACTER_SKINS).map((sk) => {
                      const isEquipped = (equippedSkinId || 'skin_default') === sk.id;
                      return (
                        <button
                          key={sk.id}
                          type=\"button\"
                          onClick={() => onEquipSkin(sk.id)}
                          className={`relative rounded-xl border p-1 text-center cursor-pointer transition-all flex flex-col items-center gap-1 group ${
                            isEquipped
                              ? 'bg-slate-800/95 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-105 z-10'
                              : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                          }`}
                          title={`${sk.name} · ${sk.sectTitle}\\n${sk.description}`}
                        >
                          {isEquipped && (
                            <div className=\"absolute -top-1.5 -right-1 px-1 py-0.2 rounded-full bg-emerald-500 text-slate-950 text-[7px] font-bold z-20 shadow\">
                              ĐANG MẶC
                            </div>
                          )}
                          <div className=\"w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50\">
                            <img
                              src={`${import.meta.env.BASE_URL || './'}${sk.cardPath}`}
                              alt={sk.name}
                              className=\"w-full h-full object-cover group-hover:scale-110 transition-transform duration-300\"
                            />
                            <div className=\"absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none\" />
                            <span className=\"absolute bottom-0.5 right-1 text-[11px]\">{sk.icon}</span>
                          </div>
                          <span className={`text-[9px] font-tech font-bold leading-tight truncate w-full ${
                            isEquipped ? 'text-amber-300' : 'text-slate-300'
                          }`}>
                            {sk.name.replace('Phàm Nhân ', '').replace('Cửu Tiêu ', '').replace('Hắc Diệm ', '').replace('Bất Chu ', '').replace('Thanh Mộc ', '').replace('Thái Cổ ', '').replace('Phần Thiên ', '').replace('Bích Lạc ', '')}
                          </span>
                        </button>
                      );
                    })}
                  </div>"""

new_sm_wardrobe = """                  <div className=\"grid grid-cols-2 gap-2.5 max-w-sm mx-auto w-full\">
                    {AVAILABLE_CHARACTER_SKINS.map((sk) => {
                      const isEquipped = (equippedSkinId || 'skin_default') === sk.id;
                      return (
                        <button
                          key={sk.id}
                          type=\"button\"
                          onClick={() => onEquipSkin(sk.id)}
                          className={`relative rounded-xl border p-2 text-center cursor-pointer transition-all flex flex-col items-center gap-1.5 group ${
                            isEquipped
                              ? 'bg-slate-800/95 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-[1.02] z-10'
                              : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                          }`}
                          title={`${sk.name} · ${sk.sectTitle}\\n${sk.description}`}
                        >
                          {isEquipped && (
                            <div className=\"absolute -top-1.5 -right-1 px-1.5 py-0.5 rounded-full bg-emerald-500 text-slate-950 text-[8px] font-bold z-20 shadow\">
                              ĐANG MẶC
                            </div>
                          )}
                          <div className=\"w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50\">
                            <img
                              src={`${import.meta.env.BASE_URL || './'}${sk.cardPath}`}
                              alt={sk.name}
                              className=\"w-full h-full object-cover group-hover:scale-105 transition-transform duration-300\"
                            />
                            <div className=\"absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none\" />
                            <span className=\"absolute bottom-1 right-1.5 text-xs\">{sk.icon}</span>
                          </div>
                          <span className={`text-[11px] font-tech font-bold leading-tight truncate w-full ${
                            isEquipped ? 'text-amber-300' : 'text-slate-200'
                          }`}>
                            {sk.name}
                          </span>
                          <span className=\"text-[9px] text-slate-400 font-tech truncate w-full\">
                            {sk.sectTitle.split('·')[0].trim()}
                          </span>
                        </button>
                      );
                    })}
                  </div>"""

if old_sm_wardrobe in sm:
    sm = sm.replace(old_sm_wardrobe, new_sm_wardrobe, 1)
    print("Patched StatusModal wardrobe section.")
else:
    print("Warning: old_sm_wardrobe not found in StatusModal!")

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(sm)

# 3. Update TitlePages.tsx
with open('frontend/src/components/TitlePages.tsx', 'r', encoding='utf-8') as f:
    tp = f.read()

tp = tp.replace(
    "import { PLAYER_CLASSES, PlayerClassId, CHARACTER_SKINS } from '../game/rules';",
    "import { PLAYER_CLASSES, PlayerClassId, CHARACTER_SKINS, AVAILABLE_CHARACTER_SKINS } from '../game/rules';"
)

tp = tp.replace(
    "👘 TỦ ĐỒ TIÊN GIA (7 BỘ TRANG PHỤC)",
    f"👘 TỦ ĐỒ TIÊN GIA (TRANG PHỤC HOÀN THIỆN)"
)

old_tp_wardrobe = """            {/* SUB-VIEW 2: TỦ ĐỒ TIÊN GIA SHOWCASE */}
            {characterViewMode === 'wardrobe' && (
              <div className=\"grid grid-cols-2 sm:grid-cols-3 md:grid-cols-7 gap-3\">
                {Object.values(CHARACTER_SKINS).map((sk) => (
                  <div key={sk.id} className=\"rounded-xl border border-slate-800 bg-slate-900/70 p-2 flex flex-col gap-2 hover:border-amber-400/60 transition-all group\">
                    <div className=\"w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-950 relative border border-slate-800\">
                      <img 
                        src={`${cleanBase}${sk.cardPath}`} 
                        alt={sk.name} 
                        className=\"w-full h-full object-cover group-hover:scale-105 transition-transform duration-300\" 
                      />
                      <span className=\"absolute bottom-1 right-1 text-sm drop-shadow\">{sk.icon}</span>
                      <span className={`absolute top-1 left-1 px-1.5 py-0.2 rounded text-[8px] font-bold uppercase ${sk.rarityBadgeBg}`}>
                        {sk.rarity.replace('_', ' ')}
                      </span>
                    </div>
                    <div className=\"min-w-0\">
                      <h5 className=\"text-xs font-bold text-slate-200 font-tech truncate\">{sk.name}</h5>
                      <span className=\"text-[10px] text-amber-400/90 font-tech block truncate\">{sk.sectTitle}</span>
                      <p className=\"text-[9px] text-slate-400 font-light mt-1 line-clamp-2 leading-tight\">
                        {sk.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}"""

new_tp_wardrobe = """            {/* SUB-VIEW 2: TỦ ĐỒ TIÊN GIA SHOWCASE */}
            {characterViewMode === 'wardrobe' && (
              <div className=\"grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-xl mx-auto\">
                {AVAILABLE_CHARACTER_SKINS.map((sk) => (
                  <div key={sk.id} className=\"rounded-2xl border border-slate-800 bg-slate-900/80 p-3.5 flex flex-col gap-3 hover:border-amber-400/60 transition-all group shadow-lg\">
                    <div className=\"w-full aspect-[3/4] rounded-xl overflow-hidden bg-slate-950 relative border border-slate-700/60\">
                      <img 
                        src={`${cleanBase}${sk.cardPath}`} 
                        alt={sk.name} 
                        className=\"w-full h-full object-cover group-hover:scale-105 transition-transform duration-300\" 
                      />
                      <span className=\"absolute bottom-1.5 right-2 text-base drop-shadow\">{sk.icon}</span>
                      <span className={`absolute top-2 left-2 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${sk.rarityBadgeBg}`}>
                        {sk.rarity.replace('_', ' ')}
                      </span>
                    </div>
                    <div className=\"min-w-0 space-y-1\">
                      <div className=\"flex items-center justify-between\">
                        <h5 className=\"text-sm font-bold text-amber-200 font-tech truncate\">{sk.name}</h5>
                        <span className=\"text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-400/30 font-tech\">
                          ĐÃ HOÀN THIỆN
                        </span>
                      </div>
                      <span className=\"text-[11px] text-amber-400/90 font-tech block truncate\">{sk.sectTitle}</span>
                      <p className=\"text-[11px] text-slate-300 font-light leading-relaxed\">
                        {sk.description}
                      </p>
                      <div className=\"text-[10px] text-cyan-300 font-tech pt-1 border-t border-slate-800/80\">
                        ✨ {sk.bonusStatText}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}"""

if old_tp_wardrobe in tp:
    tp = tp.replace(old_tp_wardrobe, new_tp_wardrobe, 1)
    print("Patched TitlePages wardrobe showcase.")
else:
    print("Warning: old_tp_wardrobe not found in TitlePages!")

with open('frontend/src/components/TitlePages.tsx', 'w', encoding='utf-8') as f:
    f.write(tp)

# 4. Update InteractiveAltarPreview.tsx
with open('frontend/src/components/InteractiveAltarPreview.tsx', 'r', encoding='utf-8') as f:
    iap = f.read()

iap = iap.replace(
    "import { PlayerClassId, PLAYER_CLASSES, StanceKey, SECT_DEFAULT_SKIN, CHARACTER_SKINS } from '../game/rules';",
    "import { PlayerClassId, PLAYER_CLASSES, StanceKey, SECT_DEFAULT_SKIN, CHARACTER_SKINS, getSkinOrDefault } from '../game/rules';"
)

iap = iap.replace(
    "  const activeSkinId = skinId || SECT_DEFAULT_SKIN[selectedClassId] || 'skin_default';",
    "  const activeSkinId = getSkinOrDefault(skinId, selectedClassId).id;"
)

with open('frontend/src/components/InteractiveAltarPreview.tsx', 'w', encoding='utf-8') as f:
    f.write(iap)
print("Patched InteractiveAltarPreview.tsx.")

# 5. Update App.tsx
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app_code = f.read()

app_code = app_code.replace(
    "  CHARACTER_SKINS,\n} from './game/rules';",
    "  CHARACTER_SKINS,\n  getSkinOrDefault,\n} from './game/rules';"
)

app_code = app_code.replace(
    """  const [equippedSkinId, setEquippedSkinId] = useState<string>(() => {
    return safeStorage.getItem('phatroi_equipped_skin') || 'skin_default';
  });""",
    """  const [equippedSkinId, setEquippedSkinId] = useState<string>(() => {
    return getSkinOrDefault(safeStorage.getItem('phatroi_equipped_skin')).id;
  });"""
)

app_code = app_code.replace(
    "      const skin = profile.equippedSkinId || SECT_DEFAULT_SKIN[profile.classId] || 'skin_default';",
    "      const skin = getSkinOrDefault(profile.equippedSkinId, profile.classId).id;"
)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app_code)
print("Patched App.tsx.")

# 6. Update characterSlots.ts
with open('frontend/src/game/characterSlots.ts', 'r', encoding='utf-8') as f:
    cs = f.read()

cs = cs.replace(
    "  SECT_DEFAULT_SKIN,\n  ensureAllEquippedSlots,\n} from './rules';",
    "  SECT_DEFAULT_SKIN,\n  getSkinOrDefault,\n  ensureAllEquippedSlots,\n} from './rules';"
)

cs = cs.replace(
    "  const finalSkinId = skinId || SECT_DEFAULT_SKIN[classId] || 'skin_default';",
    "  const finalSkinId = getSkinOrDefault(skinId, classId).id;"
)

with open('frontend/src/game/characterSlots.ts', 'w', encoding='utf-8') as f:
    f.write(cs)
print("Patched characterSlots.ts.")

print("All components and logic successfully patched!")
