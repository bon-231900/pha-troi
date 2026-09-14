# -*- coding: utf-8 -*-
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
            raise ValueError(f"Trạng thái nhận thức không hợp lệ: {status}")
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""INSERT INTO knowledge_matrix (fact_key, statement, character_id, epistemic_status, chapter_num)
                       VALUES (?, ?, ?, ?, ?)""", (fact_key, statement, character_id, status, chapter_num))
        conn.commit()
        conn.close()

    def check_for_premature_knowledge_leak(self, character_id: str, text: str) -> list:
        """Kiểm tra xem nhân vật có nói hoặc nghĩ về những điều mà họ KHÔNG biết hay không."""
        violations = []
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("""
            SELECT k1.fact_key, k1.statement, k1.epistemic_status 
            FROM knowledge_matrix k1
            INNER JOIN (
                SELECT character_id, fact_key, MAX(id) AS max_id
                FROM knowledge_matrix
                WHERE character_id = ?
                GROUP BY character_id, fact_key
            ) latest ON k1.id = latest.max_id
            WHERE k1.epistemic_status IN ('UNKNOWN', 'FORGOTTEN')
        """, (character_id,))
        rows = cur.fetchall()
        conn.close()

        lower_text = text.lower()
        for f_key, stmt, status in rows:
            stmt_lower = stmt.lower()
            key_phrases = ["phong ấn", "vị diện", "cắt đứt", "tàn hồn", "thượng cổ", "khí huyết đạo"]
            matched_phrases = [p for p in key_phrases if p in stmt_lower and p in lower_text]
            if len(matched_phrases) >= 2 or (stmt_lower in lower_text):
                violations.append(f"KNOWLEDGE_LEAK: Nhân vật {character_id} đang phát ngôn/suy nghĩ về [{stmt}] trong khi trạng thái nhận thức là {status}!")
        return violations

    def check_author_secret_leak(self, text: str) -> list:
        """Kiểm tra tuyệt đối: Không để bí mật tác giả lọt vào văn bản draft."""
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
                if "chiến trường hạch tâm" in lower_text or "tần số ý chí không khuất phục" in lower_text:
                    leaks.append(f"CRITICAL_AUTHOR_SECRET_LEAK: Nội dung chứa từ khóa bí mật tác giả ({sec.get('id')})!")
        return leaks
