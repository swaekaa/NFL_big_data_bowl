import os
import re
from pathlib import Path

# Paths
FRONTEND_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def fix_colors():
    for filepath in FRONTEND_DIR.glob("*.tsx"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace light colors with dark equivalents for the white theme
        # rgba(245,245,247,X) -> rgba(0,0,0,X)
        content = re.sub(r'rgba\(245,\s*245,\s*247,\s*([0-9.]+)\)', r'rgba(43,45,66,\1)', content)
        
        # rgba(255,255,255,X) -> rgba(0,0,0,X)
        content = re.sub(r'rgba\(255,\s*255,\s*255,\s*([0-9.]+)\)', r'rgba(0,0,0,\1)', content)

        # var(--white) inline styles should also just use var(--white) (which is now dark)
        # But just in case any "color: 'white'" is hardcoded:
        content = content.replace("color: 'white'", "color: 'var(--white)'")
        content = content.replace('color: "white"', 'color: "var(--white)"')

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("Successfully updated all component colors for the light theme!")

if __name__ == "__main__":
    fix_colors()
