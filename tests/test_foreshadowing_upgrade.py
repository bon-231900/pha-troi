# -*- coding: utf-8 -*-
"""Unit tests for the Multi-Tier Macro Foreshadowing & Mystery Depth System."""

import unittest
import sqlite3
import json

from tests.test_base import IsolatedDatabaseTestCase
from system.engines.foreshadowing_engine import ForeshadowingEngine
from system.engines.critique_engine import CritiqueEngine
from system.engines.context_builder import ContextBuilder

class TestForeshadowingUpgrade(IsolatedDatabaseTestCase):

    def setUp(self):
        super().setUp()
        self.fsh_eng = ForeshadowingEngine(self.db_path)
        self.critique_eng = CritiqueEngine(self.db_path, record_to_db=False)
        self.context_builder = ContextBuilder(self.db_path)

    def test_01_classify_range_tier(self):
        """Kiểm tra phân loại cự ly phục bút: SHORT, MEDIUM, LONG, EPOCH."""
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 25), "SHORT_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 40), "SHORT_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 80), "MEDIUM_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 110), "MEDIUM_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 300), "LONG_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 510), "LONG_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 600), "EPOCH_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, 1500), "EPOCH_RANGE")
        self.assertEqual(ForeshadowingEngine.classify_range_tier(10, None), "LONG_RANGE")

    def test_02_multitier_writer_view_sanitization(self):
        """Kiểm tra danh sách phục bút đa tầng đã được khử độc an toàn (Sanitized)."""
        views = self.fsh_eng.get_writer_view_multitier(66)
        self.assertGreater(len(views), 0, "Phải có phục bút đa tầng được trả về!")
        for v in views:
            self.assertIn("id", v)
            self.assertIn("observable_clue", v)
            self.assertIn("planted_chapter", v)
            self.assertIn("status", v)
            self.assertIn("range_tier", v)
            # Tuyệt đối không rò rỉ actual_meaning
            self.assertNotIn("actual_meaning", v)
            self.assertNotIn("notices", v)

    def test_03_context_builder_includes_multitier_foreshadowing(self):
        """Kiểm tra ContextBuilder tự động nạp phục bút đa tầng vào context pack."""
        pack = self.context_builder.build_context_pack(
            chapter_num=67,
            pov="Minh An",
            active_characters=["char_minh_an"],
            location_id="loc_cau_mong",
            scene_objective="Khảo sát cọc số 5"
        )
        self.assertIn("active_foreshadowing", pack)
        active_fsh = pack["active_foreshadowing"]
        self.assertGreater(len(active_fsh), 0, "Context pack phải chứa active_foreshadowing!")
        tiers = [item.get("range_tier") for item in active_fsh]
        # Phải có ít nhất 1 tier được gán
        self.assertTrue(any(t in ("SHORT_RANGE", "MEDIUM_RANGE", "LONG_RANGE", "EPOCH_RANGE") for t in tiers))

    def test_04_dormant_seed_tiered_tagging(self):
        """Kiểm tra thông điệp cảnh báo có chứa nhãn cự ly [EPOCH_RANGE] và gợi ý trung gian."""
        self.fsh_eng.plant_seed(
            seed_id="FSH-TEST-EPOCH",
            description="Manh mối viễn cổ chư thiên",
            chapter_num=10,
            scene_num=1,
            notices=["Cổ tự"],
            actual_meaning="Bí mật tối hậu",
            payoff_chapter=1000
        )
        # Tại chương 70 (gap = 60 > 50):
        dormant = self.fsh_eng.audit_dormant_seeds(current_chapter=70, threshold_chapters=50)
        self.assertTrue(any("FSH-TEST-EPOCH" in d and "[EPOCH_RANGE]" in d for d in dormant))
        self.fsh_eng.update_status("FSH-TEST-EPOCH", "PAID", payoff_chapter=1000)

    def test_05_mystery_depth_integrity(self):
        """Kiểm tra tính toàn vẹn của ma trận chiều sâu bí mật 4 tầng."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT mystery_id, name, current_revealed_layer, surface_explanation, deep_explanation, ultimate_truth FROM mystery_depth")
        rows = cur.fetchall()
        conn.close()

        self.assertGreaterEqual(len(rows), 4, "Phải có ít nhất 4 bí mật cốt lõi trong mystery_depth!")
        for r in rows:
            self.assertTrue(r[0].startswith("MYS-"))
            self.assertIsNotNone(r[3], "Surface explanation không được null!")
            self.assertIsNotNone(r[4], "Deep explanation không được null!")
            self.assertIsNotNone(r[5], "Ultimate truth không được null!")

    def test_06_critique_engine_macro_foreshadowing_audit(self):
        """Kiểm tra CritiqueEngine chạy kiểm toán mật độ phục bút tầm xa thành công."""
        report = self.critique_eng.audit_chapter_draft(
            chapter_num=67,
            pov="Minh An",
            active_characters=["char_minh_an"],
            text="Tôi bước qua cầu Mống trong đêm tĩnh lặng. Tiếng gió rít qua lan can thép đen cổ kính rờn rợn sống lưng."
        )
        self.assertIn("passed", report)
        self.assertIn("issues", report)
        # Không được có lỗi CRITICAL hoặc HIGH từ Foreshadowing
        fsh_issues = [i for i in report["issues"] if i.get("category") == "FORESHADOWING"]
        self.assertFalse(any(i.get("severity") in ("CRITICAL", "HIGH") for i in fsh_issues))

if __name__ == "__main__":
    unittest.main()
