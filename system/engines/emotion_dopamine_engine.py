# -*- coding: utf-8 -*-
"""Động cơ Đo Lường & Điều Phối Cảm Xúc Độc Giả (Emotion & Dopamine Pacing Engine).
Chuyên trách kiểm định và điều phối:
1. Độ Đau Thương & Bi Tráng (Pathos / Tragedy Index: 0.0 - 10.0)
2. Độ Thăng Hoa & Dopamine (Triumph / Dopamine Index: 0.0 - 10.0)
3. Nhịp Thở & Neo Hiện Thực (Grounding & Breathing Index: 0.0 - 10.0)
4. Phân phối ổn định đường cong cảm xúc (Arc-level & Series-level Emotional Pacing).
"""

import os
import sys
import json
import sqlite3
import re
from datetime import datetime

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

class EmotionDopamineEngine:
    # 1. Từ khóa và mẫu hình nhận diện BI THƯƠNG (Pathos & Tragedy)
    PATHOS_MARKERS = {
        "HELPLESSNESS": [
            "bất lực", "không thể giữ", "không thể cứu", "lực bất tòng tâm",
            "run rẩy", "chỉ biết đứng nhìn", "nước mắt rơi", "nghẹn ngào",
            "đau đớn tột cùng", "cào xé tâm can", "chết lặng"
        ],
        "SACRIFICE": [
            "hy sinh", "đứng trong bóng tối", "gánh chịu", "lặng lẽ quay lưng",
            "cắn chặt môi", "nuốt vào trong", "chấp nhận", "đơn độc", "tự mình gánh vác"
        ],
        "SEPARATION": [
            "chia ly", "xa cách", "không thể về", "ngoài khung cửa sổ", "đêm mưa",
            "bóng lưng", "nguội dần", "không kịp", "vĩnh viễn", "xa lạ"
        ],
        "MEMORY_DECAY": [
            "ngươi là ai", "quên mất", "lạnh lùng", "xa lạ", "băng giá",
            "phai mờ", "không còn nhớ", "tịch diệt", "tàn hồn lụi tàn"
        ],
        "LOSS_OF_HUMANITY": [
            "liệu ta có còn là người", "máu lạnh", "nhịp tim chậm dần", "kim thạch vô cảm",
            "mất đi cảm giác", "cỗ máy chiến tranh", "hoảng sợ tự hỏi"
        ]
    }

    # 2. Từ khóa và mẫu hình nhận diện DOPAMINE (Triumph & Catharsis)
    DOPAMINE_MARKERS = {
        "OUTWIT_STRONG": [
            "lấy yếu thắng mạnh", "dùng trí", "tính toán", "bẫy", "tử huyệt",
            "địa hình", "quy luật vật lý", "không ngờ tới", "sơ hở", "lật ngược thế cờ"
        ],
        "BREAKTHROUGH": [
            "đột phá", "ngọc thạch", "cương huyết", "hoán huyết", "khai thông",
            "thức thứ", "chuyển hóa", "cực cảnh", "sôi trào", "bừng sáng", "vượt qua giới hạn"
        ],
        "COUNTERATTACK": [
            "phản kích", "chặn đứng", "búng người lao vút", "giáng thẳng", "đập tan",
            "xé toạc", "sấm sét", "không kịp trở tay", "kinh hoàng biến sắc", "gãy vụn"
        ],
        "SIGNATURE_MOVE": [
            "kính kình", "hoán huyết hóa cương", "long lân phá kình", "dĩ thể vi kiếm",
            "khí quán cửu tiêu", "hắc thiết đoản côn", "vô ngân kiếm khí", "tiếng kiếm reo"
        ],
        "JUSTICE_DELIVERED": [
            "trừng phạt", "đền tội", "tan rã", "tháo chạy", "thất bại thảm hại",
            "cứu vãn", "bình yên trở lại", "ngăn chặn thảm họa"
        ]
    }

    # 3. Neo hiện thực đời thường (Grounding & Breathing)
    GROUNDING_MARKERS = [
        "sài gòn", "cơm tấm", "cà phê", "mẹ", "phòng trọ", "nơ trang long",
        "bình thạnh", "xe máy", "wave alpha", "nước mía", "dầu giây", "quê",
        "ung văn khiêm", "bác tài", "công nhân", "tiếng chổi", "bát mì", "tiếng gà"
    ]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        """Khởi tạo các bảng lưu trữ chỉ số cảm xúc và đường cong Arc."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reader_emotional_ledger (
            chapter_num INTEGER PRIMARY KEY,
            pathos_score REAL,
            pathos_breakdown_json TEXT,
            dopamine_score REAL,
            dopamine_breakdown_json TEXT,
            grounding_score REAL,
            tension_score REAL,
            pacing_assessment TEXT,
            arc_id TEXT,
            created_at TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS arc_emotional_plans (
            arc_id TEXT PRIMARY KEY,
            arc_title TEXT,
            target_pathos_curve_json TEXT,
            target_dopamine_curve_json TEXT,
            actual_pathos_avg REAL,
            actual_dopamine_avg REAL,
            status TEXT,
            updated_at TEXT
        )
        """)
        conn.commit()
        conn.close()

    def analyze_text(self, chapter_num: int, text: str, arc_id: str = "arc_02") -> dict:
        """Phân tích toàn diện văn bản của một chương để đo lường các chỉ số cảm xúc."""
        text_lower = text.lower()
        word_count = len(text.split())

        # 1. Đo lường Pathos
        pathos_counts = {}
        total_pathos_hits = 0
        for category, keywords in self.PATHOS_MARKERS.items():
            hits = 0
            matched = []
            for kw in keywords:
                cnt = len(re.findall(re.escape(kw), text_lower))
                if cnt > 0:
                    hits += cnt
                    matched.append((kw, cnt))
            pathos_counts[category] = {"hits": hits, "matched": matched}
            total_pathos_hits += hits

        # Chuẩn hóa Pathos trên thang 10 (tính theo mật độ từ / 3000 từ)
        density_factor = 3000.0 / max(word_count, 1000)
        norm_pathos = (total_pathos_hits * density_factor) * 0.8
        pathos_score = min(10.0, round(norm_pathos, 2))

        # 2. Đo lường Dopamine
        dopamine_counts = {}
        total_dopamine_hits = 0
        for category, keywords in self.DOPAMINE_MARKERS.items():
            hits = 0
            matched = []
            for kw in keywords:
                cnt = len(re.findall(re.escape(kw), text_lower))
                if cnt > 0:
                    hits += cnt
                    matched.append((kw, cnt))
            dopamine_counts[category] = {"hits": hits, "matched": matched}
            total_dopamine_hits += hits

        norm_dopamine = (total_dopamine_hits * density_factor) * 0.55
        dopamine_score = min(10.0, round(norm_dopamine, 2))

        # 3. Đo lường Grounding
        grounding_hits = 0
        for gm in self.GROUNDING_MARKERS:
            grounding_hits += len(re.findall(re.escape(gm), text_lower))
        norm_grounding = (grounding_hits * density_factor) * 0.7
        grounding_score = min(10.0, round(norm_grounding, 2))

        # 4. Tính toán Tension (Độ căng thẳng tự sự)
        tension_score = min(10.0, round((pathos_score * 0.4 + dopamine_score * 0.6), 2))

        # 5. Đánh giá nhịp độ (Pacing Assessment)
        assessment = []
        if dopamine_score >= 7.5:
            assessment.append("DOPAMINE_HIGH (Cao trào thắng lợi/Đột phá)")
        elif dopamine_score <= 2.5:
            assessment.append("DOPAMINE_LOW (Tích lũy/Trầm lắng)")
        else:
            assessment.append("DOPAMINE_BALANCED (Ổn định)")

        if pathos_score >= 6.5:
            assessment.append("PATHOS_HIGH (Bi thương/Đau xót sâu sắc)")
        elif pathos_score <= 2.0:
            assessment.append("PATHOS_LOW (Yên bình/Ít mất mát)")
        else:
            assessment.append("PATHOS_BALANCED (Có chiều sâu)")

        if grounding_score >= 5.0:
            assessment.append("GROUNDING_SOLID (Đời thường chân thực)")
        else:
            assessment.append("GROUNDING_LOW (Cần bổ sung khoảng thở đời thường)")

        pacing_str = " | ".join(assessment)

        # Lưu vào database
        now_iso = datetime.now().isoformat()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO reader_emotional_ledger
        (chapter_num, pathos_score, pathos_breakdown_json, dopamine_score, dopamine_breakdown_json, grounding_score, tension_score, pacing_assessment, arc_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chapter_num, pathos_score, json.dumps(pathos_counts, ensure_ascii=False),
            dopamine_score, json.dumps(dopamine_counts, ensure_ascii=False),
            grounding_score, tension_score, pacing_str, arc_id, now_iso
        ))
        conn.commit()
        conn.close()

        return {
            "chapter_num": chapter_num,
            "word_count": word_count,
            "pathos_score": pathos_score,
            "dopamine_score": dopamine_score,
            "grounding_score": grounding_score,
            "tension_score": tension_score,
            "pacing_assessment": pacing_str,
            "pathos_breakdown": pathos_counts,
            "dopamine_breakdown": dopamine_counts
        }

    def audit_arc_pacing(self, arc_id: str = "arc_02") -> dict:
        """Kiểm tra sự phân phối cảm xúc của toàn bộ Arc để phát hiện lạm dụng hoặc thiếu hụt."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        rows = cur.execute("""
        SELECT chapter_num, pathos_score, dopamine_score, grounding_score, tension_score
        FROM reader_emotional_ledger
        WHERE arc_id = ?
        ORDER BY chapter_num ASC
        """, (arc_id,)).fetchall()
        conn.close()

        if not rows:
            return {"status": "NO_DATA", "message": f"Chưa có dữ liệu cho {arc_id}"}

        total_chapters = len(rows)
        avg_pathos = sum(r[1] for r in rows) / total_chapters
        avg_dopamine = sum(r[2] for r in rows) / total_chapters
        avg_grounding = sum(r[3] for r in rows) / total_chapters

        # Kiểm tra lạm dụng (Overuse) hoặc thiếu hụt (Deprivation)
        warnings = []
        # 1. Dopamine burnout: 3 chương liên tiếp Dopamine > 7.5
        dopamine_streak = 0
        for r in rows:
            if r[2] >= 7.5:
                dopamine_streak += 1
                if dopamine_streak >= 3:
                    warnings.append(f"DOPAMINE_BURNOUT: Có 3+ chương liên tiếp tại {r[0]} duy trì dopamine quá cao! Nguy cơ gây bão hòa cảm xúc sảng văn.")
            else:
                dopamine_streak = 0

        # 2. Pathos fatigue: 4 chương liên tiếp Pathos > 7.0 mà không có dopamine giải tỏa
        pathos_streak = 0
        for r in rows:
            if r[1] >= 7.0:
                pathos_streak += 1
                if pathos_streak >= 4:
                    warnings.append(f"DEPRESSION_FATIGUE: Có 4+ chương liên tiếp tại {r[0]} duy trì bi thương quá nặng nề! Cần có điểm sáng hy vọng hoặc khoảnh khắc ấm áp.")
            else:
                pathos_streak = 0

        # 3. Thiếu bi thương toàn Arc (Đúng như Author chỉ ra ở Ch 1-77)
        if avg_pathos < 3.0:
            warnings.append(f"LACK_OF_PATHOS: Toàn Arc có chỉ số bi thương trung bình chỉ đạt {avg_pathos:.2f}/10.0 (quá thấp). Cần bổ sung các tình tiết xót xa, mất mát, chia ly để tạo chiều sâu.")

        return {
            "arc_id": arc_id,
            "total_chapters_logged": total_chapters,
            "avg_pathos": round(avg_pathos, 2),
            "avg_dopamine": round(avg_dopamine, 2),
            "avg_grounding": round(avg_grounding, 2),
            "warnings": warnings,
            "recent_chapters": rows[-5:]
        }
