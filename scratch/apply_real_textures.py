import re
from pathlib import Path

FRONTEND_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def apply_real_textures():
    textures = [
        "texture-wood",
        "texture-fish",
        "texture-waves",
        "texture-houndstooth"
    ]
    
    idx = 0
    
    for filepath in sorted(FRONTEND_DIR.glob("*.tsx")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Find any existing texture class and replace it
        if 'className="texture-base ' in content:
            # We already assigned classes like 'texture-base texture-noise' etc.
            # We'll replace it with 'texture-base texture-wood' etc.
            new_class = f'texture-base {textures[idx]}'
            content = re.sub(r'texture-base texture-\w+', new_class, content)
            idx = (idx + 1) % len(textures)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

    print("Successfully mapped real image textures to slides!")

if __name__ == "__main__":
    apply_real_textures()
