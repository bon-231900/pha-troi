# -*- coding: utf-8 -*-
"""Động cơ Giám Sát Chiều Sâu Nhân Vật & Kiểm Soát Lore (Character Grounding & Lore Control Engine).
Chuyên trách giải quyết triệt để 'Bệnh Xây Dựng Thế Giới' (Worldbuilder's Disease):
1. Thực thi Lệnh Đóng Băng Lore (Lore Freeze Enforcement): Chặn đứng việc mở rộng khái niệm/vũ trụ mới.
2. Đo lường Độ Sâu Nội Tâm Nhân Vật (Character Interiority & Intimacy Index: 0.0 - 10.0).
3. Phát hiện và ngăn chặn Lạm Dụng Giảng Giải Lore (Lore-Dumping Detection).
4. Bảo vệ Bản Sắc Phàm Nhân & Đời Thường Sài Gòn 2026 (Everyday Human Anchors).
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

class CharacterGroundingEngine:
    # 1. Các mẫu câu giảng giải lý thuyết / lore-dumping cần kiểm soát
    LORE_DUMP_PATTERNS = [
        r"vào thời kỳ\s+(?:thượng cổ|viễn cổ|hồng hoang|tiền sử)",
        r"đó là một\s+(?:đại năng|tông môn|công pháp|bí thuật|cổ vật)\s+từng",
        r"theo truyền thuyết\s+(?:ngàn năm|vạn năm|cổ xưa)",
        r"nguyên do là vì\s+(?:hàng triệu năm|thời viễn cổ)",
        r"trong cấu trúc vũ trụ\s+(?:7 đạo|chư thiên|cửu thiên)",
        r"bản chất của\s+(?:phong ấn|trận pháp|linh mạch|long mạch)\s+này là"
    ]

    # 2. Dấu hiệu nội tâm, cảm xúc và lo toan con người của Minh An (Interiority & Vulnerability)
    INTERIORITY_MARKERS = [
        "tôi tự hỏi", "trong lòng dâng lên", "nỗi sợ", "lo lắng", "mệt mỏi",
        "nhớ mẹ", "căn phòng trọ", "tiền thuê", "công việc", "bất lực",
        "nghẹn ngào", "nước mắt", "cắn chặt môi", "cô độc", "tội lỗi",
        "liệu tôi có", "tôi chỉ là một", "nhân viên", "kỹ sư", "người phàm"
    ]

    # 3. Dấu hiệu đời sống trần thế Sài Gòn 2026 (Grounding & Daily Life)
    DAILY_LIFE_MARKERS = [
        "sài gòn", "cơm tấm", "cà phê", "mẹ", "tiền trọ", "nơ trang long",
        "bình thạnh", "ung văn khiêm", "xe máy", "wave alpha", "kẹt xe",
        "tiếng còi xe", "bác tài", "công an", "viện địa tầng", "tuấn",
        "bát mì", "quán nước", "tiếng chổi tre", "mưa rào"
    ]

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS character_intimacy_ledger (
            chapter_num INTEGER PRIMARY KEY,
            interiority_score REAL,
            daily_life_score REAL,
            lore_dump_count INTEGER,
            new_concepts_detected_json TEXT,
            status TEXT,
            recommendation TEXT,
            created_at TEXT
        )
        """)
        conn.commit()
        conn.close()

    def audit_chapter_intimacy(self, chapter_num: int, text: str, lore_freeze_active: bool = True) -> dict:
        """Kiểm định toàn diện bản thảo để đảm bảo Minh An ở trung tâm và không bị lore-dumping."""
        text_lower = text.lower()
        word_count = len(text.split())
        density_factor = 3000.0 / max(word_count, 1000)

        # 1. Đo lường mức độ nội tâm (Interiority Score: 0.0 - 10.0)
        interiority_hits = 0
        matched_interiority = []
        for marker in self.INTERIORITY_MARKERS:
            cnt = len(re.findall(re.escape(marker), text_lower))
            if cnt > 0:
                interiority_hits += cnt
                matched_interiority.append((marker, cnt))

        norm_interiority = (interiority_hits * density_factor) * 0.9
        interiority_score = min(10.0, round(norm_interiority, 2))

        # 2. Đo lường đời sống trần thế (Daily Life Score: 0.0 - 10.0)
        daily_life_hits = 0
        matched_daily = []
        for marker in self.DAILY_LIFE_MARKERS:
            cnt = len(re.findall(re.escape(marker), text_lower))
            if cnt > 0:
                daily_life_hits += cnt
                matched_daily.append((marker, cnt))

        norm_daily = (daily_life_hits * density_factor) * 0.75
        daily_life_score = min(10.0, round(norm_daily, 2))

        # 3. Quét các đoạn lore-dumping dài dòng
        lore_dump_hits = []
        for pattern in self.LORE_DUMP_PATTERNS:
            matches = re.findall(pattern, text_lower)
            if matches:
                lore_dump_hits.extend(matches)

        lore_dump_count = len(lore_dump_hits)

        # 4. Đánh giá và khuyến nghị
        warnings = []
        status = "PASSED"

        if lore_freeze_active and lore_dump_count >= 3:
            warnings.append(f"LORE_DUMP_OVERFLOW: Phát hiện {lore_dump_count} đoạn văn giảng giải lore dài dòng. Cần cắt giảm và chuyển sang kể qua trải nghiệm thực tế của Minh An.")
            status = "WARNING"

        if interiority_score < 3.5:
            warnings.append(f"WEAK_INTERIORITY: Điểm chiều sâu nội tâm của Minh An chỉ đạt {interiority_score:.2f}/10.0. Minh An đang bị biến thành công cụ hành động, thiếu cảm xúc, suy tư và lo toan con người.")
            status = "WARNING"

        if daily_life_score < 3.0:
            warnings.append(f"UNGROUNDED: Thiếu vắng các chi tiết đời thường Sài Gòn/người mẹ/cuộc sống phàm trần (Điểm: {daily_life_score:.2f}/10.0). Nguy cơ biến thành tiên hiệp xa lạ.")
            status = "WARNING"

        recommendation = "Bản thảo cân bằng tốt giữa con người và bối cảnh." if not warnings else " | ".join(warnings)

        # Lưu vào database
        now_iso = datetime.now().isoformat()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO character_intimacy_ledger
        (chapter_num, interiority_score, daily_life_score, lore_dump_count, new_concepts_detected_json, status, recommendation, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chapter_num, interiority_score, daily_life_score, lore_dump_count,
            json.dumps(lore_dump_hits, ensure_ascii=False), status, recommendation, now_iso
        ))
        conn.commit()
        conn.close()

        return {
            "chapter_num": chapter_num,
            "interiority_score": interiority_score,
            "daily_life_score": daily_life_score,
            "lore_dump_count": lore_dump_count,
            "status": status,
            "warnings": warnings,
            "recommendation": recommendation,
            "matched_interiority": matched_interiority,
            "matched_daily": matched_daily
        }
