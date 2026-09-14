# -*- coding: utf-8 -*-
"""Bộ kiểm thử đơn vị cho kiến trúc nâng cấp Novel OS 3.000+ chương.
Kiểm tra toàn diện 5 động cơ mới và nâng cấp:
1. StoryThreadEngine (Quản lý tuyến truyện, phát hiện tuyến ngủ quên)
2. FatigueEngine (Phát hiện sáo ngữ, lặp cliffhanger, thiếu khoảng thở đời thường)
3. EscalationEngine (Kiểm soát trần leo thang 6 trục, ngăn ngừa power creep)
4. HierarchyEngine (Phân cấp 8 tầng, lát cắt ngữ cảnh phân tầng)
5. KnowledgeEngine (Phân tách nhận thức 4 tầng: World Truth, Character Belief, Suspicion, Reader Knowledge)
"""

import unittest
import os
import sys
import sqlite3
import json

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

from system.core.config import DB_PATH
from system.engines.thread_engine import StoryThreadEngine
from system.engines.fatigue_engine import FatigueEngine
from system.engines.escalation_engine import EscalationEngine
from system.engines.hierarchy_engine import HierarchyEngine
from system.engines.knowledge_engine import KnowledgeEngine

class Test3000UpgradeSuite(unittest.TestCase):
    def setUp(self):
        self.db_path = DB_PATH
        self.thread_eng = StoryThreadEngine(self.db_path)
        self.fatigue_eng = FatigueEngine(self.db_path)
        self.escalation_eng = EscalationEngine(self.db_path)
        self.hierarchy_eng = HierarchyEngine(self.db_path)
        self.knowledge_eng = KnowledgeEngine(self.db_path)

    # 1. StoryThreadEngine tests
    def test_01_story_thread_lifecycle_and_dormancy(self):
        # Tạo tuyến truyện thử nghiệm
        self.thread_eng.create_thread(
            thread_id="TH-TEST-DORMANT",
            thread_type="SUBPLOT",
            title="Tuyến điều tra phụ của kỹ sư Tuấn",
            description="Tuấn phát hiện số liệu đo đạc bờ kè bị sai lệch",
            origin_chapter=10,
            revisit_window_chapters=15,
            urgency="MEDIUM",
            importance="MINOR"
        )
        
        # Kiểm tra trạng thái ban đầu
        t = self.thread_eng.get_thread("TH-TEST-DORMANT")
        self.assertIsNotNone(t)
        self.assertEqual(t["status"], "ACTIVE")
        self.assertEqual(t["last_touched_chapter"], 10)

        # Tại chương 20 (chưa quá 15 chương): không bị coi là dormant
        dormant_at_20 = self.thread_eng.audit_dormant_threads(current_chapter=20)
        self.assertFalse(any(d["thread_id"] == "TH-TEST-DORMANT" for d in dormant_at_20))

        # Tại chương 30 (cách 20 chương > 15): PHẢI bị cảnh báo dormant!
        dormant_at_30 = self.thread_eng.audit_dormant_threads(current_chapter=30)
        self.assertTrue(any(d["thread_id"] == "TH-TEST-DORMANT" for d in dormant_at_30))

        # Touch tuyến tại chương 30
        self.thread_eng.touch_thread("TH-TEST-DORMANT", chapter_num=30, new_state="Tuấn báo cáo số liệu cho Minh An")
        dormant_after_touch = self.thread_eng.audit_dormant_threads(current_chapter=30)
        self.assertFalse(any(d["thread_id"] == "TH-TEST-DORMANT" for d in dormant_after_touch))

        # Resolve tuyến
        self.thread_eng.resolve_thread("TH-TEST-DORMANT", chapter_num=35, resolution_summary="Số liệu đã được hiệu chỉnh")
        resolved_t = self.thread_eng.get_thread("TH-TEST-DORMANT")
        self.assertEqual(resolved_t["status"], "RESOLVED")

    # 2. FatigueEngine tests
    def test_02_fatigue_vocabulary_repetition_detection(self):
        # Văn bản lạm dụng cụm từ 'hít một hơi sâu' và 'đồng tử co rụt'
        repetitive_text = """
        Minh An hít một hơi sâu nhìn dòng sông. Hắn lại hít một hơi sâu khi thấy sóng lớn.
        Lâm Tịch nhắc nhở, hắn tiếp tục hít một hơi sâu để bình tâm.
        Đồng tử co rụt lại khi nhìn thấy cấu trúc kim loại. Hắn đồng tử co rụt thêm lần nữa. Đồng tử co rụt liên hồi.
        """
        analysis = self.fatigue_eng.analyze_chapter_text(chapter_num=999, text=repetitive_text)
        self.assertTrue(analysis["has_fatigue"])
        types = [a["pattern_type"] for a in analysis["alerts"]]
        self.assertIn("VOCABULARY_REPETITION", types)

    def test_03_fatigue_cliffhanger_consecutive_detection(self):
        ending_text = "Tôi nhìn xuống vực sâu, đột nhiên một bàn tay lạnh ngắt vươn ra từ làn nước."
        # Giả sử 2 chương trước cũng là cliffhanger
        analysis = self.fatigue_eng.analyze_chapter_text(
            chapter_num=45,
            text=ending_text,
            recent_chapter_endings=[True, True]
        )
        self.assertTrue(analysis["has_fatigue"])
        cliff_alerts = [a for a in analysis["alerts"] if a["pattern_type"] == "ENDING_CLIFFHANGER_REPETITION"]
        self.assertEqual(len(cliff_alerts), 1)
        self.assertEqual(cliff_alerts[0]["severity"], "CRITICAL")

    # 3. EscalationEngine tests
    def test_04_escalation_ceiling_and_cooldown_enforcement(self):
        # Volume 1 Power Ceiling là 2.5
        # Kiểm tra mức 2.0 (hợp lệ)
        valid, msg = self.escalation_eng.validate_escalation("volume_01", "POWER_CEILING", proposed_level=2.0, chapter_num=50)
        self.assertTrue(valid)

        # Kiểm tra mức 3.5 (vượt trần 2.5 -> PHẢI CHẶN)
        invalid_ceil, msg_ceil = self.escalation_eng.validate_escalation("volume_01", "POWER_CEILING", proposed_level=3.5, chapter_num=50)
        self.assertFalse(invalid_ceil)
        self.assertIn("VI PHẠM TRẦN LEO THANG", msg_ceil)

        # Kiểm tra cooldown (last escalated ở ch 41, cooldown là 5 -> chương 43 bị chặn)
        invalid_cool, msg_cool = self.escalation_eng.validate_escalation("volume_01", "POWER_CEILING", proposed_level=2.2, chapter_num=43)
        self.assertFalse(invalid_cool)
        self.assertIn("VI PHẠM COOLDOWN", msg_cool)

    # 4. HierarchyEngine tests
    def test_05_hierarchy_ancestor_slicing_and_context(self):
        slice_42 = self.hierarchy_eng.get_chapter_hierarchy_context(42)
        self.assertIsNotNone(slice_42)
        self.assertEqual(slice_42["chapter_id"], "ch_042")
        self.assertEqual(slice_42["mini_arc"]["id"], "mini_arc_01_03")
        self.assertEqual(slice_42["arc"]["id"], "arc_01")
        self.assertEqual(slice_42["volume"]["id"], "volume_01")
        self.assertEqual(slice_42["saga"]["id"], "saga_01")

    # 5. 4-Tier Epistemic Knowledge tests
    def test_06_epistemic_quadrant_truth_vs_belief_vs_reader(self):
        fact = "fact_earth_prison_origin"
        # 1. World truth
        self.knowledge_eng.record_world_truth(fact, "Trái Đất là nhà tù phong ấn hạch tâm kỷ nguyên viễn cổ")
        
        # 2. Reader knowledge
        self.knowledge_eng.record_reader_knowledge(fact, "Độc giả biết Trái Đất có đại phong ấn qua POV Lâm Tịch", chapter_num=40)
        
        # 3. Minh An belief / state (Chỉ nghi ngờ)
        self.knowledge_eng.set_character_epistemic_status("char_minh_an", fact, "Minh An nghi ngờ đây là kết cấu quân sự cổ", "SUSPECTED", chapter_num=40)

        # Trích xuất quadrant
        quad = self.knowledge_eng.get_epistemic_quadrant("char_minh_an", fact)
        self.assertEqual(quad["world_truth"], "Trái Đất là nhà tù phong ấn hạch tâm kỷ nguyên viễn cổ")
        self.assertEqual(quad["reader_knowledge"], "Độc giả biết Trái Đất có đại phong ấn qua POV Lâm Tịch")
        self.assertIn("kết cấu quân sự cổ", quad["character_suspicion"])
        self.assertIsNone(quad["character_belief"])
        self.assertEqual(quad["epistemic_status"], "SUSPECTED")

if __name__ == "__main__":
    unittest.main()
