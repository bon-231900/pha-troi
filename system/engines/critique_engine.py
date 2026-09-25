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

    DEFAULT_NAME_TYPOS = {
        "Minh Ánh": "Nguyễn Minh An",
        "Minh Ang": "Nguyễn Minh An",
        "Lâm Tích": "Lâm Tịch",
        "Lâm Tịnh": "Lâm Tịch"
    }

    CHEAP_CLIFFHANGERS = [
        "và hắn không biết rằng",
        "hắn vĩnh viễn không thể ngờ được",
        "chuyện gì đến cũng phải đến",
        "hơn ai hết, hắn hiểu rằng",
        "như một lẽ tất nhiên",
        "thời gian như ngưng đọng",
        "dường như đang muốn nói điều gì đó"
    ]

    FORBIDDEN_SPONTANEOUS_ITEMS = [
        "thần kiếm",
        "túi trữ vật",
        "linh đan",
        "ngọc giản",
        "pháp bảo"
    ]

    def __init__(self, db_path: str = DB_PATH, name_typos: dict = None, forbidden_items: list = None, record_to_db: bool = True):
        self.db_path = db_path
        self.record_to_db = record_to_db
        self.name_typos = name_typos if name_typos is not None else self.DEFAULT_NAME_TYPOS.copy()
        self.forbidden_spontaneous_items = forbidden_items if forbidden_items is not None else self.FORBIDDEN_SPONTANEOUS_ITEMS.copy()
        self.cheap_cliffhangers = self.CHEAP_CLIFFHANGERS.copy()
        self.canon_eng = CanonEngine(db_path)
        self.know_eng = KnowledgeEngine(db_path)
        self.char_eng = CharacterEngine(db_path)
        self.power_eng = PowerEngine()

    def audit_chapter_draft(self, chapter_num: int, pov: str, active_characters: list, text: str, save_errors: bool = None) -> dict:
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

        # 6. Style & Cheap Cliffhangers & Anti-AI Smells
        for cc in self.cheap_cliffhangers:
            if cc in text.lower():
                issues.append({
                    "category": "STYLE", "severity": "MEDIUM",
                    "description": f"Lạm dụng sáo ngữ giật gân rẻ tiền: '{cc}'!"
                })

        # 6.1. Banned Formulaic Ending Teasers
        forbidden_ending_teasers = [
            "mọi thứ giờ mới thật sự bắt đầu", "mọi thứ giờ mới bắt đầu",
            "mọi chuyện giờ mới bắt đầu", "chuẩn bị có thử thách",
            "chuẩn bị đón nhận", "thử thách mới đang chờ",
            "chặng đường mới đang chờ", "hành trình mới đang vẫy gọi",
            "đang vẫy gọi tôi", "đang vẫy gọi"
        ]
        text_clean = text.strip()
        paragraphs = [p.strip() for p in text_clean.split("\n") if p.strip()]
        last_para = paragraphs[-1].lower() if paragraphs else ""
        for fet in forbidden_ending_teasers:
            if fet in last_para:
                issues.append({
                    "category": "STYLE", "severity": "CRITICAL",
                    "description": f"FORMULAIC_ENDING_TEASER: Kết chương dập khuôn mo-tip 'Chuẩn bị có thử thách': '{fet}'"
                })

        # 6.2. Shonen Exclamation Ending (!)
        if paragraphs and (paragraphs[-1].endswith("!") or paragraphs[-1].endswith('!"') or paragraphs[-1].endswith("!'")):
            issues.append({
                "category": "STYLE", "severity": "HIGH",
                "description": f"SHONEN_EXCLAMATION_ENDING: Chương kết thúc bằng câu hô khẩu hiệu dấu chấm than (!)"
            })

        # 6.3. Opening Formulaic Timestamp
        if paragraphs:
            p_first = paragraphs[0]
            if re.search(r'^(?:[B|b]ây giờ là|[V|v]ào lúc)?\s*(?:[M|m]ột|[H|h]ai|[B|b]a|[B|b]ốn|[N|n]ăm|[S|s]áu|[B|b]ảy|[T|t]ám|[C|c]hín|[M|m]ười|[M|m]ười một|[M|m]ười hai)\s*giờ(?:\s*(?:ba mươi|mười lăm|bốn mươi lăm|\d+)\s*phút)?(?:\s*(?:sáng|trưa|chiều|tối|đêm))?', p_first):
                issues.append({
                    "category": "STYLE", "severity": "CRITICAL",
                    "description": f"FORMULAIC_OPENING_TIMESTAMP: Mở đầu chương dập khuôn mo-tip 'Bây giờ là mấy giờ': '{p_first[:60]}...'"
                })

        # 6.4. Bold Entity Slop
        if re.search(r'\*\*[^*]+\*\*', text):
            issues.append({
                "category": "STYLE", "severity": "HIGH",
                "description": "BOLD_ENTITY_SLOP: Phát hiện thẻ in đậm Markdown (**...**) trong thân bài văn xuôi."
            })

        # 7. Word Count Check
        words = len(text.split())
        if words < 400:
            issues.append({
                "category": "NARRATIVE", "severity": "MEDIUM",
                "description": f"Chương quá ngắn ({words} từ), cần phát triển chiều sâu bối cảnh và cảm xúc."
            })

        # 8. Name & Alias Consistency Check
        for typo, correct in self.name_typos.items():
            if typo.lower() in text.lower():
                issues.append({
                    "category": "CONSISTENCY", "severity": "MEDIUM",
                    "description": f"Phát hiện sai sót chính tả tên nhân vật: '{typo}' -> Tên chuẩn là '{correct}'!"
                })

        # 9. Inventory Possession Check
        # Nếu nhân vật rút/sử dụng vũ khí đặc biệt mà không có trong túi đồ
        if "minh an" in pov.lower():
            for fi in self.forbidden_spontaneous_items:
                if f"rút {fi}" in text.lower() or f"lấy {fi} ra" in text.lower() or f"cầm {fi}" in text.lower():
                    # Kiểm tra xem có trong inventory không
                    st = self.char_eng.get_character("char_minh_an").get("latest_state", {})
                    inv = st.get("inventory", [])
                    if not any(fi in str(item).lower() for item in inv):
                        issues.append({
                            "category": "INVENTORY", "severity": "HIGH",
                            "description": f"INVENTORY_VIOLATION: Minh An sử dụng '{fi}' nhưng đồ vật này không có trong túi đồ được ghi nhận!"
                        })

        # 9.5. Kiểm tra Bão Hòa Tự Sự & Sáo Ngữ (Narrative Fatigue)
        from system.engines.fatigue_engine import FatigueEngine
        fe = FatigueEngine(self.db_path)
        fatigue_res = fe.analyze_chapter_text(chapter_num, text)
        for alert in fatigue_res["alerts"]:
            issues.append({
                "category": "FATIGUE",
                "severity": alert["severity"],
                "description": alert["details"]
            })

        # 9.6. Kiểm toán Mật Độ Phục Bút Tầm Xa (Macro Foreshadowing Density Audit)
        from system.engines.foreshadowing_engine import ForeshadowingEngine
        fe_fsh = ForeshadowingEngine(self.db_path)
        dormant_alerts = fe_fsh.audit_dormant_seeds(chapter_num)
        for da in dormant_alerts:
            severity = "MEDIUM" if "OVERDUE" in da else "LOW"
            issues.append({
                "category": "FORESHADOWING",
                "severity": severity,
                "description": da
            })

        # 10. Ghi nhận Telemetry (Viễn trắc kiểm tra tất định)
        from system.engines.telemetry_engine import TelemetryEngine
        te = TelemetryEngine(self.db_path)
        # Một lượt kiểm tra toàn diện 11 chiều kích bằng LLM thường tốn ~3.000 tokens
        te.record_event(
            task_type="CONTINUITY_AUDIT_DETERMINISTIC",
            model_tier="DETERMINISTIC",
            tokens_in_est=0,
            tokens_out_est=0,
            tokens_saved_est=3200,
            deterministic_ops_count=10,
            cache_hit=True,
            description=f"Kiểm tra tính nhất quán tất định Chương {chapter_num} (Tiết kiệm 3.200 tokens LLM)"
        )

        # Lưu lỗi vào DB
        should_save = save_errors if save_errors is not None else self.record_to_db
        if issues and should_save:
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
