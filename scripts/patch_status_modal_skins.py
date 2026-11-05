# -*- coding: utf-8 -*-
with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_imp = "import { Sparkles, Trophy, Award, Flame, RefreshCw, Volume2, VolumeX, Shield, Play } from 'lucide-react';"
new_imp = "import { Sparkles, Trophy, Award, Flame, RefreshCw, Volume2, VolumeX, Shield, Play } from 'lucide-react';\nimport { CHARACTER_SKINS } from '../game/rules';"
if old_imp not in content:
    old_imp = old_imp.replace("\n", "\r\n")
    new_imp = new_imp.replace("\n", "\r\n")
content = content.replace(old_imp, new_imp, 1)

# 2. Update StatusModalProps
old_props = """interface StatusModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRestart: () => void;
  onReturnTitle: () => void;
  onSwitchCharacter?: () => void;
  onToggleMute?: () => void;
  muted?: boolean;
  playerClass?: PlayerClassMeta;
}"""

new_props = """interface StatusModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRestart: () => void;
  onReturnTitle: () => void;
  onSwitchCharacter?: () => void;
  onToggleMute?: () => void;
  muted?: boolean;
  playerClass?: PlayerClassMeta;
  equippedSkinId?: string;
  onEquipSkin?: (skinId: string) => void;
}"""

if old_props not in content:
    old_props = old_props.replace("\n", "\r\n")
    new_props = new_props.replace("\n", "\r\n")
content = content.replace(old_props, new_props, 1)

# 3. Update component destructuring
old_destruct = """  onToggleMute,
  muted = false,
  playerClass,
}) => {"""

new_destruct = """  onToggleMute,
  muted = false,
  playerClass,
  equippedSkinId = 'skin_default',
  onEquipSkin,
}) => {"""

if old_destruct not in content:
    old_destruct = old_destruct.replace("\n", "\r\n")
    new_destruct = new_destruct.replace("\n", "\r\n")
content = content.replace(old_destruct, new_destruct, 1)

# 4. Insert Outfit Wardrobe section before Restart & Return buttons
old_row = """              {/* 3. Restart and Title Actions */}"""

clean_base = "${import.meta.env.BASE_URL || './'}"
wardrobe_section = f"""              {{/* 2B. Tủ Đồ Tiên Gia: 5 Bộ Y Phục Môn Phái */}}
              {{onEquipSkin && (
                <div className="p-3 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-col gap-2">
                  <div className="flex items-center justify-between text-xs font-tech">
                    <span className="text-amber-300 font-bold uppercase tracking-wider flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                      <span>TỦ ĐỒ TIÊN GIA (CHỌN TRANG PHỤC):</span>
                    </span>
                    <span className="text-[11px] text-slate-400">
                      Đang mặc: <b className="text-amber-300">{{CHARACTER_SKINS[equippedSkinId || 'skin_default']?.name}}</b>
                    </span>
                  </div>

                  <div className="grid grid-cols-5 gap-1.5">
                    {{Object.values(CHARACTER_SKINS).map((sk) => {{
                      const isEquipped = (equippedSkinId || 'skin_default') === sk.id;
                      return (
                        <button
                          key={{sk.id}}
                          type="button"
                          onClick={{() => onEquipSkin(sk.id)}}
                          className={{`relative rounded-xl border p-1 text-center cursor-pointer transition-all flex flex-col items-center gap-1 group ${{
                            isEquipped
                              ? 'bg-slate-800/95 border-amber-400 ring-2 ring-amber-400/50 shadow-lg scale-105 z-10'
                              : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                          }}`}}
                          title={{`${{sk.name}} · ${{sk.sectTitle}}\\n${{sk.description}}`}}
                        >
                          {{isEquipped && (
                            <div className="absolute -top-1.5 -right-1 px-1 py-0.2 rounded-full bg-emerald-500 text-slate-950 text-[7px] font-bold z-20 shadow">
                              ĐANG MẶC
                            </div>
                          )}}
                          <div className="w-full aspect-[3/4] rounded-lg overflow-hidden bg-slate-900/90 relative border border-slate-700/50">
                            <img
                              src={{`${clean_base}${{sk.cardPath}}`}}
                              alt={{sk.name}}
                              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
                            <span className="absolute bottom-0.5 right-1 text-[11px]">{{sk.icon}}</span>
                          </div>
                          <span className={{`text-[9px] font-tech font-bold leading-tight truncate w-full ${{
                            isEquipped ? 'text-amber-300' : 'text-slate-300'
                          }}`}}>
                            {{sk.name.replace('Phàm Nhân ', '').replace('Cửu Tiêu ', '').replace('Hắc Diệm ', '').replace('Bất Chu ', '').replace('Thanh Mộc ', '')}}
                          </span>
                        </button>
                      );
                    }})}}
                  </div>
                </div>
              )}}

              {{/* 3. Restart and Title Actions */}}"""

content = content.replace(old_row, wardrobe_section, 1)

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: StatusModal.tsx patched with wardrobe outfit selector!")
