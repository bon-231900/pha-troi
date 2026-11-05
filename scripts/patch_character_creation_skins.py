# -*- coding: utf-8 -*-
with open('frontend/src/components/CharacterCreationModal.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_imp = "import {\n  PlayerClassId,\n  PLAYER_CLASSES,\n  PlayerClassMeta,\n} from '../game/rules';"
new_imp = "import {\n  PlayerClassId,\n  PLAYER_CLASSES,\n  PlayerClassMeta,\n  CHARACTER_SKINS,\n  SECT_DEFAULT_SKIN,\n  CharacterSkinMeta,\n} from '../game/rules';"
if old_imp not in content:
    old_imp = old_imp.replace("\n", "\r\n")
    new_imp = new_imp.replace("\n", "\r\n")
content = content.replace(old_imp, new_imp, 1)

# 2. Update CharacterCreationModalProps
old_props = """interface CharacterCreationModalProps {
  currentClassId?: PlayerClassId | null;
  currentName?: string;
  isInitialCreation?: boolean;
  slotId?: 1 | 2 | 3;
  onConfirm: (classId: PlayerClassId, characterName: string) => void;
  onCancel?: () => void;
}"""

new_props = """interface CharacterCreationModalProps {
  currentClassId?: PlayerClassId | null;
  currentName?: string;
  currentSkinId?: string | null;
  isInitialCreation?: boolean;
  slotId?: 1 | 2 | 3;
  onConfirm: (classId: PlayerClassId, characterName: string, skinId?: string) => void;
  onCancel?: () => void;
}"""
if old_props not in content:
    old_props = old_props.replace("\n", "\r\n")
    new_props = new_props.replace("\n", "\r\n")
content = content.replace(old_props, new_props, 1)

# 3. Update component parameters and state
old_comp = """export const CharacterCreationModal: React.FC<CharacterCreationModalProps> = ({
  currentClassId = null,
  currentName = '',
  isInitialCreation = false,
  slotId,
  onConfirm,
  onCancel,
}) => {
  const [selectedClassId, setSelectedClassId] = useState<PlayerClassId>(currentClassId || 'thunder');"""

new_comp = """export const CharacterCreationModal: React.FC<CharacterCreationModalProps> = ({
  currentClassId = null,
  currentName = '',
  currentSkinId = null,
  isInitialCreation = false,
  slotId,
  onConfirm,
  onCancel,
}) => {
  const [selectedClassId, setSelectedClassId] = useState<PlayerClassId>(currentClassId || 'thunder');
  const [selectedSkinId, setSelectedSkinId] = useState<string>(() => {
    if (currentSkinId && CHARACTER_SKINS[currentSkinId]) return currentSkinId;
    return SECT_DEFAULT_SKIN[currentClassId || 'thunder'] || 'skin_thunder_robe';
  });"""

if old_comp not in content:
    old_comp = old_comp.replace("\n", "\r\n")
    new_comp = new_comp.replace("\n", "\r\n")
content = content.replace(old_comp, new_comp, 1)

# 4. Update handleSelectClass & handleCommit
old_handlers = """  const handleSelectClass = (cId: PlayerClassId) => {
    setSelectedClassId(cId);
    const cls = PLAYER_CLASSES[cId];
    soundEngine.playStanceSwitch(cls.stanceKey);
  };

  const handleCommit = () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    soundEngine.unlockAudio();
    soundEngine.playGlobalBurstFanfare();
    setTimeout(() => {
      onConfirm(selectedClassId, characterName.trim() || 'Thợ Rèn Vô Danh');
    }, 400);
  };"""

new_handlers = """  const handleSelectClass = (cId: PlayerClassId) => {
    setSelectedClassId(cId);
    setSelectedSkinId(SECT_DEFAULT_SKIN[cId] || 'skin_default');
    const cls = PLAYER_CLASSES[cId];
    soundEngine.playStanceSwitch(cls.stanceKey);
  };

  const handleSelectSkin = (sId: string) => {
    setSelectedSkinId(sId);
    soundEngine.playAnvilStrike('GREAT', 'Q', false);
  };

  const handleCommit = () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    soundEngine.unlockAudio();
    soundEngine.playGlobalBurstFanfare();
    setTimeout(() => {
      onConfirm(selectedClassId, characterName.trim() || 'Thợ Rèn Vô Danh', selectedSkinId);
    }, 400);
  };"""

if old_handlers not in content:
    old_handlers = old_handlers.replace("\n", "\r\n")
    new_handlers = new_handlers.replace("\n", "\r\n")
content = content.replace(old_handlers, new_handlers, 1)

# 5. Update InteractiveAltarPreview invocation and add Outfit Selector
old_left_col = """          {/* LEFT COLUMN: 2.5D INTERACTIVE ALTAR & PRE-TEST HAMMER */}
          <div className="lg:col-span-5 flex flex-col justify-between">
            <InteractiveAltarPreview
              ref={altarPreviewRef}
              selectedClassId={selectedClassId}
              characterName={characterName}
            />
          </div>"""

clean_base = "${import.meta.env.BASE_URL || './'}"
new_left_col = f"""          {{/* LEFT COLUMN: 2.5D INTERACTIVE ALTAR & PRE-TEST HAMMER */}}
          <div className="lg:col-span-5 flex flex-col justify-between gap-2.5">
            <InteractiveAltarPreview
              ref={{altarPreviewRef}}
              selectedClassId={{selectedClassId}}
              characterName={{characterName}}
              skinId={{selectedSkinId}}
            />

            {{/* Sect Outfits & Robe Selector */}}
            <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col gap-2">
              <div className="flex items-center justify-between text-xs font-tech">
                <span className="text-amber-300 font-bold uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>Y PHỤC MÔN PHÁI (5 BỘ ĐỒ ĐỘC BẢN):</span>
                </span>
                <span className="text-[11px] text-slate-400">
                  Đang chọn: <b className="text-amber-300">{{CHARACTER_SKINS[selectedSkinId]?.name || 'Phục Trang'}}</b>
                </span>
              </div>

              {{/* 5 Outfit Cards Row */}}
              <div className="grid grid-cols-5 gap-1.5">
                {{Object.values(CHARACTER_SKINS).map((sk) => {{
                  const isSelected = selectedSkinId === sk.id;
                  const isSectMatch = sk.sectId === selectedClassId;
                  return (
                    <button
                      key={{sk.id}}
                      type="button"
                      onClick={{() => handleSelectSkin(sk.id)}}
                      className={{`relative rounded-xl border p-1 text-center cursor-pointer transition-all flex flex-col items-center gap-1 group ${{
                        isSelected
                          ? 'bg-slate-800/90 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-105 z-10'
                          : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                      }}`}}
                      title={{`${{sk.name}} · ${{sk.sectTitle}}\\n${{sk.description}}`}}
                    >
                      {{/* Sect Recommended Tag */}}
                      {{isSectMatch && (
                        <div className="absolute -top-1.5 -right-1 px-1 py-0.2 rounded-full bg-amber-500 text-slate-950 text-[7px] font-bold z-20 shadow">
                          CHUẨN
                        </div>
                      )}}

                      {{/* Outfit Card Image */}}
                      <div className="w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50">
                        <img
                          src={{`${clean_base}${{sk.cardPath}}`}}
                          alt={{sk.name}}
                          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
                        <span className="absolute bottom-0.5 right-1 text-[11px]">{{sk.icon}}</span>
                      </div>

                      {{/* Outfit Short Name */}}
                      <span className={{`text-[9px] font-tech font-bold leading-tight truncate w-full ${{
                        isSelected ? 'text-amber-300' : 'text-slate-300'
                      }}`}}>
                        {{sk.name.replace('Phàm Nhân ', '').replace('Cửu Tiêu ', '').replace('Hắc Diệm ', '').replace('Bất Chu ', '').replace('Thanh Mộc ', '')}}
                      </span>
                    </button>
                  );
                }})}}
              </div>

              {{/* Lore / Description Line */}}
              <div className="text-[10px] font-tech text-slate-400 italic bg-slate-950/60 py-1 px-2 rounded-lg border border-slate-800/60 truncate">
                ✨ {{CHARACTER_SKINS[selectedSkinId]?.description || ''}}
              </div>
            </div>
          </div>"""

if old_left_col not in content:
    old_left_col = old_left_col.replace("\n", "\r\n")
    new_left_col = new_left_col.replace("\n", "\r\n")
content = content.replace(old_left_col, new_left_col, 1)

with open('frontend/src/components/CharacterCreationModal.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: CharacterCreationModal.tsx patched with sect outfit selector!")
