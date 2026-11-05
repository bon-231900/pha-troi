# Fix StatusModal.tsx imports
with open('frontend/src/components/StatusModal.tsx', 'r', encoding='utf-8') as f:
    sm = f.read()

old_sm_import = "import { PlayerClassMeta } from '../game/rules';"
new_sm_import = "import { PlayerClassMeta, CHARACTER_SKINS } from '../game/rules';\nimport { Sparkles } from 'lucide-react';"

assert old_sm_import in sm, 'old_sm_import not found'
sm = sm.replace(old_sm_import, new_sm_import, 1)

with open('frontend/src/components/StatusModal.tsx', 'w', encoding='utf-8') as f:
    f.write(sm)
print('StatusModal.tsx imports fixed!')

# Fix App.tsx imports
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    app = f.read()

old_app_import = "  QUENCH_OPTIONS,\n} from './game/rules';"
new_app_import = "  QUENCH_OPTIONS,\n  SECT_DEFAULT_SKIN,\n  CHARACTER_SKINS,\n} from './game/rules';"

assert old_app_import in app, 'old_app_import not found'
app = app.replace(old_app_import, new_app_import, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app)
print('App.tsx imports fixed!')
