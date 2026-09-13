# -*- coding: utf-8 -*-
import os
import json
import sqlite3
from system.core.config import DB_PATH, CANON_DIR

class ContextBuilder:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def build_context_pack(self, chapter_num: int, pov: str, active_characters: list, location_id: str) -> dict:
        """Tạo gói ngữ cảnh tinh gọn (Context Pack) tối ưu ngân sách token, cách ly tuyệt đối AUTHOR_SECRET."""
        pack = {
            "chapter_num": chapter_num,
            "pov": pov,
            "location_id": location_id,
            "canon_summary": [],
            "character_states": {},
            "epistemic_knowledge": {},
            "active_foreshadowing": [],
            "recent_events": [],
            "style_constraints": [
                "Modern Cinematic: Giàu hình ảnh, nhịp phim, không gian rõ ràng, thoại tự nhiên đời thực.",
                "Literary Depth: Khắc họa nội tâm, kết cấu cảm xúc sâu, có ý nghĩa nhân sinh.",
                "Mature Dark Fantasy: Nghiêm túc, tàn khốc khi cần, không lạm dụng bạo lực vô nghĩa.",
                "Vietnam 2026: Đời thường TP.HCM, kẹt xe, thời tiết, căn hộ, thói quen sinh hoạt thực tế.",
                "Không dump lore! Mọi thông tin mở ra qua hành động, quan sát và đối thoại.",
                "Minh An 100% là người bình thường. Cấm mọi suy diễn gian lận/hệ thống/chuyển sinh."
            ]
        }

        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()

        cur.execute("SELECT key, title, content FROM canon_entries WHERE level IN ('LOCKED', 'CONFIRMED')")
        for row in cur.fetchall():
            pack["canon_summary"].append(f"[{row[0]}] {row[1]}: {row[2]}")

        for cid in active_characters:
            cur.execute("""SELECT cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state
                           FROM character_states WHERE character_id = ? ORDER BY chapter_num DESC LIMIT 1""", (cid,))
            st = cur.fetchone()
            if st:
                pack["character_states"][cid] = {
                    "realm": st[0], "condition": st[1],
                    "injuries": json.loads(st[2]) if st[2] else [],
                    "inventory": json.loads(st[3]) if st[3] else [],
                    "emotion": st[4]
                }

        for cid in active_characters:
            cur.execute("SELECT statement, epistemic_status FROM knowledge_matrix WHERE character_id = ?", (cid,))
            knows = cur.fetchall()
            pack["epistemic_knowledge"][cid] = {k[0]: k[1] for k in knows}

        cur.execute("SELECT id, seed_description, actual_meaning FROM foreshadowing_ledger WHERE status IN ('PLANTED', 'ACTIVE')")
        for r in cur.fetchall():
            pack["active_foreshadowing"].append({"id": r[0], "seed": r[1], "meaning": r[2]})

        cur.execute("SELECT title, summary FROM timeline_events ORDER BY chapter_num DESC, scene_num DESC LIMIT 3")
        for r in cur.fetchall():
            pack["recent_events"].append(f"{r[0]}: {r[1]}")

        conn.close()
        return pack
