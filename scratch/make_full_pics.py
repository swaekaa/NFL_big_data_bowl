import re
from pathlib import Path

CSS_FILE = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/index.css")

def main():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Make images fully opaque
    content = content.replace("  mix-blend-mode: overlay;\n  opacity: 0.15;\n", "")
    content = content.replace("  mix-blend-mode: multiply;\n  opacity: 0.35;\n", "")
    content = content.replace("  mix-blend-mode: soft-light;\n  opacity: 0.15;\n", "")
    content = content.replace("  mix-blend-mode: multiply;\n  opacity: 0.25;\n", "")

    # Push texture-base behind all content
    content = content.replace("z-index: 0;", "z-index: -1;")

    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully converted textures to full opaque pictures!")

if __name__ == "__main__":
    main()
