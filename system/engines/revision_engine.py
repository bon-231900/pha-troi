import os
import re

class RevisionEngine:
    def auto_fix_minor_issues(self, text: str, issues: list) -> str:
        """T? ??ng s?a c?c l?i nh? v? phong c?ch, s?o ng? m? kh?ng l?m thay ??i n?i dung canon."""
        refined_text = text
        for iss in issues:
            if iss.get("category") == "STYLE":
                # Thay th? c?c c?m t? s?o ng? r? ti?n
                refined_text = re.sub(r'(?i)v? h?n kh?ng bi?t r?ng[,:]?', '', refined_text)
                refined_text = re.sub(r'(?i)h?n v?nh vi?n kh?ng th? ng? ???c[,:]?', '', refined_text)
        return refined_text
