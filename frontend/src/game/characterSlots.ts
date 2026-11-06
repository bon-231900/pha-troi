import { safeStorage } from './storage';
import {
  PlayerClassId,
  PLAYER_CLASSES,
  INITIAL_STANCE_SKILLS,
  INITIAL_UPGRADES,
  INITIAL_SPIRIT_NODES,
  INITIAL_EQUIPPED_SLOTS,
  StanceSkillNode,
  SECT_DEFAULT_SKIN,
} from './rules';

export interface CharacterSlotProgress {
  bossHp?: number;
  linhThach: number;
  tinhHoa: number;
  upgrades: any[];
  spiritNodes: any[];
  stanceSkills: StanceSkillNode[];
  equippedItems: Record<string, any>;
  inventory: any[];
  playerTotalDamage: number;
  claimedMilestones: string[] | number[] | Record<string | number, boolean>;
  currentVaultId: number;
  userGuildId?: string | null;
  guildHearths?: Record<string, any>;
  serverFurnaceHeat?: number;
  serverAnvilHp?: number;
  raidContributionScore?: number;
  equippedSkinId?: string;
  lastActiveTimestamp: number;
}

export interface CharacterProfile {
  slotId: 1 | 2 | 3;
  characterName: string;
  classId: PlayerClassId;
  createdAt: number;
  lastPlayedAt: number;
  level: number;
  equippedSkinId?: string;
  progress: CharacterSlotProgress;
}

export const MAX_CHARACTER_SLOTS = 3;

function getSlotStorageKey(googleId?: string): string {
  return googleId ? `phatroi_characters_acc_${googleId}` : 'phatroi_characters_guest';
}

function getActiveSlotStorageKey(googleId?: string): string {
  return googleId ? `phatroi_active_slot_acc_${googleId}` : 'phatroi_active_slot_guest';
}

/**
 * Migration helper: If user has a single legacy save, wrap it into Slot 1
 */
function checkAndMigrateLegacySave(googleId?: string): (CharacterProfile | null)[] | null {
  try {
    const legacyKey = googleId ? `phatroi_account_${googleId}` : 'phatroi_guest_save';
    const legacyStr = safeStorage.getItem(legacyKey) || (!googleId ? safeStorage.getItem('phatroi_save_v6') : null);

    if (!legacyStr) return null;

    const parsed = JSON.parse(legacyStr);
    if (!parsed || typeof parsed !== 'object') return null;

    const savedClass = (parsed.playerClassId || safeStorage.getItem('phatroi_player_class') || 'thunder') as PlayerClassId;
    const validClassId = PLAYER_CLASSES[savedClass] ? savedClass : 'thunder';

    const savedName = safeStorage.getItem('phatroi_user_name') || 'Thợ Rèn Tiêu Dao';

    const slot1: CharacterProfile = {
      slotId: 1,
      characterName: savedName,
      classId: validClassId,
      createdAt: parsed.lastActiveTimestamp || Date.now(),
      lastPlayedAt: parsed.lastActiveTimestamp || Date.now(),
      level: Math.max(1, Math.floor(Math.sqrt((parsed.playerTotalDamage || 0) / 10000)) + 1),
      progress: {
        bossHp: parsed.bossHp,
        linhThach: parsed.linhThach || 0,
        tinhHoa: parsed.tinhHoa || 0,
        upgrades: Array.isArray(parsed.upgrades) ? parsed.upgrades : INITIAL_UPGRADES,
        spiritNodes: Array.isArray(parsed.spiritNodes) ? parsed.spiritNodes : INITIAL_SPIRIT_NODES,
        stanceSkills: Array.isArray(parsed.stanceSkills) && parsed.stanceSkills.length === INITIAL_STANCE_SKILLS.length
          ? parsed.stanceSkills
          : INITIAL_STANCE_SKILLS,
        equippedItems: parsed.equippedItems && typeof parsed.equippedItems === 'object' ? parsed.equippedItems : INITIAL_EQUIPPED_SLOTS,
        inventory: Array.isArray(parsed.inventory) ? parsed.inventory : [],
        playerTotalDamage: parsed.playerTotalDamage || 0,
        claimedMilestones: Array.isArray(parsed.claimedMilestones) ? parsed.claimedMilestones : [],
        currentVaultId: typeof parsed.currentVaultId === 'number' ? parsed.currentVaultId : 1,
        userGuildId: parsed.userGuildId || null,
        guildHearths: parsed.guildHearths || [],
        serverFurnaceHeat: parsed.serverFurnaceHeat || 3000,
        serverAnvilHp: parsed.serverAnvilHp || 10000,
        raidContributionScore: parsed.raidContributionScore || 0,
        lastActiveTimestamp: parsed.lastActiveTimestamp || Date.now(),
      },
    };

    const initialSlots: (CharacterProfile | null)[] = [slot1, null, null];
    const key = getSlotStorageKey(googleId);
    safeStorage.setItem(key, JSON.stringify(initialSlots));
    safeStorage.setItem(getActiveSlotStorageKey(googleId), '1');

    return initialSlots;
  } catch (err) {
    console.warn('Legacy save migration error:', err);
    return null;
  }
}

/**
 * Load 3 character slots for the active account/guest
 */
export function loadCharacterSlots(googleId?: string): (CharacterProfile | null)[] {
  try {
    const key = getSlotStorageKey(googleId);
    const stored = safeStorage.getItem(key);

    if (stored) {
      const parsed = JSON.parse(stored);
      if (Array.isArray(parsed) && parsed.length === MAX_CHARACTER_SLOTS) {
        // Sanitize and self-heal any corrupted slots from previous versions
        let dirty = false;
        for (const slot of parsed) {
          if (slot && slot.progress) {
            if (
              !Array.isArray(slot.progress.stanceSkills) ||
              slot.progress.stanceSkills.length !== INITIAL_STANCE_SKILLS.length
            ) {
              slot.progress.stanceSkills = INITIAL_STANCE_SKILLS;
              dirty = true;
            }
            if (!Array.isArray(slot.progress.upgrades) || slot.progress.upgrades.length === 0) {
              slot.progress.upgrades = INITIAL_UPGRADES;
              dirty = true;
            }
            if (!Array.isArray(slot.progress.spiritNodes) || slot.progress.spiritNodes.length === 0) {
              slot.progress.spiritNodes = INITIAL_SPIRIT_NODES;
              dirty = true;
            }
            if (!slot.progress.equippedItems || typeof slot.progress.equippedItems !== 'object') {
              slot.progress.equippedItems = INITIAL_EQUIPPED_SLOTS;
              dirty = true;
            }
          }
        }
        if (dirty) {
          saveAllCharacterSlots(parsed, googleId);
        }
        return parsed;
      }
    }

    // Try migration from legacy save if exists
    const migrated = checkAndMigrateLegacySave(googleId);
    if (migrated) return migrated;

    // Default 3 empty slots
    const emptySlots: (CharacterProfile | null)[] = [null, null, null];
    safeStorage.setItem(key, JSON.stringify(emptySlots));
    return emptySlots;
  } catch (err) {
    console.error('Failed to load character slots:', err);
    return [null, null, null];
  }
}

/**
 * Save updated slot list
 */
export function saveAllCharacterSlots(slots: (CharacterProfile | null)[], googleId?: string): void {
  try {
    const key = getSlotStorageKey(googleId);
    safeStorage.setItem(key, JSON.stringify(slots));
  } catch (err) {
    console.error('Failed to save character slots:', err);
  }
}

/**
 * Get active slot ID (1, 2, or 3)
 */
export function getActiveSlotId(googleId?: string): 1 | 2 | 3 {
  try {
    const key = getActiveSlotStorageKey(googleId);
    const val = safeStorage.getItem(key);
    if (val === '2') return 2;
    if (val === '3') return 3;
    return 1;
  } catch {
    return 1;
  }
}

/**
 * Set active slot ID
 */
export function setActiveSlotId(slotId: 1 | 2 | 3, googleId?: string): void {
  try {
    const key = getActiveSlotStorageKey(googleId);
    safeStorage.setItem(key, String(slotId));
  } catch (err) {
    console.error('Failed to set active slot:', err);
  }
}

/**
 * Create a new character in a specified slot
 */
export function createCharacterInSlot(
  slotId: 1 | 2 | 3,
  characterName: string,
  classId: PlayerClassId,
  googleId?: string,
  skinId?: string
): CharacterProfile {
  const slots = loadCharacterSlots(googleId);

  const finalSkinId = skinId || SECT_DEFAULT_SKIN[classId] || 'skin_default';
  const newProfile: CharacterProfile = {
    slotId,
    characterName: characterName.trim() || `Thợ Rèn #${Math.floor(Math.random() * 8999 + 1000)}`,
    classId,
    equippedSkinId: finalSkinId,
    createdAt: Date.now(),
    lastPlayedAt: Date.now(),
    level: 1,
    progress: {
      bossHp: 1500000000,
      linhThach: 0,
      tinhHoa: 0,
      upgrades: INITIAL_UPGRADES,
      spiritNodes: INITIAL_SPIRIT_NODES,
      stanceSkills: INITIAL_STANCE_SKILLS,
      equippedItems: INITIAL_EQUIPPED_SLOTS,
      inventory: [],
      playerTotalDamage: 0,
      claimedMilestones: [],
      currentVaultId: 1,
      userGuildId: null,
      guildHearths: [],
      serverFurnaceHeat: 3500,
      serverAnvilHp: 10000,
      raidContributionScore: 0,
      equippedSkinId: finalSkinId,
      lastActiveTimestamp: Date.now(),
    },
  };

  slots[slotId - 1] = newProfile;
  saveAllCharacterSlots(slots, googleId);
  setActiveSlotId(slotId, googleId);

  // Sync to legacy name/class keys for compatibility
  safeStorage.setItem('phatroi_user_name', newProfile.characterName);
  safeStorage.setItem('phatroi_player_class', classId);

  return newProfile;
}

/**
 * Delete a character from a slot
 */
export function deleteCharacterSlot(slotId: 1 | 2 | 3, googleId?: string): void {
  const slots = loadCharacterSlots(googleId);
  slots[slotId - 1] = null;
  saveAllCharacterSlots(slots, googleId);

  // If deleted the active slot, switch to the first occupied slot or slot 1
  const activeId = getActiveSlotId(googleId);
  if (activeId === slotId) {
    const nextSlot = slots.findIndex((s) => s !== null);
    if (nextSlot !== -1) {
      setActiveSlotId((nextSlot + 1) as 1 | 2 | 3, googleId);
    } else {
      setActiveSlotId(1, googleId);
    }
  }
}

/**
 * Update the active slot's progression payload
 */
export function updateActiveSlotProgress(
  slotId: 1 | 2 | 3,
  progressPatch: Partial<CharacterSlotProgress>,
  googleId?: string
): void {
  const slots = loadCharacterSlots(googleId);
  const current = slots[slotId - 1];
  if (!current) return;

  current.lastPlayedAt = Date.now();
  current.progress = {
    ...current.progress,
    ...progressPatch,
    lastActiveTimestamp: Date.now(),
  };

  // Re-calculate level based on total damage
  current.level = Math.max(1, Math.floor(Math.sqrt((current.progress.playerTotalDamage || 0) / 10000)) + 1);

  slots[slotId - 1] = current;
  saveAllCharacterSlots(slots, googleId);
}


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
