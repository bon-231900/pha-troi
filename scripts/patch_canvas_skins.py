# -*- coding: utf-8 -*-
with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add equippedSkinId to CommunityPanoramicForgeCanvasProps
old_props = """interface CommunityPanoramicForgeCanvasProps {
  activeStance?: StanceKey;
  onAnvilHit?: (x: number, y: number) => void;
  bossHpPct?: number;
  skyState?: number;
  isHitFlashing?: boolean;
  playerName?: string;
}"""

new_props = """interface CommunityPanoramicForgeCanvasProps {
  activeStance?: StanceKey;
  onAnvilHit?: (x: number, y: number) => void;
  bossHpPct?: number;
  skyState?: number;
  isHitFlashing?: boolean;
  playerName?: string;
  equippedSkinId?: string;
}"""

if old_props not in content:
    old_props = old_props.replace("\n", "\r\n")
    new_props = new_props.replace("\n", "\r\n")
content = content.replace(old_props, new_props, 1)

# 2. Add equippedSkinId to component destructuring
old_destruct = """    const {
      activeStance = 'Q',
      onAnvilHit,
      bossHpPct = 100,
      skyState = 1,
      isHitFlashing = false,
      playerName = 'Thợ Rèn Tiêu Dao',
    } = props;"""

new_destruct = """    const {
      activeStance = 'Q',
      onAnvilHit,
      bossHpPct = 100,
      skyState = 1,
      isHitFlashing = false,
      playerName = 'Thợ Rèn Tiêu Dao',
      equippedSkinId = 'skin_default',
    } = props;"""

if old_destruct not in content:
    old_destruct = old_destruct.replace("\n", "\r\n")
    new_destruct = new_destruct.replace("\n", "\r\n")
content = content.replace(old_destruct, new_destruct, 1)

# 3. Add skin image cache ref and loader
old_ref = "  const playerNameRef = useRef<string>(playerName);"
new_ref = """  const playerNameRef = useRef<string>(playerName);
  const skinSpritesRef = useRef<Map<string, HTMLImageElement>>(new Map());
  const equippedSkinIdRef = useRef<string>(equippedSkinId);
  equippedSkinIdRef.current = equippedSkinId;

  // Preload equipped skin
  useEffect(() => {
    if (!equippedSkinId) return;
    const base = import.meta.env.BASE_URL || '/';
    const cleanBase = base.endsWith('/') ? base : `${base}/`;
    if (!skinSpritesRef.current.has(equippedSkinId)) {
      const img = new Image();
      img.src = `${cleanBase}assets/art/skins/${equippedSkinId}/spritesheet_strip.webp`;
      skinSpritesRef.current.set(equippedSkinId, img);
    }
  }, [equippedSkinId]);"""

if old_ref not in content:
    old_ref = old_ref.replace("\n", "\r\n")
    new_ref = new_ref.replace("\n", "\r\n")
content = content.replace(old_ref, new_ref, 1)

# 4. Use custom skin sheet if loaded when drawing hero
old_draw_hero = """        // ---------------------------------------------------------------------
        // LAYER 11: MAIN HERO (BALANCED 0.38 SCALE, EQUAL PROMINENCE)
        // ---------------------------------------------------------------------
        if (assets.heroSheet.loaded) {
          const sheet = assets.heroSheet.img;"""

new_draw_hero = """        // ---------------------------------------------------------------------
        // LAYER 11: MAIN HERO (BALANCED 0.38 SCALE, EQUAL PROMINENCE)
        // ---------------------------------------------------------------------
        if (assets.heroSheet.loaded) {
          const currentSkinId = equippedSkinIdRef.current || 'skin_default';
          const customSkinImg = skinSpritesRef.current.get(currentSkinId);
          const sheet = (customSkinImg && customSkinImg.complete && customSkinImg.naturalWidth > 0)
            ? customSkinImg
            : assets.heroSheet.img;"""

if old_draw_hero not in content:
    old_draw_hero = old_draw_hero.replace("\n", "\r\n")
    new_draw_hero = new_draw_hero.replace("\n", "\r\n")
content = content.replace(old_draw_hero, new_draw_hero, 1)

with open('frontend/src/components/CommunityPanoramicForgeCanvas.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: CommunityPanoramicForgeCanvas.tsx patched with skin support!")
