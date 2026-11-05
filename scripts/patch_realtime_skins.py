# -*- coding: utf-8 -*-
with open('frontend/src/game/realtimeRoom.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update PeerPresence
content = content.replace(
    "slotIndex: number; // 0..17 (slots on panoramic terraces)\n  lastSeen: number;",
    "slotIndex: number; // 0..23 (slots on panoramic terraces)\n  skinId?: string;\n  lastSeen: number;"
).replace(
    "slotIndex: number; // 0..17 (slots on panoramic terraces)\r\n  lastSeen: number;",
    "slotIndex: number; // 0..23 (slots on panoramic terraces)\r\n  skinId?: string;\r\n  lastSeen: number;"
)

# 2. Add localSkinId to RealtimeRoomClient
old_props = "private localStance: StanceKey = 'Q';\n  private assignedSlotIndex: number = 1;"
new_props = "private localStance: StanceKey = 'Q';\n  private localSkinId: string = 'skin_default';\n  private assignedSlotIndex: number = 1;"
if old_props not in content:
    old_props = old_props.replace("\n", "\r\n")
    new_props = new_props.replace("\n", "\r\n")
content = content.replace(old_props, new_props, 1)

# 3. Update updateIdentity
old_id = "public updateIdentity(stance?: StanceKey, guildId?: string, name?: string) {"
new_id = "public updateIdentity(stance?: StanceKey, guildId?: string, name?: string, skinId?: string) {"
if old_id not in content:
    old_id = old_id.replace("\n", "\r\n")
    new_id = new_id.replace("\n", "\r\n")
content = content.replace(old_id, new_id, 1)

old_id_body = "if (stance) this.localStance = stance;\n    if (guildId) this.localGuildId = guildId;"
new_id_body = "if (stance) this.localStance = stance;\n    if (guildId) this.localGuildId = guildId;\n    if (skinId) this.localSkinId = skinId;"
if old_id_body not in content:
    old_id_body = old_id_body.replace("\n", "\r\n")
    new_id_body = new_id_body.replace("\n", "\r\n")
content = content.replace(old_id_body, new_id_body, 1)

# 4. Include skinId in broadcastPresence
old_pres = "stance: this.localStance,\n      slotIndex: this.assignedSlotIndex,\n      lastSeen: Date.now(),"
new_pres = "stance: this.localStance,\n      slotIndex: this.assignedSlotIndex,\n      skinId: this.localSkinId,\n      lastSeen: Date.now(),"
if old_pres not in content:
    old_pres = old_pres.replace("\n", "\r\n")
    new_pres = new_pres.replace("\n", "\r\n")
content = content.replace(old_pres, new_pres, 1)

with open('frontend/src/game/realtimeRoom.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: realtimeRoom.ts patched with skin support!")
