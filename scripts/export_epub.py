# -*- coding: utf-8 -*-
"""Script đóng gói toàn bộ 46 chương Quyển 1 thành tệp sách điện tử EPUB hoàn chỉnh."""

import os
import re
import markdown
from ebooklib import epub

def export_novel_to_epub():
    base_dir = r"d:\tieu-thuyet"
    manuscript_dir = os.path.join(base_dir, "manuscript", "markdown", "volume_01", "arc_01")
    output_dir = os.path.join(base_dir, "exports")
    os.makedirs(output_dir, exist_ok=True)
    epub_path = os.path.join(output_dir, "Pha_Troi_Quyen_1.epub")

    book = epub.EpubBook()
    book.set_identifier("pha-troi-vol-01-arc-01")
    book.set_title("Phá Trời — Quyển 1: Cố Thổ Thức Tỉnh")
    book.set_language("vi")
    book.add_author("Tác giả Phá Trời")

    css_style = """
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Bookerly", "Georgia", "Palatino", serif;
        line-height: 1.8;
        padding: 0 4%;
        text-align: justify;
    }
    h1 {
        text-align: center;
        font-size: 1.5em;
        line-height: 1.35;
        margin-top: 1.5em;
        margin-bottom: 1.2em;
        font-weight: bold;
    }
    p {
        text-indent: 1.6em;
        margin-top: 0;
        margin-bottom: 0.8em;
    }
    strong {
        font-weight: bold;
    }
    em {
        font-style: italic;
    }
    hr {
        border: none;
        border-top: 1px dashed #999999;
        margin: 2em auto;
        width: 60%;
    }
    """
    default_css = epub.EpubItem(
        uid="style_default",
        file_name="style/default.css",
        media_type="text/css",
        content=css_style
    )
    book.add_item(default_css)

    files = sorted([f for f in os.listdir(manuscript_dir) if f.endswith(".md") and f.startswith("ch_")])
    chapters = []
    toc = []

    for idx, f in enumerate(files, 1):
        file_path = os.path.join(manuscript_dir, f)
        with open(file_path, "r", encoding="utf-8") as file:
            raw_text = file.read()

        # Tách bỏ YAML frontmatter
        body = raw_text
        if raw_text.startswith("---"):
            parts = raw_text.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].strip()

        # Lấy tiêu đề chương
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Chương {idx}"

        # Chuyển đổi Markdown sang HTML
        html_body = markdown.markdown(body, extensions=["extra"])

        # Tạo trang chương
        ch_id = f.replace(".md", "")
        ch = epub.EpubHtml(title=title, file_name=f"{ch_id}.xhtml", lang="vi")
        ch.set_content(f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="style/default.css" type="text/css"/>
</head>
<body>
{html_body}
</body>
</html>""")
        ch.add_item(default_css)
        book.add_item(ch)
        chapters.append(ch)
        toc.append(ch)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + chapters

    epub.write_epub(epub_path, book)
    file_size_kb = os.path.getsize(epub_path) / 1024
    print(f"[+] Đã tạo thành công tệp EPUB: {epub_path}")
    print(f"    - Tổng số chương: {len(chapters)}")
    print(f"    - Dung lượng: {file_size_kb:.1f} KB")
    return epub_path

if __name__ == "__main__":
    export_novel_to_epub()
