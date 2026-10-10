import os
import re
from pathlib import Path

FRONTEND_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def fix_colors():
    for filepath in FRONTEND_DIR.glob("*.tsx"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Revert the dark text colors back to light text colors for the dark olive theme
        # rgba(43,45,66,X) -> rgba(245,245,247,X)
        content = re.sub(r'rgba\(43,\s*45,\s*66,\s*([0-9.]+)\)', r'rgba(245,245,247,\1)', content)
        
        # rgba(0,0,0,X) -> rgba(255,255,255,X)
        content = re.sub(r'rgba\(0,\s*0,\s*0,\s*([0-9.]+)\)', r'rgba(255,255,255,\1)', content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("Successfully updated all component colors for the dark olive theme!")

if __name__ == "__main__":
    fix_colors()
