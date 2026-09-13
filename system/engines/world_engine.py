import sqlite3
import json
from system.core.config import DB_PATH

class WorldEngine:
    COSMOLOGY_RANKS = {
        1: "??i ??i Gi?i",
        2: "C?c V?c",
        3: "C?c Tinh H?i",
        4: "C?c V? Di?n",
        5: "Th? Gi?i",
        6: "Tr?i ??t"
    }

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_node(self, node_id: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT id, name, parent_id, cosmology_rank, cultivation_system, status, access_conditions, description FROM world_nodes WHERE id = ?", (node_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0], "name": row[1], "parent_id": row[2],
                "rank": row[3], "rank_name": self.COSMOLOGY_RANKS.get(row[3], "Kh?ng x?c ??nh"),
                "cultivation_system": row[4], "status": row[5],
                "access_conditions": row[6], "description": row[7]
            }
        return None

    def list_nodes(self) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT id, name, parent_id, cosmology_rank, cultivation_system, status, description FROM world_nodes ORDER BY cosmology_rank")
        rows = cur.fetchall()
        conn.close()
        return [{
            "id": r[0], "name": r[1], "parent_id": r[2], "rank": r[3],
            "rank_name": self.COSMOLOGY_RANKS.get(r[3]), "cultivation_system": r[4],
            "status": r[5], "description": r[6]
        } for r in rows]

    def validate_travel(self, source_id: str, target_id: str, elapsed_hours: float) -> tuple[bool, str]:
        # Ki?m tra th?i gian t?i thi?u h?p l? tr??c
        if elapsed_hours < 0:
            return False, "Th?i gian di chuy?n ?m l? b?t h?p l?."
        
        if source_id == target_id:
            return True, "C?ng m?t ??a ?i?m."
        
        # Ki?m tra n?u di chuy?n t? ngo?i v?o Tr?i ??t ho?c ng??c l?i
        if source_id == "node_trai_dat" or target_id == "node_trai_dat":
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cur = conn.cursor()
            cur.execute("SELECT status FROM world_nodes WHERE id = 'node_trai_dat'")
            row = cur.fetchone()
            conn.close()
            if row and row[0] == "SEALED":
                return False, "Tr?i ??t l? v? di?n b? phong ?n! C?m di chuy?n th?ng th??ng tr? khi c? s? ki?n ??c bi?t (nh? t?n h?n r?i)."

        return True, "H?p l?."
