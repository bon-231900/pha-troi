# -*- coding: utf-8 -*-
"""
Novel OS — RevisionEngine (Động cơ Hiệu đính & Đề xuất Bản vá Văn xuôi)
Thay thế việc xóa chuỗi mù quáng (blind regex) bằng cơ chế đề xuất bản vá (Patch / Diff) minh bạch.
Tách biệt: Phát hiện -> Tạo Patch Đề xuất -> Tác giả duyệt -> Áp dụng có thể hoàn tác.
"""
import re
import difflib

class RevisionEngine:
    KNOWN_CLICHES = [
        (re.compile(r'\s*và hắn không biết rằng[,:\s]*', re.IGNORECASE), ' '),
        (re.compile(r'\s*hắn vĩnh viễn không thể ngờ được[,:\s]*', re.IGNORECASE), ' '),
        (re.compile(r'\s*chuyện gì đến cũng phải đến[,:\s]*', re.IGNORECASE), ' ')
    ]

    def propose_patches(self, text: str, issues: list) -> list:
        """Tạo danh sách các bản vá đề xuất (Suggested Patches / Diffs) để tác giả xem xét trước khi áp dụng."""
        patches = []
        for iss in issues:
            cat = iss.get("category", "")
            desc = iss.get("description", "")
            
            if cat == "STYLE":
                for pattern, replacement in self.KNOWN_CLICHES:
                    match = pattern.search(text)
                    if match:
                        span = match.span()
                        orig_segment = text[max(0, span[0]-20):min(len(text), span[1]+20)]
                        fixed_segment = pattern.sub(replacement, orig_segment)
                        patches.append({
                            "category": "STYLE",
                            "original": match.group(0),
                            "replacement": replacement.strip(),
                            "context_before": orig_segment,
                            "context_after": fixed_segment,
                            "rationale": f"Loại bỏ sáo ngữ giật gân rẻ tiền ({desc})"
                        })
            elif cat == "CONSISTENCY" and "->" in desc:
                # Đề xuất sửa chính tả tên nhân vật: 'Minh Ánh' -> 'Nguyễn Minh An'
                m = re.search(r"'([^']+)'\s*->\s*Tên chuẩn là\s*'([^']+)'", desc)
                if m:
                    wrong, correct = m.group(1), m.group(2)
                    if wrong.lower() in text.lower():
                        patches.append({
                            "category": "CONSISTENCY",
                            "original": wrong,
                            "replacement": correct,
                            "rationale": f"Chuẩn hóa chính tả tên nhân vật theo Canon: {wrong} -> {correct}"
                        })
        return patches

    def generate_diff(self, original_text: str, revised_text: str) -> str:
        """Sinh chuỗi so sánh Unified Diff trực quan giữa bản gốc và bản hiệu đính."""
        orig_lines = original_text.splitlines(keepends=True)
        rev_lines = revised_text.splitlines(keepends=True)
        diff = difflib.unified_diff(orig_lines, rev_lines, fromfile="Bản gốc", tofile="Bản hiệu đính", lineterm="")
        return "".join(diff)

    def auto_fix_minor_issues(self, text: str, issues: list) -> str:
        """Tự động sửa các lỗi nhỏ (STYLE, TYPO) có kiểm soát, làm sạch dấu câu và khoảng trắng thừa.
        Giữ tính tương thích ngược với CoAuthorEngine."""
        refined_text = text
        for iss in issues:
            if iss.get("category") == "STYLE":
                for pattern, replacement in self.KNOWN_CLICHES:
                    refined_text = pattern.sub(replacement, refined_text)
            elif iss.get("category") == "CONSISTENCY":
                desc = iss.get("description", "")
                m = re.search(r"'([^']+)'\s*->\s*Tên chuẩn là\s*'([^']+)'", desc)
                if m:
                    wrong, correct = m.group(1), m.group(2)
                    refined_text = re.sub(re.escape(wrong), correct, refined_text, flags=re.IGNORECASE)

        # Dọn dẹp khoảng trắng kép và lỗi dấu phẩy đứng đầu câu do xóa cụm từ
        refined_text = re.sub(r' +', ' ', refined_text)
        refined_text = re.sub(r'\n +', '\n', refined_text)
        refined_text = re.sub(r'([.!?])\s*[,:]', r'\1', refined_text)
        return refined_text.strip()
