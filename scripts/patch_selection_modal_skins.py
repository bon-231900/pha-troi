# -*- coding: utf-8 -*-
with open('frontend/src/components/CharacterSelectionModal.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_imp = "import { PLAYER_CLASSES, PlayerClassId } from '../game/rules';"
new_imp = "import { PLAYER_CLASSES, PlayerClassId, CHARACTER_SKINS, getSkinOrDefault } from '../game/rules';"
if old_imp not in content:
    old_imp = old_imp.replace("\n", "\r\n")
    new_imp = new_imp.replace("\n", "\r\n")
content = content.replace(old_imp, new_imp, 1)

# 2. Add outfit thumbnail display to profile card
old_card = """                    {/* Character Name in Handwriting Font */}
                    <div className="mb-2">
                      <h2
                        className="text-lg sm:text-xl font-bold text-amber-200 drop-shadow truncate"
                        style={{ fontFamily: "'Lora', Georgia, serif" }}
                      >
                        {profile.characterName}
                      </h2>
                      <div className="text-xs text-slate-400 font-tech mt-0.5">
                        {cls.sectTitle.split('·')[0].trim()}
                      </div>
                    </div>"""

clean_base = "${import.meta.env.BASE_URL || './'}"
new_card = f"""                    {{/* Character Name & Outfit Avatar Thumbnail */}}
                    <div className="flex items-center gap-3 mb-2.5">
                      {{(() => {{
                        const skin = getSkinOrDefault(profile.equippedSkinId, profile.classId);
                        return (
                          <>
                            <div className="w-12 h-16 rounded-xl overflow-hidden bg-slate-900 border border-slate-700/80 shrink-0 relative shadow">
                              <img
                                src={{`${clean_base}${{skin.cardPath}}`}}
                                alt={{skin.name}}
                                className="w-full h-full object-cover"
                              />
                              <span className="absolute bottom-0.5 right-1 text-[10px]">{{skin.icon}}</span>
                            </div>
                            <div className="min-w-0 flex-1">
                              <h2
                                className="text-base sm:text-lg font-bold text-amber-200 drop-shadow truncate"
                                style={{{{ fontFamily: "'Lora', Georgia, serif" }}}}
                              >
                                {{profile.characterName}}
                              </h2>
                              <div className="text-[11px] text-amber-400 font-tech font-semibold truncate">
                                {{skin.name}}
                              </div>
                              <div className="text-[10px] text-slate-400 font-tech truncate">
                                {{cls.sectTitle.split('·')[0].trim()}}
                              </div>
                            </div>
                          </>
                        );
                      }})()}}
                    </div>"""

if old_card not in content:
    old_card = old_card.replace("\n", "\r\n")
    new_card = new_card.replace("\n", "\r\n")
content = content.replace(old_card, new_card, 1)

with open('frontend/src/components/CharacterSelectionModal.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: CharacterSelectionModal.tsx patched with outfit avatar support!")
