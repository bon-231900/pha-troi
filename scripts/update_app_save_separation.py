# -*- coding: utf-8 -*-
import sys

def main():
    with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add getInitialSaveString helper before export default function App()
    helper = """function getInitialSaveString(): string | null {
  try {
    const storedProfileStr = safeStorage.getItem('phatroi_google_profile');
    if (storedProfileStr) {
      const prof = JSON.parse(storedProfileStr);
      if (prof?.googleId) {
        const accSave = safeStorage.getItem(`phatroi_account_${prof.googleId}`);
        if (accSave && accSave.length > 50 && accSave !== '{}') {
          return accSave;
        }
        return null;
      }
    }
    return safeStorage.getItem('phatroi_guest_save') || safeStorage.getItem('phatroi_save_v6');
  } catch {
    return null;
  }
}

export default function App() {"""

    content = content.replace("export default function App() {", helper)

    # 2. Replace the 16 state initializations:
    target_str = "const s = safeStorage.getItem('phatroi_save_v6');"
    repl_str = "const s = getInitialSaveString();"
    occurrences = content.count(target_str)
    print(f"Found {occurrences} occurrences of target string.")
    content = content.replace(target_str, repl_str)

    with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Step 1 done: Replaced state initializers with getInitialSaveString().")

if __name__ == '__main__':
    main()
