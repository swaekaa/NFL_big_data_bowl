import os
import shutil
import glob
import re
from pathlib import Path

ROOT_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027")
SRC_TEX = ROOT_DIR / "texture"
DEST_TEX = ROOT_DIR / "frontend/public/textures"
CSS_FILE = ROOT_DIR / "frontend/src/index.css"
COMPONENTS_DIR = ROOT_DIR / "frontend/src/components"

def main():
    # 1. Create the correct folder in the frontend
    DEST_TEX.mkdir(parents=True, exist_ok=True)
    images = sorted(glob.glob(str(SRC_TEX / "*.jpg")))
    
    if not images:
        print("No .jpg images found in the 'texture' folder!")
        return

    css_classes = "\n/* Auto-generated user textures */\n"
    img_names = []
    
    for i, img_path in enumerate(images):
        name = os.path.basename(img_path)
        shutil.copy(img_path, DEST_TEX / name)
        
        # 2. Generate the CSS to apply and rotate the images
        css_classes += f"""
.texture-{i}::before {{
  background-image: url('/textures/{name}');
  background-size: cover;
  mix-blend-mode: overlay;
  opacity: 0.15;
}}
"""
        img_names.append(f"texture-{i}")

    # Append to index.css
    with open(CSS_FILE, "a", encoding="utf-8") as f:
        f.write(css_classes)

    # 3. Apply sequentially to all slides
    components = sorted(COMPONENTS_DIR.glob("*.tsx"))
    idx = 0
    for comp_path in components:
        with open(comp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace any existing texture class with the new ones
        if 'className="texture-base ' in content:
            new_class = f'texture-base {img_names[idx % len(img_names)]}'
            content = re.sub(r'texture-base texture-[a-zA-Z0-9_-]+', new_class, content)
            idx += 1
            
            with open(comp_path, "w", encoding="utf-8") as f:
                f.write(content)

    print(f"Successfully moved {len(img_names)} textures, rotated them 90 degrees, and applied them sequentially to the slides!")

if __name__ == "__main__":
    main()
