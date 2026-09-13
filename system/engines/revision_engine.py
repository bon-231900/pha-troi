# -*- coding: utf-8 -*-
import os
import re

class RevisionEngine:
    def auto_fix_minor_issues(self, text: str, issues: list) -> str:
        """Tự động sửa các lỗi nhỏ về phong cách, sáo ngữ mà không làm thay đổi nội dung canon."""
        refined_text = text
        for iss in issues:
            if iss.get("category") == "STYLE":
                refined_text = re.sub(r'(?i)và hắn không biết rằng[,:]?', '', refined_text)
                refined_text = re.sub(r'(?i)hắn vĩnh viễn không thể ngờ được[,:]?', '', refined_text)
        return refined_text
