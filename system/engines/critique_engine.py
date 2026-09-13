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
    """??ng c? T? Ph?n Bi?n (Self-Critique Engine) M?c ?? Cao Nh?t, ki?m duy?t 11 kh?a c?nh."""

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

        # 2. Author Secret Leak (Tuy?t ??i kh?ng r? r?)
        secret_leaks = self.know_eng.check_author_secret_leak(text)
        for sl in secret_leaks:
            issues.append({"category": "AUTHOR_SECRET", "severity": "CRITICAL", "description": sl})

        # 3. Knowledge Leak theo t?ng nh?n v?t
        for cid in active_characters:
            k_leaks = self.know_eng.check_for_premature_knowledge_leak(cid, text)
            for kl in k_leaks:
                issues.append({"category": "KNOWLEDGE", "severity": "HIGH", "description": kl})

        # 4. Dead Character Check (Nh?n v?t ch?t kh?ng ???c t?i xu?t hi?n v? l?)
        for cid in active_characters:
            if not self.char_eng.is_alive(cid):
                issues.append({
                    "category": "CHARACTER", "severity": "CRITICAL",
                    "description": f"Nh?n v?t {cid} ?? CH?T nh?ng l?i tham gia v?o ch??ng {chapter_num}!"
                })

        # 5. POV Integrity (Ch?ng Head-Hopping)
        if "nguy?n minh an" in pov.lower() or "minh an" in pov.lower():
            if "l?m t?ch th?m ngh?" in text.lower() or "trong l?ng l?m t?ch ngh?" in text.lower():
                issues.append({
                    "category": "POV", "severity": "HIGH",
                    "description": "HEAD_HOPPING: POV ?ang l? Minh An nh?ng l?i mi?u t? tr?c ti?p d?ng suy ngh? th?m k?n c?a L?m T?ch!"
                })

        # 6. Style & Cheap Cliffhanger Check
        cheap_cliffhangers = ["v? h?n kh?ng bi?t r?ng", "h?n v?nh vi?n kh?ng th? ng? ???c", "chuy?n g? ??n c?ng ph?i ??n"]
        for cc in cheap_cliffhangers:
            if cc in text.lower():
                issues.append({
                    "category": "STYLE", "severity": "MEDIUM",
                    "description": f"L?m d?ng s?o ng? gi?t g?n r? ti?n: '{cc}'!"
                })

        # 7. Word Count & Polish Check
        words = len(text.split())
        if words < 400:
            issues.append({
                "category": "NARRATIVE", "severity": "MEDIUM",
                "description": f"Ch??ng qu? ng?n ({words} t?), c?n ph?t tri?n chi?u s?u b?i c?nh v? c?m x?c."
            })

        # L?u l?i v?o DB v?i unique ID
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
