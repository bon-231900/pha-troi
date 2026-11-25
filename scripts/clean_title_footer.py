def clean_title():
    path = 'frontend/src/components/TitleScreenModal.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    old_text = "<div>Space / Chạm: Đập Đe Canh Nhịp • Q W E R: 4 Thế Búa</div>"
    new_text = "<div>Chạm màn hình / Space: Nện Búa Rèn • Q W E R: 4 Kỹ Pháp Môn Phái</div>"
    assert old_text in c, "Could not find old_text in TitleScreenModal.tsx"
    c = c.replace(old_text, new_text, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Cleaned TitleScreenModal.tsx footer text!")

if __name__ == '__main__':
    clean_title()
