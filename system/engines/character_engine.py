# -*- coding: utf-8 -*-
import sqlite3
import json
import os
from system.core.config import DB_PATH, ROOT_DIR

class CharacterEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_character(self, character_id: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT id, name, type, aliases, status, metadata_json FROM entities WHERE id = ? AND type = 'character'", (character_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return None
        
        char_info = {
            "id": row[0], "name": row[1], "type": row[2],
            "aliases": json.loads(row[3]) if row[3] else [],
            "status": row[4],
            "metadata": json.loads(row[5]) if row[5] else {}
        }
        
        char_json_file = os.path.join(ROOT_DIR, "canon", "characters", f"{character_id.replace('char_', '')}.json")
        if os.path.exists(char_json_file):
            with open(char_json_file, "r", encoding="utf-8") as f:
                extra = json.load(f)
                char_info.update(extra)

        cur.execute("""SELECT chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state
                       FROM character_states WHERE character_id = ? ORDER BY chapter_num DESC LIMIT 1""", (character_id,))
        st = cur.fetchone()
        conn.close()
        if st:
            char_info["latest_state"] = {
                "chapter_num": st[0], "location_id": st[1], "cultivation_realm": st[2],
                "physical_condition": st[3], "injuries": json.loads(st[4]) if st[4] else [],
                "inventory": json.loads(st[5]) if st[5] else [], "emotional_state": st[6]
            }
        return char_info

    def update_state(self, character_id: str, chapter_num: int, location_id: str, realm: str, condition: str, injuries: list, inventory: list, emotion: str):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (character_id, chapter_num, location_id, realm, condition, json.dumps(injuries, ensure_ascii=False), json.dumps(inventory, ensure_ascii=False), emotion))
        conn.commit()
        conn.close()

    def mark_dead(self, character_id: str, chapter_num: int, reason: str):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("UPDATE entities SET status = 'DEAD', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (character_id,))
        cur.execute("""INSERT INTO audit_log (action_type, description, details_json)
                       VALUES ('CHARACTER_DEATH', ?, ?)""", (f"Nhân vật {character_id} đã chết tại chương {chapter_num}", json.dumps({"reason": reason}, ensure_ascii=False)))
        conn.commit()
        conn.close()

    def is_alive(self, character_id: str) -> bool:
        char = self.get_character(character_id)
        return char and char.get("status") != "DEAD"
