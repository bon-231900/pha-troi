import os
import json
import sqlite3
from system.core.config import DB_PATH, CANON_DIR

class CanonEngine:
    LEVELS = ["LOCKED", "CONFIRMED", "PROVISIONAL", "UNKNOWN", "FORBIDDEN_ASSUMPTION", "PROPOSED"]

    FORBIDDEN_PATTERNS = [
        "chuy?n sinh", "h? th?ng", "huy?t m?ch", "thi?n m?nh chi t?",
        "minh an l? th?n", "minh an gi? y?u", "sau 3 ng?y", "l?m t?ch ?? ch?t",
        "h?i sinh", "xuy?n kh?ng", "b? ??o v? ??ch"
    ]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_canon(self, key: str) -> dict:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT id, category, key, title, content, level FROM canon_entries WHERE key = ?", (key,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "category": row[1], "key": row[2], "title": row[3], "content": row[4], "level": row[5]}
        return None

    def list_all_canon(self) -> list:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("SELECT id, category, key, title, content, level FROM canon_entries ORDER BY level, category")
        rows = cur.fetchall()
        conn.close()
        return [{"id": r[0], "category": r[1], "key": r[2], "title": r[3], "content": r[4], "level": r[5]} for r in rows]

    def validate_text_for_forbidden_assumptions(self, text: str) -> list:
        violations = []
        lower_text = text.lower()
        for pat in self.FORBIDDEN_PATTERNS:
            if pat in lower_text:
                violations.append(f"Ph?t hi?n suy di?n c?m k? (FORBIDDEN_ASSUMPTION): '{pat}'")
        return violations

    def propose_canon(self, key: str, title: str, content: str, category: str = "general") -> str:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        entry_id = f"CANON-PROP-{key}"
        cur.execute("""INSERT OR REPLACE INTO canon_entries (id, category, key, title, content, level, approved_by)
                       VALUES (?, ?, ?, ?, ?, 'PROPOSED', 'Pending Author')""", (entry_id, category, key, title, content))
        conn.commit()
        conn.close()
        return entry_id

    def lock_canon(self, key: str, author_name: str = "Author") -> bool:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("UPDATE canon_entries SET level = 'LOCKED', approved_by = ?, approved_at = CURRENT_TIMESTAMP WHERE key = ?", (author_name, key))
        conn.commit()
        updated = cur.rowcount > 0
        conn.close()
        return updated
