with open(r'frontend\src\components\RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

dup = """              {/* Daoist Filigree Divider */}
              <div className="flex items-center justify-center my-1.5 opacity-85 pointer-events-none">
                <img
                  src="./assets/art/ui/arsenal/board_divider_filigree.webp"
                  alt=""
                  className="w-full max-w-[340px] h-3.5 object-contain"
                />
              </div>
              {/* Daoist Filigree Divider */}
              <div className="flex items-center justify-center my-1.5 opacity-85 pointer-events-none">
                <img
                  src="./assets/art/ui/arsenal/board_divider_filigree.webp"
                  alt=""
                  className="w-full max-w-[340px] h-3.5 object-contain"
                />
              </div>"""

single = """              {/* Daoist Filigree Divider */}
              <div className="flex items-center justify-center my-2 opacity-90 pointer-events-none">
                <img
                  src="./assets/art/ui/arsenal/board_divider_filigree.webp"
                  alt=""
                  className="w-full max-w-[360px] h-4 object-contain drop-shadow"
                />
              </div>"""

if dup in c:
    c = c.replace(dup, single)
    with open(r'frontend\src\components\RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed duplicate divider")
