# -*- coding: utf-8 -*-
with open('frontend/src/game/characterSlots.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports to include SECT_DEFAULT_SKIN
old_imp = "import {\n  PlayerClassId,\n  PLAYER_CLASSES,\n  INITIAL_STANCE_SKILLS,\n  INITIAL_UPGRADES,\n  INITIAL_SPIRIT_NODES,\n  INITIAL_EQUIPPED_SLOTS,\n  StanceSkillNode,\n} from './rules';"
if old_imp not in content:
    old_imp = "import {\r\n  PlayerClassId,\r\n  PLAYER_CLASSES,\r\n  INITIAL_STANCE_SKILLS,\r\n  INITIAL_UPGRADES,\r\n  INITIAL_SPIRIT_NODES,\r\n  INITIAL_EQUIPPED_SLOTS,\r\n  StanceSkillNode,\r\n} from './rules';"

new_imp = old_imp.replace("StanceSkillNode,", "StanceSkillNode,\n  SECT_DEFAULT_SKIN,")
content = content.replace(old_imp, new_imp, 1)

# 2. Add equippedSkinId to interfaces
content = content.replace(
    "raidContributionScore?: number;\n  lastActiveTimestamp: number;\n}",
    "raidContributionScore?: number;\n  equippedSkinId?: string;\n  lastActiveTimestamp: number;\n}"
).replace(
    "raidContributionScore?: number;\r\n  lastActiveTimestamp: number;\r\n}",
    "raidContributionScore?: number;\r\n  equippedSkinId?: string;\r\n  lastActiveTimestamp: number;\r\n}"
)

content = content.replace(
    "level: number;\n  progress: CharacterSlotProgress;\n}",
    "level: number;\n  equippedSkinId?: string;\n  progress: CharacterSlotProgress;\n}"
).replace(
    "level: number;\r\n  progress: CharacterSlotProgress;\r\n}",
    "level: number;\r\n  equippedSkinId?: string;\r\n  progress: CharacterSlotProgress;\r\n}"
)

# 3. Update createCharacterInSlot signature and implementation
old_create = """export function createCharacterInSlot(
  slotId: 1 | 2 | 3,
  characterName: string,
  classId: PlayerClassId,
  googleId?: string
): CharacterProfile {"""

new_create = """export function createCharacterInSlot(
  slotId: 1 | 2 | 3,
  characterName: string,
  classId: PlayerClassId,
  googleId?: string,
  skinId?: string
): CharacterProfile {"""

if old_create not in content:
    old_create = old_create.replace("\n", "\r\n")
    new_create = new_create.replace("\n", "\r\n")

content = content.replace(old_create, new_create, 1)

old_newprofile = """  const newProfile: CharacterProfile = {
    slotId,
    characterName: characterName.trim() || `Thợ Rèn #${Math.floor(Math.random() * 8999 + 1000)}`,
    classId,
    createdAt: Date.now(),
    lastPlayedAt: Date.now(),
    level: 1,"""

new_newprofile = """  const finalSkinId = skinId || SECT_DEFAULT_SKIN[classId] || 'skin_default';
  const newProfile: CharacterProfile = {
    slotId,
    characterName: characterName.trim() || `Thợ Rèn #${Math.floor(Math.random() * 8999 + 1000)}`,
    classId,
    equippedSkinId: finalSkinId,
    createdAt: Date.now(),
    lastPlayedAt: Date.now(),
    level: 1,"""

if old_newprofile not in content:
    old_newprofile = old_newprofile.replace("\n", "\r\n")
    new_newprofile = new_newprofile.replace("\n", "\r\n")

content = content.replace(old_newprofile, new_newprofile, 1)

# Add equippedSkinId into newProfile.progress
old_prog_tail = """      raidContributionScore: 0,
      lastActiveTimestamp: Date.now(),
    },
  };"""

new_prog_tail = """      raidContributionScore: 0,
      equippedSkinId: finalSkinId,
      lastActiveTimestamp: Date.now(),
    },
  };"""

if old_prog_tail not in content:
    old_prog_tail = old_prog_tail.replace("\n", "\r\n")
    new_prog_tail = new_prog_tail.replace("\n", "\r\n")

content = content.replace(old_prog_tail, new_prog_tail, 1)

# Add updateCharacterSkinInSlot helper function at end of file
helper = """

/**
 * Update equipped skin for a character in slot
 */
export function updateCharacterSkinInSlot(
  slotId: 1 | 2 | 3,
  skinId: string,
  googleId?: string
): void {
  try {
    const slots = loadCharacterSlots(googleId);
    const profile = slots[slotId - 1];
    if (profile) {
      profile.equippedSkinId = skinId;
      if (profile.progress) {
        profile.progress.equippedSkinId = skinId;
      }
      saveAllCharacterSlots(slots, googleId);
    }
  } catch (err) {
    console.error('Failed to update character skin in slot:', err);
  }
}
"""
content += helper

with open('frontend/src/game/characterSlots.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: characterSlots.ts patched with skin support!")
