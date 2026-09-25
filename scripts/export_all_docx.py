# -*- coding: utf-8 -*-
"""
Export all cleaned Markdown chapters to Docx files matching directory structure.
Handles both YAML frontmatter and standard Markdown headers.
"""
import os
import glob
import re
import sys

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.engines.docx_pipeline import DocxPipeline

def export_all():
    pipeline = DocxPipeline()
    md_files = glob.glob(os.path.join(BASE_DIR, 'manuscript', 'markdown', '**', '*.md'), recursive=True)
    count = 0
    for mf in sorted(md_files):
        with open(mf, 'r', encoding='utf-8') as f:
            content = f.read()

        ch_num = None
        title = None

        # 1. Try filename ch_XXX.md
        fn_match = re.search(r'ch_(\d+)\.md', os.path.basename(mf))
        if fn_match:
            ch_num = int(fn_match.group(1))

        # 2. Try YAML frontmatter
        ch_yaml = re.search(r'chapter:\s*(\d+)', content)
        if ch_yaml:
            ch_num = int(ch_yaml.group(1))
        title_yaml = re.search(r'title:\s*["\']?(.*?)["\']?\n', content)
        if title_yaml:
            title = title_yaml.group(1).strip()

        # 3. Try Markdown header
        if not title:
            header_match = re.search(r'^#\s*(?:CHƯƠNG|Chương)\s*\d+[:\-—\s]+(.*?)$', content, re.MULTILINE)
            if header_match:
                title = header_match.group(1).strip()

        if ch_num is None:
            continue
        if not title:
            title = f"Chương {ch_num}"

        rel_path = os.path.relpath(mf, os.path.join(BASE_DIR, 'manuscript', 'markdown'))
        docx_rel = os.path.splitext(rel_path)[0] + '.docx'
        docx_path = os.path.join(BASE_DIR, 'manuscript', 'word', docx_rel)

        pipeline.export_chapter_to_docx(title, ch_num, content, docx_path)
        count += 1

    print(f"Đã xuất bản thành công toàn bộ {count} chương sang định dạng Word (.docx)!")

if __name__ == '__main__':
    export_all()
