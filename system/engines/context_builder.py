import os
import json
import sqlite3
from system.core.config import DB_PATH, CANON_DIR

class ContextBuilder:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def build_context_pack(self, chapter_num: int, pov: str, active_characters: list, location_id: str) -> dict:
        """T?o g?i ng? c?nh tinh g?n (Context Pack) t?i ?u ng?n s?ch token, c?ch ly tuy?t ??i AUTHOR_SECRET."""
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
                "Modern Cinematic: Gi?u h?nh ?nh, nh?p phim, kh?ng gian r? r?ng, tho?i t? nhi?n ??i th?c.",
                "Literary Depth: Kh?c h?a n?i t?m, k?t c?u c?m x?c s?u, c? ? ngh?a nh?n sinh.",
                "Mature Dark Fantasy: Nghi?m t?c, t?n kh?c khi c?n, kh?ng l?m d?ng b?o l?c v? ngh?a.",
                "Vietnam 2026: ??i th??ng TP.HCM, k?t xe, th?i ti?t, c?n h?, th?i quen sinh ho?t th?c t?.",
                "Kh?ng dump lore! M?i th?ng tin m? ra qua h?nh ??ng, quan s?t v? ??i tho?i.",
                "Minh An 100% l? ng??i b?nh th??ng. C?m m?i suy di?n gian l?n/h? th?ng/chuy?n sinh."
            ]
        }

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # 1. Canon t?m t?t
        cur.execute("SELECT key, title, content FROM canon_entries WHERE level IN ('LOCKED', 'CONFIRMED')")
        for row in cur.fetchall():
            pack["canon_summary"].append(f"[{row[0]}] {row[1]}: {row[2]}")

        # 2. Tr?ng th?i c?c nh?n v?t tham gia
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

        # 3. Ma tr?n nh?n th?c cho c?c nh?n v?t n?y
        for cid in active_characters:
            cur.execute("SELECT statement, epistemic_status FROM knowledge_matrix WHERE character_id = ?", (cid,))
            knows = cur.fetchall()
            pack["epistemic_knowledge"][cid] = {k[0]: k[1] for k in knows}

        # 4. Foreshadowing ?ang ho?t ??ng
        cur.execute("SELECT id, seed_description, actual_meaning FROM foreshadowing_ledger WHERE status IN ('PLANTED', 'ACTIVE')")
        for r in cur.fetchall():
            pack["active_foreshadowing"].append({"id": r[0], "seed": r[1], "meaning": r[2]})

        # 5. S? ki?n g?n nh?t
        cur.execute("SELECT title, summary FROM timeline_events ORDER BY chapter_num DESC, scene_num DESC LIMIT 3")
        for r in cur.fetchall():
            pack["recent_events"].append(f"{r[0]}: {r[1]}")

        conn.close()
        return pack
