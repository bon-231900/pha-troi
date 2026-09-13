import json
import os
from system.core.config import ROOT_DIR

class PowerEngine:
    REALM_RANKS = {
        # Kh? Huy?t ??o (Earth)
        "Luy?n Th?": 1, "Kh? C?m": 2, "Kh? H?i": 3, "Ti?n Thi?n": 4,
        "T?ng S?": 5, "??i T?ng S?": 6, "Ph? C?nh": 7,
        # Linh ??o
        "T? Kh?": 1, "Khai M?ch": 2, "Linh H?i": 3, "Nguy?n ?an": 4, "Nguy?n Anh": 5,
        "H?a Th?n": 6, "Ph?n H?": 7, "H?p ??o": 8, "Thi?n M?n": 9, "Ch? T?n": 10
    }

    def __init__(self):
        self.systems_file = os.path.join(ROOT_DIR, "canon", "cultivation", "cultivation_systems.json")
        with open(self.systems_file, "r", encoding="utf-8") as f:
            self.systems = json.load(f)["paths"]

    def validate_realm_jump(self, old_realm: str, new_realm: str, chapters_elapsed: int) -> tuple[bool, str]:
        if old_realm == new_realm or old_realm == "Ph?m nh?n":
            return True, "H?p l?."
        old_rank = self.REALM_RANKS.get(old_realm, 0)
        new_rank = self.REALM_RANKS.get(new_realm, 0)
        
        # Nh?y v?t qu? 2 c?nh gi?i trong th?i gian ng?n
        if new_rank - old_rank > 1 and chapters_elapsed < 30:
            return False, f"REALM_JUMP_VIOLATION: ??t ph? t? {old_realm} l?n {new_realm} ch? trong {chapters_elapsed} ch??ng l? vi ph?m nguy?n t?c tu luy?n ch?m r?i!"
        return True, "H?p l?."

    def evaluate_combat(self, attacker_realm: str, defender_realm: str, tactical_advantages: list) -> dict:
        """Ki?m tra chi?n ??u: C?nh gi?i cao kh?ng t? ??ng th?ng n?u ??i ph??ng c? ??a h?nh, ph?p b?o, th??ng th?."""
        att_rank = self.REALM_RANKS.get(attacker_realm, 1)
        def_rank = self.REALM_RANKS.get(defender_realm, 1)
        rank_diff = att_rank - def_rank

        base_win_prob = 0.5 + (rank_diff * 0.15)
        # B? tr? l?i th? chi?n thu?t
        tactical_mod = len(tactical_advantages) * 0.1
        final_score = base_win_prob - tactical_mod
        
        return {
            "attacker_realm": attacker_realm,
            "defender_realm": defender_realm,
            "rank_difference": rank_diff,
            "tactical_modifier": tactical_mod,
            "can_defender_win": final_score < 0.7 or len(tactical_advantages) >= 3,
            "rule": "Chi?n ??u ph? thu?c ?i?u ki?n, ph?p b?o, chu?n b? v? th??ng th?."
        }
