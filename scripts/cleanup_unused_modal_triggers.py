# -*- coding: utf-8 -*-
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove onOpenClassModal from TopBossHeader call
code = code.replace("        onOpenClassModal={() => setShowClassModal(true)}\n", "")
code = code.replace("        onOpenClassModal={() => setShowClassModal(true)}\r\n", "")

# 2. Remove onOpenClassSelect from ClassSkillBar call
code = code.replace("        onOpenClassSelect={() => setShowClassModal(true)}\n", "")
code = code.replace("        onOpenClassSelect={() => setShowClassModal(true)}\r\n", "")

# 3. Remove onOpenClassModal from RightProgressionPanel call
code = code.replace("            onOpenClassModal={() => setShowClassModal(true)}\n", "")
code = code.replace("            onOpenClassModal={() => setShowClassModal(true)}\r\n", "")

# 4. Remove const [showClassModal, setShowClassModal] = useState<boolean>(false);
code = code.replace("  const [showClassModal, setShowClassModal] = useState<boolean>(false);\n", "")
code = code.replace("  const [showClassModal, setShowClassModal] = useState<boolean>(false);\r\n", "")

# 5. Remove setShowClassModal(false); in handleCommitClass
code = code.replace("      setShowClassModal(false);\n", "")
code = code.replace("      setShowClassModal(false);\r\n", "")

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Cleaned up App.tsx triggers!")
