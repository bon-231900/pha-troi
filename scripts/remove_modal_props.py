# -*- coding: utf-8 -*-

# 1. ClassSkillBar.tsx
with open('frontend/src/components/ClassSkillBar.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("  onOpenClassSelect?: () => void;\n", "")
c = c.replace("  onOpenClassSelect?: () => void;\r\n", "")
c = c.replace("  onOpenClassSelect,\n", "")
c = c.replace("  onOpenClassSelect,\r\n", "")
with open('frontend/src/components/ClassSkillBar.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

# 2. RightProgressionPanel.tsx
with open('frontend/src/components/RightProgressionPanel.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("  onOpenClassModal?: () => void;\n", "")
c = c.replace("  onOpenClassModal?: () => void;\r\n", "")
c = c.replace("  onOpenClassModal,\n", "")
c = c.replace("  onOpenClassModal,\r\n", "")
with open('frontend/src/components/RightProgressionPanel.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

# 3. TopBossHeader.tsx
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("  onOpenClassModal?: () => void;\n", "")
c = c.replace("  onOpenClassModal?: () => void;\r\n", "")
c = c.replace("  onOpenClassModal,\n", "")
c = c.replace("  onOpenClassModal,\r\n", "")
with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("Props successfully removed!")
