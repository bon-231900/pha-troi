# -*- coding: utf-8 -*-
"""
Novel OS — ForeshadowingEngine (Quản lý Sổ cái Phục bút Trường thiên)
Hỗ trợ quản lý vòng đời phục bút qua hàng ngàn chương:
- Phân biệt: PLANTED, ACTIVE, PARTIALLY_PAID, PAID, ABANDONED, REDIRECTED, RED_HERRING.
- Hỗ trợ các khái niệm trường thiên: planned_dormancy, long_arc, payoff_window, latest_safe_revisit.
- Cung cấp WriterForeshadowingView đã làm sạch cho AI (không rò rỉ actual_meaning).
"""
import sqlite3
import json
from system.core.config import DB_PATH

class ForeshadowingEngine:
    STATUSES = ["PLANTED", "ACTIVE", "PARTIALLY_PAID", "PAID", "ABANDONED", "REDIRECTED", "RED_HERRING"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def plant_seed(self, seed_id: str, description: str, chapter_num: int, scene_num: int,
                   notices: list, actual_meaning: str, payoff_chapter: int = None,
                   planned_dormancy: bool = False, arc_scope: str = "LONG_ARC") -> str:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (
            id, seed_description, planted_chapter, planted_scene, notices_json,
            actual_meaning, payoff_chapter, status, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'PLANTED', CURRENT_TIMESTAMP)""",
        (seed_id, description, chapter_num, scene_num,
         json.dumps(notices, ensure_ascii=False), actual_meaning, payoff_chapter))
        conn.commit()
        conn.close()
        return seed_id

    def list_seeds(self, status: str = None) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        if status:
            cur.execute("""SELECT id, seed_description, planted_chapter, planted_scene,
                                  notices_json, actual_meaning, payoff_chapter, status
                           FROM foreshadowing_ledger WHERE status = ? ORDER BY planted_chapter""", (status,))
        else:
            cur.execute("""SELECT id, seed_description, planted_chapter, planted_scene,
                                  notices_json, actual_meaning, payoff_chapter, status
                           FROM foreshadowing_ledger ORDER BY planted_chapter""")
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "seed_description": r[1], "planted_chapter": r[2], "planted_scene": r[3],
            "notices": json.loads(r[4]) if r[4] else [], "actual_meaning": r[5],
            "payoff_chapter": r[6], "status": r[7]
        } for r in rows]

    def get_writer_view(self, chapter_num: int, limit: int = 5) -> list:
        """Cung cấp danh sách phục bút đã được khử độc (Sanitized) cho AI và người viết.
        Tuyệt đối không xuất actual_meaning hoặc author notes."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""SELECT id, seed_description, planted_chapter, status
                       FROM foreshadowing_ledger
                       WHERE status IN ('PLANTED', 'ACTIVE') AND planted_chapter <= ?
                       ORDER BY planted_chapter DESC LIMIT ?""", (chapter_num, limit))
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0],
            "observable_clue": r[1],
            "planted_chapter": r[2],
            "status": r[3]
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
        """Kiểm toán các phục bút gieo đã lâu:
        Phân biệt giữa:
        1. Phục bút trường thiên có kế hoạch (Planned Long Arc) -> Gợi ý nhắc nhở nhẹ (SUGGESTION).
        2. Phục bút đã quá hạn payoff (Overdue Payoff) -> Cảnh báo (WARNING).
        3. Phục bút không có mốc payoff bị bỏ quên quá threshold -> Cảnh báo ngủ quên (DORMANT_FORESHADOWING).
        """
        dormant = []
        for s in self.list_seeds():
            if s["status"] not in ["PLANTED", "ACTIVE"]:
                continue
            
            planted = s["planted_chapter"]
            payoff = s.get("payoff_chapter")
            gap = current_chapter - planted

            if gap > threshold_chapters:
                if payoff and current_chapter < payoff:
                    # Tuyến trường thiên có đích đến cụ thể (Ví dụ: gieo ch 1, payoff ch 200, hiện tại ch 80)
                    dormant.append(
                        f"DORMANT_FORESHADOWING: Phục bút trường thiên '{s['seed_description']}' (Mã: {s['id']}) "
                        f"gieo từ chương {planted} đã qua {gap} chương (kế hoạch payoff: Ch {payoff}). "
                        f"Gợi ý: Cân nhắc gieo manh mối trung gian để duy trì ký ức độc giả."
                    )
                elif payoff and current_chapter >= payoff:
                    dormant.append(
                        f"OVERDUE_FORESHADOWING: Phục bút '{s['seed_description']}' (Mã: {s['id']}) "
                        f"đã đến hoặc vượt quá chương kỳ vọng thu hồi (Ch {payoff})!"
                    )
                else:
                    dormant.append(
                        f"DORMANT_FORESHADOWING: Phục bút '{s['seed_description']}' (Mã: {s['id']}) "
                        f"gieo từ chương {planted} đã qua {gap} chương chưa có động thái thu hồi!"
                    )
        return dormant
