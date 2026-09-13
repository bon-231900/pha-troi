import sqlite3
import json
from system.core.config import DB_PATH

class PlotGraphEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_hierarchy(self) -> list:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, node_type, parent_id, order_index, title, objective, conflict, stakes, pov, status FROM plot_nodes ORDER BY order_index")
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "node_type": r[1], "parent_id": r[2], "order_index": r[3],
            "title": r[4], "objective": r[5], "conflict": r[6], "stakes": r[7],
            "pov": r[8], "status": r[9]
        } for r in rows]

    def get_current_chapter_target(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, title, objective, conflict, stakes, pov, status FROM plot_nodes WHERE node_type = 'chapter' AND status IN ('PLANNED', 'DRAFTING') ORDER BY order_index ASC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "title": row[1], "objective": row[2], "conflict": row[3], "stakes": row[4], "pov": row[5], "status": row[6]}
        return {"id": "ch_001", "title": "Ch??ng 1", "objective": "B?t ??u", "pov": "Nguy?n Minh An"}
