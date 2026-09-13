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
    """B? ki?m th? narrative 20 t?nh hu?ng ph? ho?i logic v? m? ph?ng tr? nh? d?i h?n 2.000 ch??ng."""

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

    # Test 1: Character knows information too early
    def test_01_character_knows_information_too_early(self):
        # Minh An kh?ng bi?t Tr?i ??t b? phong ?n
        text = "T?i bi?t r? Tr?i ??t l? v? di?n b? phong ?n v? c?c con ???ng tu luy?n kh?c ?? b? c?t ??t."
        leaks = self.know_eng.check_for_premature_knowledge_leak("char_minh_an", text)
        self.assertTrue(len(leaks) > 0, "H? th?ng ph?i ph?t hi?n nh?n v?t bi?t th?ng tin qu? s?m!")

    # Test 2: Dead character appears
    def test_02_dead_character_appears(self):
        # ??nh d?u m?t nh?n v?t ph? ch?t
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO entities (id, name, type, status) VALUES ('char_dead_npc', 'Tr?n V?n Ch?t', 'character', 'DEAD')")
        conn.commit()
        conn.close()

        res = self.critique_eng.audit_chapter_draft(10, "Minh An", ["char_minh_an", "char_dead_npc"], "Tr?n V?n Ch?t b??c v?o ph?ng v? n?i chuy?n vui v?.")
        self.assertFalse(res["passed"], "H? th?ng ph?i ch?n nh?n v?t ?? ch?t xu?t hi?n tr? l?i!")
        self.assertTrue(any("?? CH?T" in i["description"] for i in res["issues"]))

    # Test 3: Impossible travel
    def test_03_impossible_travel(self):
        # C? t?nh di chuy?n b?nh th??ng v?o Tr?i ??t khi ?ang b? phong ?n
        valid, msg = self.world_eng.validate_travel("node_vi_dien_linh_dao", "node_trai_dat", 2.0)
        self.assertFalse(valid, "H? th?ng ph?i ch?n vi?c di chuy?n v?o Tr?i ??t th?ng th??ng qua c?ng phong ?n!")

    # Test 4: Realm jumps
    def test_04_realm_jumps(self):
        # Nh?y t? Luy?n Th? l?n T?ng S? ch? trong 5 ch??ng
        valid, msg = self.power_eng.validate_realm_jump("Luy?n Th?", "T?ng S?", 5)
        self.assertFalse(valid, "H? th?ng ph?i ch?n ??t ph? c?nh gi?i nh?y v?t phi l?!")

    # Test 5: Artifact appears without acquisition
    def test_05_artifact_without_acquisition(self):
        char = self.char_eng.get_character("char_minh_an")
        inv = char.get("latest_state", {}).get("inventory", [])
        self.assertNotIn("Chung C?c Chi Ki?m", inv, "V?t ph?m ch?a t?ng thu th?p kh?ng th? t? nhi?n c? trong t?i ??.")

    # Test 6: Foreshadowing forgotten
    def test_06_foreshadowing_forgotten(self):
        # Gieo ph?c b?t ? ch??ng 1, ki?m tra ? ch??ng 80 (v??t ng??ng 50 ch??ng)
        dormant = self.fsh_eng.audit_dormant_seeds(current_chapter=80, threshold_chapters=50)
        self.assertTrue(len(dormant) > 0, "H? th?ng ph?i c?nh b?o ph?c b?t b? b? qu?n qu? l?u!")

    # Test 7: Location contradiction
    def test_07_location_contradiction(self):
        valid, msg = self.world_eng.validate_travel("loc_hcmc", "loc_hcmc", -5.0)
        self.assertFalse(valid, "Th?i gian di chuy?n ?m ho?c m?u thu?n ph?i b? b?t l?i.")

    # Test 8: POV leak (Head hopping)
    def test_08_pov_leak(self):
        text = "T?i b??c ?i tr?n ???ng. Trong l?ng L?m T?ch ngh? r?ng n?i n?y th?t k? l? v? n?ng th?m t?nh to?n k? ho?ch."
        res = self.critique_eng.audit_chapter_draft(1, "Nguy?n Minh An", ["char_minh_an"], text)
        self.assertTrue(any(i["category"] == "POV" for i in res["issues"]), "H? th?ng ph?i b?t l?i Head-hopping khi POV Minh An ??c tr?m suy ngh? L?m T?ch!")

    # Test 9: AUTHOR_SECRET leak
    def test_09_author_secret_leak(self):
        text = "N?i n?y t?ng l? chi?n tr??ng h?ch t?m c?a cu?c chi?n k? nguy?n tr??c."
        res = self.critique_eng.audit_chapter_draft(1, "Nguy?n Minh An", ["char_minh_an"], text)
        self.assertFalse(res["passed"], "H? th?ng ph?i ch?n r? r? b? m?t t?c gi?!")
        self.assertTrue(any(i["category"] == "AUTHOR_SECRET" for i in res["issues"]))

    # Test 10: Research accidentally treated as canon
    def test_10_research_accidentally_treated_as_canon(self):
        items = self.res_vault.get_items()
        for it in items:
            self.assertEqual(it.get("canon_status"), "RESEARCH_ONLY", "Nghi?n c?u ??i th?c kh?ng ???c t? ??ng bi?n th?nh Canon!")

    # Test 11: Minor lore silently changes major canon
    def test_11_minor_lore_silently_changes_major_canon(self):
        # Th? ghi ?? canon LOCKED
        entry = self.canon_eng.get_canon("minh_an_ordinary")
        self.assertEqual(entry["level"], "LOCKED", "Canon LOCKED kh?ng ???c ph?p b? s?a ??i l?n l?t!")

    # Test 12: Rewrite accidentally changes canon
    def test_12_rewrite_accidentally_changes_canon(self):
        # Ki?m tra v?n b?n vi?t l?i ch?a suy ?o?n c?m k?
        rewrite_draft = "Minh An b?t ng? nh?n ra h?n ch?nh l? ng??i chuy?n sinh t? vi?n c?."
        violations = self.canon_eng.validate_text_for_forbidden_assumptions(rewrite_draft)
        self.assertTrue(len(violations) > 0, "B?n vi?t l?i kh?ng ???c vi ph?m canon ?? kh?a!")

    # Test 13: Two simultaneous timelines conflict
    def test_13_two_simultaneous_timelines_conflict(self):
        # Ch??ng 5 ghi nh?n th?i gian s?m h?n Ch??ng 4 m? kh?ng ph?i flashback
        valid, msg = self.time_eng.validate_chronology(5, "2026-09-10T12:00:00+07:00")
        self.assertFalse(valid, "H? th?ng ph?i ph?t hi?n d?ng th?i gian b? ??o ng??c v? l?!")

    # Test 14: Character relationship changes without event
    def test_14_relationship_jump_without_event(self):
        rel = self.rel_eng.get_relationship("char_minh_an", "char_lam_tich")
        # Kh?i ??u m?i quan h? ph?i l? 0 ho?c ch?a nh?n th?c
        self.assertEqual(rel.get("romantic_awareness", 0), 0, "Quan h? t?nh c?m kh?ng ???c nh?y v?t khi ch?a c? bi?n c? t??ng t?c!")

    # Test 15: Minh An suddenly becomes hidden OP
    def test_15_minh_an_suddenly_becomes_hidden_op(self):
        text = "Minh An thi tri?n huy?t m?ch th?n th?nh h?y di?t to?n b? qu?n ??ch sau 3 ng?y tu luy?n."
        violations = self.canon_eng.validate_text_for_forbidden_assumptions(text)
        self.assertTrue(len(violations) >= 2, "H? th?ng ph?i ng?n ch?n Minh An bi?n th?nh hidden OP!")

    # Test 16: L?m T?ch randomly loses/regains power
    def test_16_lam_tich_power_mechanics(self):
        char = self.char_eng.get_character("char_lam_tich")
        self.assertIn("Nguy?n Th?n T?n Phi?n", char["cultivation"]["current_status"])
        # Ph?i c? c? ch? th??ng t?n ??o c?
        self.assertIn("??o c? v? n?t", char["latest_state"]["injuries"])

    # Test 17: Resurrection violates death rules
    def test_17_resurrection_violates_death_rules(self):
        canon_rule = self.canon_eng.get_canon("absolute_death")
        self.assertIn("v?nh vi?n", canon_rule["content"], "Quy t?c c?i ch?t tuy?t ??i ph?i ???c b?o to?n.")

    # Test 18: Earth suddenly becomes stronger than cosmology
    def test_18_earth_power_hierarchy(self):
        node = self.world_eng.get_node("node_trai_dat")
        self.assertEqual(node["rank"], 6, "Tr?i ??t l? v? di?n t?ng th?p nh?t trong ph?n t?ng cosmology hi?n t?i!")

    # Test 19: New cultivation path appears with no logical basis
    def test_19_unauthorized_cultivation_path(self):
        self.assertNotIn("H? Th?ng Hack ?i?m ??o", self.power_eng.systems, "H? th?ng tu luy?n phi l? kh?ng ???c ph?p xu?t hi?n!")

    # Test 20: Chapter 1500 contradicts Chapter 100
    def test_20_long_term_continuity_consistency(self):
        # Gi? l?p s? ki?n ? ch??ng 100 v? ki?m tra t?nh li?n t?c ? ch??ng 1500
        self.time_eng.add_event("EVT-CH100", "L?m T?ch ti?t l? t?n th?t cho Minh An", 100, 1, "2026-10-01T20:00:00+07:00", "loc_hcmc", ["char_minh_an", "char_lam_tich"], "Minh An bi?t t?n L?m T?ch", "Minh An ghi nh?.")
        self.know_eng.set_character_epistemic_status("char_minh_an", "fact_lam_tich_name", "T?n th?t c?a n? nh?n trong th?c h?i l? L?m T?ch", "KNOWN", 100)
        
        status_at_1500 = self.know_eng.get_character_epistemic_status("char_minh_an", "fact_lam_tich_name")
        self.assertEqual(status_at_1500, "KNOWN", "Th?ng tin ?? bi?t ? ch??ng 100 kh?ng ???c b? m?t d?u ? ch??ng 1500!")

    # LONG-FORM MEMORY SIMULATION TEST (Section 104)
    def test_21_long_form_memory_simulation(self):
        """M? ph?ng chu?i 1500 ch??ng: Ch 1 (A introduced) -> Ch 50 (B learns) -> Ch 100 (C false belief) -> Ch 300 (A relevant) -> Ch 700 (B dies) -> Ch 1000 (A returns) -> Ch 1500 (Payoff)."""
        # Ch 1: Gi?i thi?u b? m?t c? v?t A
        self.fsh_eng.plant_seed("FSH-SIM-A", "M?nh ng?c c? mang t?n ni?m c?a Th?n Ma V?c", 1, 1, ["L?m T?ch"], "Ch?a kh?a m? phong ?n c? x?a", payoff_chapter=1500)
        
        # Ch 50: Nh?n v?t B (Minh An) bi?t s? th?t A
        self.know_eng.set_character_epistemic_status("char_minh_an", "fact_ancient_jade", "M?nh ng?c c? l? ch?a kh?a m? phong ?n", "KNOWN", 50)
        self.assertEqual(self.know_eng.get_character_epistemic_status("char_minh_an", "fact_ancient_jade"), "KNOWN")

        # Ch 100: Nh?n v?t C tin v?o phi?n b?n sai l?ch (FALSE_BELIEF)
        self.know_eng.set_character_epistemic_status("char_antagonist_c", "fact_ancient_jade", "M?nh ng?c c? ch? l? ?? phong th?y b?nh th??ng", "FALSE_BELIEF", 100)
        self.assertEqual(self.know_eng.get_character_epistemic_status("char_antagonist_c", "fact_ancient_jade"), "FALSE_BELIEF")

        # Ch 700: Nh?n v?t ??ng minh D ch?t
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO entities (id, name, type, status) VALUES ('char_ally_d', '??ng Minh D', 'character', 'ACTIVE')")
        conn.commit()
        conn.close()
        self.char_eng.mark_dead("char_ally_d", 700, "Hy sinh khi b?o v? tr?n ??a")
        self.assertFalse(self.char_eng.is_alive("char_ally_d"), "??ng minh D ph?i ???c x?c nh?n ?? ch?t v?nh vi?n sau ch??ng 700.")

        # Ch 1500: Payoff ho?n t?t
        self.fsh_eng.update_status("FSH-SIM-A", "PAID", payoff_chapter=1500)
        seeds = self.fsh_eng.list_seeds(status="PAID")
        self.assertTrue(any(s["id"] == "FSH-SIM-A" for s in seeds), "Ph?c b?t gieo t? ch??ng 1 ph?i ???c thu h?i tr?n v?n t?i ch??ng 1500!")

if __name__ == "__main__":
    unittest.main()
