# -*- coding: utf-8 -*-
import sqlite3
import json
from system.core.config import DB_PATH

class ForeshadowingEngine:
    STATUSES = ["PLANTED", "ACTIVE", "PARTIALLY_PAID", "PAID", "ABANDONED", "REDIRECTED", "RED_HERRING"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def plant_seed(self, seed_id: str, description: str, chapter_num: int, scene_num: int, notices: list, actual_meaning: str, payoff_chapter: int = None) -> str:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, 'PLANTED')""",
                    (seed_id, description, chapter_num, scene_num, json.dumps(notices, ensure_ascii=False), actual_meaning, payoff_chapter))
        conn.commit()
        conn.close()
        return seed_id

    def list_seeds(self, status: str = None) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        if status:
            cur.execute("SELECT id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status FROM foreshadowing_ledger WHERE status = ?", (status,))
        else:
            cur.execute("SELECT id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status FROM foreshadowing_ledger ORDER BY planted_chapter")
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "seed_description": r[1], "planted_chapter": r[2], "planted_scene": r[3],
            "notices": json.loads(r[4]) if r[4] else [], "actual_meaning": r[5],
            "payoff_chapter": r[6], "status": r[7]
        } for r in rows]

    def update_status(self, seed_id: str, new_status: str, payoff_chapter: int = None):
        if new_status not in self.STATUSES:
            raise ValueError(f"Trạng thái phục bút không hợp lệ: {new_status}")
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        if payoff_chapter:
            cur.execute("UPDATE foreshadowing_ledger SET status = ?, payoff_chapter = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, payoff_chapter, seed_id))
        else:
            cur.execute("UPDATE foreshadowing_ledger SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, seed_id))
        conn.commit()
        conn.close()

    def audit_dormant_seeds(self, current_chapter: int, threshold_chapters: int = 50) -> list:
        dormant = []
        for s in self.list_seeds():
            if s["status"] in ["PLANTED", "ACTIVE"] and (current_chapter - s["planted_chapter"] > threshold_chapters):
                dormant.append(f"DORMANT_FORESHADOWING: Phục bút '{s['seed_description']}' (Mã: {s['id']}) gieo từ chương {s['planted_chapter']} đã qua {current_chapter - s['planted_chapter']} chương chưa có động thái thu hồi!")
        return dormant
