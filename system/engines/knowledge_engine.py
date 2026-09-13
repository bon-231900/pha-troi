import sqlite3
import json
import os
from system.core.config import DB_PATH, AUTHOR_SECRET_DIR

class KnowledgeEngine:
    EPISTEMIC_STATES = ["KNOWN", "SUSPECTED", "BELIEVED", "MISUNDERSTOOD", "FALSE_BELIEF", "UNKNOWN", "FORGOTTEN"]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_character_epistemic_status(self, character_id: str, fact_key: str) -> str:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""SELECT epistemic_status FROM knowledge_matrix 
                       WHERE character_id = ? AND fact_key = ? ORDER BY chapter_num DESC, id DESC LIMIT 1""", (character_id, fact_key))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else "UNKNOWN"

    def set_character_epistemic_status(self, character_id: str, fact_key: str, statement: str, status: str, chapter_num: int):
        if status not in self.EPISTEMIC_STATES:
            raise ValueError(f"Invalid epistemic status: {status}")
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT INTO knowledge_matrix (fact_key, statement, character_id, epistemic_status, chapter_num)
                       VALUES (?, ?, ?, ?, ?)""", (fact_key, statement, character_id, status, chapter_num))
        conn.commit()
        conn.close()

    def check_for_premature_knowledge_leak(self, character_id: str, text: str) -> list:
        """Ki?m tra xem nh?n v?t c? n?i ho?c ngh? v? nh?ng ?i?u m? h? KH?NG bi?t hay kh?ng."""
        violations = []
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""SELECT fact_key, statement, epistemic_status FROM knowledge_matrix 
                       WHERE character_id = ? AND epistemic_status IN ('UNKNOWN', 'FORGOTTEN')""", (character_id,))
        rows = cur.fetchall()
        conn.close()

        lower_text = text.lower()
        for f_key, stmt, status in rows:
            # Ki?m tra c?m t? ho?c t? kh?a quan tr?ng
            stmt_lower = stmt.lower()
            key_phrases = ["phong ?n", "v? di?n", "c?t ??t", "t?n h?n", "th??ng c?", "kh? huy?t ??o"]
            matched_phrases = [p for p in key_phrases if p in stmt_lower and p in lower_text]
            if len(matched_phrases) >= 2 or (stmt_lower in lower_text):
                violations.append(f"KNOWLEDGE_LEAK: Nh?n v?t {character_id} ?ang ph?t ng?n/suy ngh? v? [{stmt}] trong khi tr?ng th?i nh?n th?c l? {status}!")
        return violations

    def check_author_secret_leak(self, text: str) -> list:
        """Ki?m tra tuy?t ??i: Kh?ng ?? b? m?t t?c gi? l?t v?o v?n b?n draft."""
        leaks = []
        secret_file = os.path.join(AUTHOR_SECRET_DIR, "secrets.json")
        if not os.path.exists(secret_file):
            return leaks
        with open(secret_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        secrets = data.get("secrets", [])
        lower_text = text.lower()
        for sec in secrets:
            if sec.get("status") == "LOCKED":
                if "chi?n tr??ng h?ch t?m" in lower_text or "t?n s? ? ch? kh?ng khu?t ph?c" in lower_text:
                    leaks.append(f"CRITICAL_AUTHOR_SECRET_LEAK: N?i dung ch?a t? kh?a b? m?t t?c gi? ({sec.get('id')})!")
        return leaks
