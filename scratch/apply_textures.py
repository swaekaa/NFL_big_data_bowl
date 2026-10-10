import re
from pathlib import Path
import random

FRONTEND_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def apply_textures():
    textures = [
        "texture-base texture-noise",
        "texture-base texture-wood",
        "texture-base texture-cardboard",
        "texture-base texture-notebook"
    ]
    
    # We want to predictably cycle through them
    idx = 0
    
    for filepath in sorted(FRONTEND_DIR.glob("*.tsx")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if 'className="grid-bg"' in content:
            # Replace grid-bg with one of the new texture classes
            content = content.replace('className="grid-bg"', f'className="{textures[idx]}"')
            idx = (idx + 1) % len(textures)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

    print("Successfully applied diverse textures to all slides!")

if __name__ == "__main__":
    apply_textures()
