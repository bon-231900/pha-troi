# -*- coding: utf-8 -*-
"""Động cơ Phòng Thủ Bão Hòa & Công Thức Tự Sự (Narrative Fatigue & Repetition Defense Matrix).
Kiểm soát tất định:
- Lặp lại công thức kết chương (Cliffhanger fatigue)
- Lặp lại chu kỳ biến cố (Anomaly -> Danger -> Epiphany loop)
- Sáo ngữ từ vựng và cử chỉ thể xác lặp đi lặp lại
- Mất cân bằng nhịp điệu (Thiếu khoảng thở đời thường hoặc trì trệ kéo dài)
"""

import re
import sqlite3
import uuid
from datetime import datetime
from system.core.config import DB_PATH

class FatigueEngine:
    CLIFFHANGER_KEYWORDS = [
        "đột nhiên", "bất ngờ", "bỗng nhiên", "biến sắc", "kinh hoàng",
        "đồng tử co rụt", "chuyện gì đã xảy ra", "không xong rồi", "nguy hiểm",
        "phải chăng", "vĩnh viễn không ngờ", "vừa mới bắt đầu"
    ]

    OVERUSED_PHRASES = [
        ("hít một hơi sâu", 2),
        ("hít sâu một hơi", 2),
        ("đồng tử co rụt", 2),
        ("sắc mặt đại biến", 1),
        ("trong lòng run lên", 2),
        ("cười khổ", 3),
        ("không khỏi", 4),
        ("nhướng mày", 3),
        ("chợt giật mình", 2)
    ]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def analyze_chapter_text(self, chapter_num: int, text: str, recent_chapter_endings: list = None) -> dict:
        """Phân tích văn bản của một chương để phát hiện sáo ngữ, kết chương lặp và nhịp điệu."""
        alerts = []
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        last_para = lines[-1].lower() if lines else ""
        text_lower = text.lower()

        # 1. Kiểm tra sáo ngữ cử chỉ / từ vựng lặp (Vocabulary & Phrase Fatigue)
        for phrase, max_allowed in self.OVERUSED_PHRASES:
            count = len(re.findall(re.escape(phrase), text_lower))
            if count > max_allowed:
                alerts.append({
                    "pattern_type": "VOCABULARY_REPETITION",
                    "severity": "WARNING",
                    "phrase": phrase,
                    "count": count,
                    "limit": max_allowed,
                    "details": f"Cụm từ sáo mòn '{phrase}' xuất hiện {count} lần trong chương (ngưỡng tối đa khuyến nghị: {max_allowed} lần)."
                })

        # 2. Kiểm tra công thức kết thúc chương (Ending Cliffhanger Check)
        ending_is_cliffhanger = False
        ending_matched_kw = None
        for kw in self.CLIFFHANGER_KEYWORDS:
            if kw in last_para:
                ending_is_cliffhanger = True
                ending_matched_kw = kw
                break

        # Nếu có lịch sử các chương trước, kiểm tra chuỗi cliffhanger liên tiếp
        if recent_chapter_endings:
            consecutive_cliffhangers = sum(1 for is_cliff in recent_chapter_endings[-3:] if is_cliff)
            if ending_is_cliffhanger and consecutive_cliffhangers >= 2:
                alerts.append({
                    "pattern_type": "ENDING_CLIFFHANGER_REPETITION",
                    "severity": "CRITICAL",
                    "details": f"Đã có {consecutive_cliffhangers + 1} chương liên tiếp kết thúc bằng cliffhanger giật gân! Cần chuyển sang kết thúc lắng đọng, mở rộng suy ngẫm hoặc nhịp thở đời thường."
                })

        # 3. Kiểm tra nhịp điệu đời thường (Everyday Realism / Breathing Room)
        realism_markers = ["sài gòn", "cơm", "cà phê", "xe máy", "kẹt xe", "công ty", "đồng nghiệp", "tin nhắn", "mẹ", "tiền", "ung văn khiêm", "bình thạnh"]
        realism_count = sum(1 for rm in realism_markers if rm in text_lower)
        if realism_count == 0 and len(text.split()) > 1500:
            alerts.append({
                "pattern_type": "PACING_LACK_OF_GROUNDING",
                "severity": "WARNING",
                "details": "Chương hoàn toàn thiếu các neo hiện thực đời thường TP.HCM 2026. Nguy cơ biến thành tu tiên trừu tượng vô căn cứ."
            })

        # Ghi log nếu có cảnh báo
        if alerts:
            self._log_fatigue_alerts(chapter_num, alerts)

        return {
            "chapter_num": chapter_num,
            "has_fatigue": len(alerts) > 0,
            "alerts": alerts,
            "ending_is_cliffhanger": ending_is_cliffhanger,
            "realism_score": realism_count
        }

    def audit_narrative_cycle(self, chapter_window_summaries: list) -> list:
        """Kiểm tra chu kỳ 5-10 chương gần nhất để phát hiện vòng lặp biến cố lặp đi lặp lại."""
        alerts = []
        if len(chapter_window_summaries) < 4:
            return alerts

        # Đếm tần suất các mô-típ cốt truyện xuất hiện liên tục
        combat_count = sum(1 for s in chapter_window_summaries if any(w in s.lower() for w in ["giao chiến", "đột phá", "nguy hiểm", "sát khí"]))
        if combat_count >= len(chapter_window_summaries) * 0.8:
            alerts.append({
                "pattern_type": "ANOMALY_CYCLE",
                "severity": "WARNING",
                "details": f"Căng thẳng/chiến đấu quá dày đặc ({combat_count}/{len(chapter_window_summaries)} chương gần nhất). Cần ít nhất 1-2 chương nhịp chậm, khảo sát khoa học hoặc đời sống tâm lý."
            })
        return alerts

    def _log_fatigue_alerts(self, chapter_num: int, alerts: list):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        now_iso = datetime.now().isoformat()
        for alt in alerts:
            lid = f"FAT-{chapter_num}-{uuid.uuid4().hex[:6]}"
            cur.execute("""
            INSERT INTO thread_fatigue_logs (log_id, chapter_num, pattern_type, occurrences_window, severity, details, detected_at)
            VALUES (?, ?, ?, 1, ?, ?, ?)
            """, (lid, chapter_num, alt["pattern_type"], alt["severity"], alt["details"], now_iso))
        conn.commit()
        conn.close()
