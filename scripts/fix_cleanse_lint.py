def fix_errors():
    # 1. Fix rules.ts
    path_rules = 'frontend/src/game/rules.ts'
    with open(path_rules, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace("(isGolden ? 8 : 4)", "(isCrit ? 8 : 4)")
    c = c.replace("(isGolden ? 2 : 1)", "(isCrit ? 2 : 1)")
    c = c.replace("(isGolden ? 25 : 12)", "(isCrit ? 25 : 12)")
    c = c.replace("(isGolden ? 6 : 2)", "(isCrit ? 6 : 2)")
    c = c.replace("(isGolden ? 20 : 8)", "(isCrit ? 20 : 8)")
    c = c.replace("    isGolden,\n    isGlancingHit,", "    isGolden: false,\n    isGlancingHit,")
    with open(path_rules, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed rules.ts!")

    # 2. Fix App.tsx
    path_app = 'frontend/src/App.tsx'
    with open(path_app, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace("if (grade === 'PERFECT') {", "if (isCritHit) {")
    c = c.replace("const grade: JudgmentGrade = 'GREAT';", "const grade: JudgmentGrade = isCritHit ? 'PERFECT' : 'GREAT';")
    with open(path_app, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed App.tsx!")

    # 3. Fix CommunityPanoramicForgeCanvas.tsx
    path_canvas = 'frontend/src/components/CommunityPanoramicForgeCanvas.tsx'
    with open(path_canvas, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace("const sparkCount = forceGolden ? 48 : 34;", "const sparkCount = isCrit ? 44 : 24;")
    with open(path_canvas, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed CommunityPanoramicForgeCanvas.tsx!")

    # 4. Fix InteractiveAltarPreview.tsx
    path_preview = 'frontend/src/components/InteractiveAltarPreview.tsx'
    with open(path_preview, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace("soundEngine.playAnvilStrike(rating === 'HIT' ? 'GREAT' : rating, stanceKey, rating === 'PERFECT');", "soundEngine.playAnvilStrike(rating, stanceKey, isCrit);")
    with open(path_preview, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed InteractiveAltarPreview.tsx!")

if __name__ == '__main__':
    fix_errors()
