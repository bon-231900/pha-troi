# -*- coding: utf-8 -*-
import json
import os
from system.core.config import ROOT_DIR

class PowerEngine:
    REALM_RANKS = {
        "Phàm nhân": 0,
        # Khí Huyết Đạo (Earth)
        "Luyện Thể": 1, "Khí Cảm": 2, "Khí Hải": 3, "Tiên Thiên": 4,
        "Tông Sư": 5, "Đại Tông Sư": 6, "Phá Cảnh": 7,
        # Linh Đạo
        "Tụ Khí": 1, "Khai Mạch": 2, "Linh Hải": 3, "Nguyên Đan": 4, "Nguyên Anh": 5,
        "Hóa Thần": 6, "Phản Hư": 7, "Hợp Đạo": 8, "Thiên Môn": 9, "Chí Tôn": 10
    }

    def __init__(self):
        self.systems_file = os.path.join(ROOT_DIR, "canon", "cultivation", "cultivation_systems.json")
        with open(self.systems_file, "r", encoding="utf-8") as f:
            self.systems = json.load(f)["paths"]

    def validate_realm_jump(self, old_realm: str, new_realm: str, chapters_elapsed: int) -> tuple[bool, str]:
        if old_realm == new_realm:
            return True, "Hợp lệ."
        old_rank = self.REALM_RANKS.get(old_realm, 0)
        new_rank = self.REALM_RANKS.get(new_realm, 0)
        
        # Nhảy vọt quá 1 cảnh giới trong thời gian dưới 30 chương
        if new_rank - old_rank > 1 and chapters_elapsed < 30:
            return False, f"REALM_JUMP_VIOLATION: Đột phá từ {old_realm} lên {new_realm} chỉ trong {chapters_elapsed} chương là vi phạm nguyên tắc tu luyện chậm rãi!"
        return True, "Hợp lệ."

    def evaluate_combat(self, attacker_realm: str, defender_realm: str, tactical_advantages: list) -> dict:
        att_rank = self.REALM_RANKS.get(attacker_realm, 1)
        def_rank = self.REALM_RANKS.get(defender_realm, 1)
        rank_diff = att_rank - def_rank
        base_win_prob = 0.5 + (rank_diff * 0.15)
        tactical_mod = len(tactical_advantages) * 0.1
        final_score = base_win_prob - tactical_mod
        
        return {
            "attacker_realm": attacker_realm,
            "defender_realm": defender_realm,
            "rank_difference": rank_diff,
            "tactical_modifier": tactical_mod,
            "can_defender_win": final_score < 0.7 or len(tactical_advantages) >= 3,
            "rule": "Chiến đấu phụ thuộc điều kiện, pháp bảo, chuẩn bị và thương thế."
        }
