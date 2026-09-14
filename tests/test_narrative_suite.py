# -*- coding: utf-8 -*-
import unittest
import sqlite3
import json
import os
import shutil
from system.core.config import DB_PATH, ROOT_DIR
from system.engines.canon_engine import CanonEngine
from system.engines.world_engine import WorldEngine
from system.engines.character_engine import CharacterEngine
from system.engines.knowledge_engine import KnowledgeEngine
from system.engines.power_engine import PowerEngine
from system.engines.timeline_engine import TimelineEngine
from system.engines.foreshadowing_engine import ForeshadowingEngine
from system.engines.critique_engine import CritiqueEngine
from system.engines.relationship_engine import RelationshipEngine
from system.engines.research_vault import ResearchVault
from system.engines.proposal_manager import ProposalManager

class TestNovelOSNarrativeSuite(unittest.TestCase):
    """Bộ kiểm thử narrative 20 tình huống phá hoại logic và mô phỏng trí nhớ dài hạn 2.000 chương."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = DB_PATH
        cls.canon_eng = CanonEngine(cls.db_path)
        cls.world_eng = WorldEngine(cls.db_path)
        cls.char_eng = CharacterEngine(cls.db_path)
        cls.know_eng = KnowledgeEngine(cls.db_path)
        cls.power_eng = PowerEngine()
        cls.time_eng = TimelineEngine(cls.db_path)
        cls.fsh_eng = ForeshadowingEngine(cls.db_path)
        cls.critique_eng = CritiqueEngine(cls.db_path)
        cls.rel_eng = RelationshipEngine()
        cls.res_vault = ResearchVault()
        cls.prop_mgr = ProposalManager(cls.db_path)

    # Test 1: Nhân vật biết thông tin quá sớm (Knowledge leak)
    def test_01_character_knows_information_too_early(self):
        text = "Tôi biết rõ Trái Đất là vị diện bị phong ấn và các con đường tu luyện khác đã bị cắt đứt."
        leaks = self.know_eng.check_for_premature_knowledge_leak("char_minh_an", text)
        self.assertTrue(len(leaks) > 0, "Hệ thống phải phát hiện nhân vật biết thông tin quá sớm!")

    # Test 2: Nhân vật đã chết xuất hiện trở lại
    def test_02_dead_character_appears(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO entities (id, name, type, status) VALUES ('char_dead_npc', 'Trần Văn Chết', 'character', 'DEAD')")
        conn.commit()
        conn.close()

        res = self.critique_eng.audit_chapter_draft(10, "Minh An", ["char_minh_an", "char_dead_npc"], "Trần Văn Chết bước vào phòng và nói chuyện vui vẻ.")
        self.assertFalse(res["passed"], "Hệ thống phải chặn nhân vật đã chết xuất hiện trở lại!")
        self.assertTrue(any("ĐÃ CHẾT" in i["description"] for i in res["issues"]))

    # Test 3: Di chuyển phi lý (Vượt cổng phong ấn)
    def test_03_impossible_travel(self):
        valid, msg = self.world_eng.validate_travel("node_vi_dien_linh_dao", "node_trai_dat", 2.0)
        self.assertFalse(valid, "Hệ thống phải chặn việc di chuyển vào Trái Đất thông thường qua cổng phong ấn!")

    # Test 4: Đột phá cảnh giới nhảy cóc phi lý
    def test_04_realm_jumps(self):
        valid, msg = self.power_eng.validate_realm_jump("Luyện Thể", "Tông Sư", 5)
        self.assertFalse(valid, "Hệ thống phải chặn đột phá cảnh giới nhảy vọt phi lý!")

    # Test 5: Bảo vật xuất hiện khi chưa từng thu thập
    def test_05_artifact_without_acquisition(self):
        char = self.char_eng.get_character("char_minh_an")
        inv = char.get("latest_state", {}).get("inventory", [])
        self.assertNotIn("Chung Cực Chi Kiếm", inv, "Vật phẩm chưa từng thu thập không thể tự nhiên có trong túi đồ.")

    # Test 6: Phục bút bị bỏ quên quá lâu
    def test_06_foreshadowing_forgotten(self):
        # Gieo phục bút ở chương 1, kiểm tra ở chương 80 (vượt ngưỡng 50 chương)
        self.fsh_eng.plant_seed("FSH-TEST-DORMANT", "Bảo vật cổ xưa bị bỏ quên", 1, 1, ["Minh An"], "Ý nghĩa thử nghiệm", payoff_chapter=200)
        dormant = self.fsh_eng.audit_dormant_seeds(current_chapter=80, threshold_chapters=50)
        self.assertTrue(len(dormant) > 0, "Hệ thống phải cảnh báo phục bút bị bỏ quên quá lâu!")
        self.fsh_eng.update_status("FSH-TEST-DORMANT", "PAID", payoff_chapter=200)

    # Test 7: Mâu thuẫn địa lý và thời gian âm
    def test_07_location_contradiction(self):
        valid, msg = self.world_eng.validate_travel("loc_hcmc", "loc_hcmc", -5.0)
        self.assertFalse(valid, "Thời gian di chuyển âm hoặc mâu thuẫn phải bị bắt lỗi.")

    # Test 8: Nhảy góc nhìn (POV Leak / Head hopping)
    def test_08_pov_leak(self):
        text = "Tôi bước đi trên đường. Trong lòng Lâm Tịch nghĩ rằng nơi này thật kỳ lạ và nàng thầm tính toán kế hoạch."
        res = self.critique_eng.audit_chapter_draft(1, "Nguyễn Minh An", ["char_minh_an"], text)
        self.assertTrue(any(i["category"] == "POV" for i in res["issues"]), "Hệ thống phải bắt lỗi Head-hopping khi POV Minh An đọc trộm suy nghĩ Lâm Tịch!")

    # Test 9: Rò rỉ bí mật tác giả (AUTHOR_SECRET leak)
    def test_09_author_secret_leak(self):
        text = "Nơi này từng là chiến trường hạch tâm của cuộc chiến kỷ nguyên trước."
        res = self.critique_eng.audit_chapter_draft(1, "Nguyễn Minh An", ["char_minh_an"], text)
        self.assertFalse(res["passed"], "Hệ thống phải chặn rò rỉ bí mật tác giả!")
        self.assertTrue(any(i["category"] == "AUTHOR_SECRET" for i in res["issues"]))

    # Test 10: Nhầm lẫn nghiên cứu đời thực thành Canon
    def test_10_research_accidentally_treated_as_canon(self):
        items = self.res_vault.get_items()
        for it in items:
            self.assertEqual(it.get("canon_status"), "RESEARCH_ONLY", "Nghiên cứu đời thực không được tự động biến thành Canon!")

    # Test 11: Lore nhỏ âm thầm đổi Canon đã khóa
    def test_11_minor_lore_silently_changes_major_canon(self):
        entry = self.canon_eng.get_canon("minh_an_ordinary")
        self.assertEqual(entry["level"], "LOCKED", "Canon LOCKED không được phép bị sửa đổi lén lút!")

    # Test 12: Viết lại vi phạm tiền đề đã khóa
    def test_12_rewrite_accidentally_changes_canon(self):
        rewrite_draft = "Minh An bất ngờ nhận ra hắn chính là người chuyển sinh từ viễn cổ."
        violations = self.canon_eng.validate_text_for_forbidden_assumptions(rewrite_draft)
        self.assertTrue(len(violations) > 0, "Bản viết lại không được vi phạm canon đã khóa!")

    # Test 13: Xung đột dòng thời gian
    def test_13_two_simultaneous_timelines_conflict(self):
        valid, msg = self.time_eng.validate_chronology(5, "2026-09-10T12:00:00+07:00")
        self.assertFalse(valid, "Hệ thống phải phát hiện dòng thời gian bị đảo ngược vô lý!")

    # Test 14: Quan hệ tình cảm nhảy vọt khi chưa có biến cố
    def test_14_relationship_jump_without_event(self):
        rel = self.rel_eng.get_relationship("char_minh_an", "char_lam_tich")
        self.assertEqual(rel.get("romantic_awareness", 0), 0, "Quan hệ tình cảm không được nhảy vọt khi chưa có biến cố tương tác!")

    # Test 15: Minh An đột ngột biến thành hidden OP
    def test_15_minh_an_suddenly_becomes_hidden_op(self):
        text = "Minh An thi triển huyết mạch thần hủy diệt toàn bộ quân địch sau 3 ngày tu luyện."
        violations = self.canon_eng.validate_text_for_forbidden_assumptions(text)
        self.assertTrue(len(violations) >= 2, "Hệ thống phải ngăn chặn Minh An biến thành hidden OP!")

    # Test 16: Cơ chế thương tổn và giới hạn sức mạnh của Lâm Tịch
    def test_16_lam_tich_power_mechanics(self):
        char = self.char_eng.get_character("char_lam_tich")
        self.assertIn("Nguyên Thần Tàn Phiến", char["cultivation"]["current_status"])
        self.assertIn("Đạo cơ vỡ nát", char["latest_state"]["injuries"])

    # Test 17: Quy tắc cái chết tuyệt đối (Chống hồi sinh)
    def test_17_resurrection_violates_death_rules(self):
        canon_rule = self.canon_eng.get_canon("absolute_death")
        self.assertIn("vĩnh viễn", canon_rule["content"], "Quy tắc cái chết tuyệt đối phải được bảo toàn.")

    # Test 18: Phân tầng sức mạnh thế giới (Trái Đất là vị diện phong ấn tầng 6)
    def test_18_earth_power_hierarchy(self):
        node = self.world_eng.get_node("node_trai_dat")
        self.assertEqual(node["rank"], 6, "Trái Đất là vị diện tầng thấp nhất trong phân tầng cosmology hiện tại!")

    # Test 19: Chặn hệ thống tu luyện ngoại đạo phi lý
    def test_19_unauthorized_cultivation_path(self):
        self.assertNotIn("Hệ Thống Hack Điểm Đạo", self.power_eng.systems, "Hệ thống tu luyện phi lý không được phép xuất hiện!")

    # Test 20: Tính liên tục xuyên suốt hàng ngàn chương (Ch 100 -> Ch 1500)
    def test_20_long_term_continuity_consistency(self):
        self.time_eng.add_event("EVT-CH100", "Lâm Tịch tiết lộ tên thật cho Minh An", 100, 1, "2026-10-01T20:00:00+07:00", "loc_hcmc", ["char_minh_an", "char_lam_tich"], "Minh An biết tên Lâm Tịch", "Minh An ghi nhớ.")
        self.know_eng.set_character_epistemic_status("char_minh_an", "fact_lam_tich_name", "Tên thật của nữ nhân trong thức hải là Lâm Tịch", "KNOWN", 100)
        
        status_at_1500 = self.know_eng.get_character_epistemic_status("char_minh_an", "fact_lam_tich_name")
        self.assertEqual(status_at_1500, "KNOWN", "Thông tin đã biết ở chương 100 không được bị mất dấu ở chương 1500!")

    # BÀI KIỂM TRA MÔ PHỎNG TRÍ NHỚ DÀI HẠN (Mục 104)
    def test_21_long_form_memory_simulation(self):
        """Mô phỏng chuỗi 1500 chương: Ch 1 (gieo bảo vật) -> Ch 50 (Minh An biết) -> Ch 100 (đối thủ hiểu sai) -> Ch 700 (đồng minh tử trận) -> Ch 1500 (Payoff)."""
        # Ch 1: Gieo hạt mầm cổ vật
        self.fsh_eng.plant_seed("FSH-SIM-A", "Mảnh ngọc cổ mang tàn niệm của Thần Ma Vực", 1, 1, ["Lâm Tịch"], "Chìa khóa mở phong ấn cổ xưa", payoff_chapter=1500)
        
        # Ch 50: Minh An biết sự thật
        self.know_eng.set_character_epistemic_status("char_minh_an", "fact_ancient_jade", "Mảnh ngọc cổ là chìa khóa mở phong ấn", "KNOWN", 50)
        self.assertEqual(self.know_eng.get_character_epistemic_status("char_minh_an", "fact_ancient_jade"), "KNOWN")

        # Ch 100: Nhân vật phản diện tin vào phiên bản sai lệch (FALSE_BELIEF)
        self.know_eng.set_character_epistemic_status("char_antagonist_c", "fact_ancient_jade", "Mảnh ngọc cổ chỉ là đá phong thủy bình thường", "FALSE_BELIEF", 100)
        self.assertEqual(self.know_eng.get_character_epistemic_status("char_antagonist_c", "fact_ancient_jade"), "FALSE_BELIEF")

        # Ch 700: Nhân vật đồng minh hy sinh
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO entities (id, name, type, status) VALUES ('char_ally_d', 'Đồng Minh D', 'character', 'ACTIVE')")
        conn.commit()
        conn.close()
        self.char_eng.mark_dead("char_ally_d", 700, "Hy sinh khi bảo vệ trận địa")
        self.assertFalse(self.char_eng.is_alive("char_ally_d"), "Đồng minh D phải được xác nhận đã chết vĩnh viễn sau chương 700.")

        # Ch 1500: Payoff hoàn tất
        self.fsh_eng.update_status("FSH-SIM-A", "PAID", payoff_chapter=1500)
        seeds = self.fsh_eng.list_seeds(status="PAID")
        self.assertTrue(any(s["id"] == "FSH-SIM-A" for s in seeds), "Phục bút gieo từ chương 1 phải được thu hồi trọn vẹn tại chương 1500!")

if __name__ == "__main__":
    unittest.main()