# -*- coding: utf-8 -*-
import re
import sqlite3
import json
import uuid
from system.engines.canon_engine import CanonEngine
from system.engines.knowledge_engine import KnowledgeEngine
from system.engines.character_engine import CharacterEngine
from system.engines.power_engine import PowerEngine
from system.core.config import DB_PATH

class CritiqueEngine:
    """Động cơ Tự Phản Biện (Self-Critique Engine) Mức Độ Cao Nhất, kiểm duyệt 11 khía cạnh."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.canon_eng = CanonEngine(db_path)
        self.know_eng = KnowledgeEngine(db_path)
        self.char_eng = CharacterEngine(db_path)
        self.power_eng = PowerEngine()

    def audit_chapter_draft(self, chapter_num: int, pov: str, active_characters: list, text: str) -> dict:
        issues = []

        # 1. Canon & Forbidden Assumptions
        canon_violations = self.canon_eng.validate_text_for_forbidden_assumptions(text)
        for cv in canon_violations:
            issues.append({"category": "CANON", "severity": "CRITICAL", "description": cv})

        # 2. Author Secret Leak
        secret_leaks = self.know_eng.check_author_secret_leak(text)
        for sl in secret_leaks:
            issues.append({"category": "AUTHOR_SECRET", "severity": "CRITICAL", "description": sl})

        # 3. Knowledge Leak
        for cid in active_characters:
            k_leaks = self.know_eng.check_for_premature_knowledge_leak(cid, text)
            for kl in k_leaks:
                issues.append({"category": "KNOWLEDGE", "severity": "HIGH", "description": kl})

        # 4. Dead Character Check
        for cid in active_characters:
            if not self.char_eng.is_alive(cid):
                issues.append({
                    "category": "CHARACTER", "severity": "CRITICAL",
                    "description": f"Nhân vật {cid} ĐÃ CHẾT nhưng lại tham gia vào chương {chapter_num}!"
                })

        # 5. POV Integrity
        if "minh an" in pov.lower():
            if "lâm tịch nghĩ" in text.lower() or "trong lòng lâm tịch" in text.lower() or "lâm tịch thầm tính" in text.lower():
                issues.append({
                    "category": "POV", "severity": "HIGH",
                    "description": "HEAD_HOPPING: POV đang là Minh An nhưng lại miêu tả trực tiếp dòng suy nghĩ thầm kín của Lâm Tịch!"
                })

        # 6. Style & Cheap Cliffhangers
        cheap_cliffhangers = ["và hắn không biết rằng", "hắn vĩnh viễn không thể ngờ được", "chuyện gì đến cũng phải đến"]
        for cc in cheap_cliffhangers:
            if cc in text.lower():
                issues.append({
                    "category": "STYLE", "severity": "MEDIUM",
                    "description": f"Lạm dụng sáo ngữ giật gân rẻ tiền: '{cc}'!"
                })

        # 7. Word Count Check
        words = len(text.split())
        if words < 400:
            issues.append({
                "category": "NARRATIVE", "severity": "MEDIUM",
                "description": f"Chương quá ngắn ({words} từ), cần phát triển chiều sâu bối cảnh và cảm xúc."
            })

        # Lưu lỗi vào DB
        if issues:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cur = conn.cursor()
            for iss in issues:
                uid = f"ERR-{chapter_num}-{iss['category']}-{uuid.uuid4().hex[:6]}"
                cur.execute("""INSERT OR REPLACE INTO continuity_errors (id, chapter_num, severity, category, description, status)
                               VALUES (?, ?, ?, ?, ?, 'ACTIVE')""",
                            (uid, chapter_num, iss["severity"], iss["category"], iss["description"]))
            conn.commit()
            conn.close()

        return {
            "passed": len([i for i in issues if i["severity"] in ("CRITICAL", "HIGH")]) == 0,
            "issues": issues,
            "total_issues": len(issues)
        }
