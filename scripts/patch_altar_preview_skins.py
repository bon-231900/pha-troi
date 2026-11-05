# -*- coding: utf-8 -*-
with open('frontend/src/components/InteractiveAltarPreview.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_imp = "import { PlayerClassId, PLAYER_CLASSES, StanceKey } from '../game/rules';"
new_imp = "import { PlayerClassId, PLAYER_CLASSES, StanceKey, SECT_DEFAULT_SKIN, CHARACTER_SKINS } from '../game/rules';"
if old_imp not in content:
    old_imp = old_imp.replace("\n", "\r\n")
    new_imp = new_imp.replace("\n", "\r\n")
content = content.replace(old_imp, new_imp, 1)

# 2. Add skinId to InteractiveAltarPreviewProps
old_props = """interface InteractiveAltarPreviewProps {
  selectedClassId: PlayerClassId;
  characterName: string;
  onStrikeStatsUpdate?: (stats: { totalStrikes: number; perfectStrikes: number; lastRating: string }) => void;
}"""

new_props = """interface InteractiveAltarPreviewProps {
  selectedClassId: PlayerClassId;
  characterName: string;
  skinId?: string;
  onStrikeStatsUpdate?: (stats: { totalStrikes: number; perfectStrikes: number; lastRating: string }) => void;
}"""
if old_props not in content:
    old_props = old_props.replace("\n", "\r\n")
    new_props = new_props.replace("\n", "\r\n")
content = content.replace(old_props, new_props, 1)

# 3. Update component destructured props
old_comp = "export const InteractiveAltarPreview = forwardRef<InteractiveAltarPreviewRef, InteractiveAltarPreviewProps>(\n  ({ selectedClassId, characterName, onStrikeStatsUpdate }, ref) => {"
new_comp = "export const InteractiveAltarPreview = forwardRef<InteractiveAltarPreviewRef, InteractiveAltarPreviewProps>(\n  ({ selectedClassId, characterName, skinId, onStrikeStatsUpdate }, ref) => {"
if old_comp not in content:
    old_comp = old_comp.replace("\n", "\r\n")
    new_comp = new_comp.replace("\n", "\r\n")
content = content.replace(old_comp, new_comp, 1)

# 4. Update asset loader to support dynamic skin switching
old_loader = """  // Asset image refs
  const altarImgRef = useRef<HTMLImageElement | null>(null);
  const heroSheetRef = useRef<HTMLImageElement | null>(null);
  const assetsLoadedRef = useRef<boolean>(false);

  // Load assets once
  useEffect(() => {
    let active = true;
    const base = import.meta.env.BASE_URL || '/';
    const cleanBase = base.endsWith('/') ? base : `${base}/`;

    const altarImg = new Image();
    const heroImg = new Image();

    let loadedCount = 0;
    const onAssetLoad = () => {
      loadedCount++;
      if (loadedCount >= 2 && active) {
        altarImgRef.current = altarImg;
        heroSheetRef.current = heroImg;
        assetsLoadedRef.current = true;
      }
    };

    altarImg.onload = onAssetLoad;
    heroImg.onload = onAssetLoad;

    altarImg.src = `${cleanBase}assets/art/altar_platform.webp`;
    heroImg.src = `${cleanBase}assets/art/hero_spritesheet_strip.webp`;

    if (altarImg.complete) onAssetLoad();
    if (heroImg.complete) onAssetLoad();

    return () => {
      active = false;
    };
  }, []);"""

new_loader = """  // Asset image refs
  const altarImgRef = useRef<HTMLImageElement | null>(null);
  const heroSheetRef = useRef<HTMLImageElement | null>(null);
  const skinCacheRef = useRef<Map<string, HTMLImageElement>>(new Map());
  const assetsLoadedRef = useRef<boolean>(false);

  // Effective skin for this class
  const activeSkinId = skinId || SECT_DEFAULT_SKIN[selectedClassId] || 'skin_default';

  // Base platform asset loader
  useEffect(() => {
    let active = true;
    const base = import.meta.env.BASE_URL || '/';
    const cleanBase = base.endsWith('/') ? base : `${base}/`;

    const altarImg = new Image();
    altarImg.onload = () => {
      if (active) {
        altarImgRef.current = altarImg;
        assetsLoadedRef.current = true;
      }
    };
    altarImg.src = `${cleanBase}assets/art/altar_platform.webp`;
    if (altarImg.complete) {
      altarImgRef.current = altarImg;
      assetsLoadedRef.current = true;
    }

    return () => {
      active = false;
    };
  }, []);

  // Dynamic Skin Spritesheet Loader (instant cached switching)
  useEffect(() => {
    let active = true;
    const base = import.meta.env.BASE_URL || '/';
    const cleanBase = base.endsWith('/') ? base : `${base}/`;

    const cached = skinCacheRef.current.get(activeSkinId);
    if (cached && cached.complete) {
      heroSheetRef.current = cached;
      return;
    }

    const skinMeta = CHARACTER_SKINS[activeSkinId];
    const srcPath = skinMeta ? `${cleanBase}${skinMeta.spritesheetPath}` : `${cleanBase}assets/art/hero_spritesheet_strip.webp`;
    const skinImg = new Image();
    skinImg.onload = () => {
      if (active) {
        skinCacheRef.current.set(activeSkinId, skinImg);
        heroSheetRef.current = skinImg;
      }
    };
    skinImg.src = srcPath;
    if (skinImg.complete) {
      skinCacheRef.current.set(activeSkinId, skinImg);
      heroSheetRef.current = skinImg;
    }

    return () => {
      active = false;
    };
  }, [activeSkinId]);"""

if old_loader not in content:
    old_loader = old_loader.replace("\n", "\r\n")
    new_loader = new_loader.replace("\n", "\r\n")
content = content.replace(old_loader, new_loader, 1)

with open('frontend/src/components/InteractiveAltarPreview.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: InteractiveAltarPreview.tsx patched with dynamic skin support!")
