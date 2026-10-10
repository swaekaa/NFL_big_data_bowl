import re
from pathlib import Path

FRONTEND_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def revert_palette():
    for filepath in FRONTEND_DIR.glob("*.tsx"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Revert HARVEST (173,136,32) -> Old Red (255,45,85)
        content = re.sub(r'173,\s*136,\s*32', '255,45,85', content)
        content = content.replace('#ad8820', '#ff2d55')
        
        # Revert MIST (182,187,217) -> Old Cyan (0,212,255)
        content = re.sub(r'182,\s*187,\s*217', '0,212,255', content)
        content = content.replace('#b6bbd9', '#00d4ff')

        # Revert TERRAIN (144,132,74) -> Old Orange (255,107,0)
        content = re.sub(r'144,\s*132,\s*74', '255,107,0', content)
        content = content.replace('#90844a', '#ff6b00')

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("Successfully reverted plot colors to original neon!")

if __name__ == "__main__":
    revert_palette()
