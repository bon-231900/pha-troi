with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

target1 = '''  equippedSkinId?: string;
  onEquipSkin?: (skinId: string) => void;
}'''

replacement1 = '''  equippedSkinId?: string;
  onEquipSkin?: (skinId: string) => void;
  onOpenGuide?: () => void;
}'''

target2 = '''  equippedSkinId = 'skin_default',
  onEquipSkin,
}) => {'''

replacement2 = '''  equippedSkinId = 'skin_default',
  onEquipSkin,
  onOpenGuide,
}) => {'''

target3 = '''              {/* 2B. Tủ Đồ Tiên Gia: 5 Bộ Y Phục Môn Phái */}'''

replacement3 = '''              {/* Hướng Dẫn & Cẩm Nang Bí Kíp Button */}
              {onOpenGuide && (
                <button
                  type="button"
                  onClick={onOpenGuide}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-cyan-950/40 hover:bg-cyan-900/50 text-cyan-200 border border-cyan-500/50 hover:border-cyan-400 font-tech font-bold text-xs shadow-md cursor-pointer transition-all active:scale-[0.98]"
                  title="Mở cẩm nang hướng dẫn luật chơi, lò rèn, đe và các chiêu thức"
                >
                  <span className="text-base">📜</span>
                  <span>XEM CẨM NANG BÍ KÍP RÈN ĐÚC [?]</span>
                </button>
              )}

              {/* 2B. Tủ Đồ Tiên Gia: 5 Bộ Y Phục Môn Phái */}'''

assert target1 in c, 'Target 1 not found'
assert target2 in c, 'Target 2 not found'
assert target3 in c, 'Target 3 not found'

c = c.replace(target1, replacement1, 1)
c = c.replace(target2, replacement2, 1)
c = c.replace(target3, replacement3, 1)

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated StatusModal.tsx successfully!')
