import re
from pathlib import Path

FRONTEND_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def apply_palette():
    for filepath in FRONTEND_DIR.glob("*.tsx"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Old Red (255,45,85) -> HARVEST (173,136,32)
        content = re.sub(r'255,\s*45,\s*85', '173,136,32', content)
        content = content.replace('#ff2d55', '#ad8820')
        
        # Old Cyan (0,212,255) -> MIST (182,187,217)
        content = re.sub(r'0,\s*212,\s*255', '182,187,217', content)
        content = content.replace('#00d4ff', '#b6bbd9')

        # Old Orange (255,107,0) -> TERRAIN (144,132,74)
        content = re.sub(r'255,\s*107,\s*0', '144,132,74', content)
        content = content.replace('#ff6b00', '#90844a')
        
        # Custom separation gradient in Scatter charts:
        # High separation: 'rgba(100,200,255,0.8)' -> 'rgba(182,187,217,0.8)' (MIST)
        content = re.sub(r'100,\s*200,\s*255', '182,187,217', content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("Successfully updated hardcoded component colors to the new palette!")

if __name__ == "__main__":
    apply_palette()
