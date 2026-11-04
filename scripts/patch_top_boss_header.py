# -*- coding: utf-8 -*-
with open('frontend/src/components/TopBossHeader.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add import
old_import = """import { GoogleUserProfile } from '../game/googleAuth';"""
new_import = """import { GoogleUserProfile } from '../game/googleAuth';
import { PlayerClassMeta } from '../game/rules';"""
code = code.replace(old_import, new_import, 1)

# 2. Add props
old_props = """  googleProfile?: GoogleUserProfile | null;
  onGoogleLogin?: () => void;
  onGoogleLogout?: () => void;
}"""

new_props = """  googleProfile?: GoogleUserProfile | null;
  onGoogleLogin?: () => void;
  onGoogleLogout?: () => void;
  playerClass?: PlayerClassMeta;
  onOpenClassModal?: () => void;
}"""
code = code.replace(old_props, new_props, 1)

# 3. Add destructuring
old_destruct = """  googleProfile = null,
  onGoogleLogin,
  onGoogleLogout,
}) => {"""

new_destruct = """  googleProfile = null,
  onGoogleLogin,
  onGoogleLogout,
  playerClass,
  onOpenClassModal,
}) => {"""
code = code.replace(old_destruct, new_destruct, 1)

# 4. Insert Badge in Right Floating Capsule
target_pos = """        {/* Google Cloud Save Button or User Profile */}"""
badge_code = """        {/* Player Class / Sect Commitment Badge */}
        {playerClass && (
          <button
            type="button"
            onClick={onOpenClassModal}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-tech font-bold shadow-md border cursor-pointer transition-all hover:scale-105 active:scale-95 ${playerClass.badgeBg}`}
            title={`${playerClass.name} - ${playerClass.sectTitle} (Nhấn để xem kỹ năng hoặc đổi phái)`}
          >
            <span>{playerClass.icon}</span>
            <span className="hidden md:inline font-bold">{playerClass.name}</span>
          </button>
        )}

        {/* Google Cloud Save Button or User Profile */}"""

code = code.replace(target_pos, badge_code, 1)

with open('frontend/src/components/TopBossHeader.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated TopBossHeader.tsx with Class Badge!")
