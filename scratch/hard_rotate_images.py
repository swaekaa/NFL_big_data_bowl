import os
import sys
import subprocess
from pathlib import Path

def install_pillow_and_rotate():
    # Ensure Pillow is installed
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image

    TEXTURES_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/public/textures")
    
    if not TEXTURES_DIR.exists():
        print(f"Directory not found: {TEXTURES_DIR}")
        return

    images = list(TEXTURES_DIR.glob("*.jpg"))
    if not images:
        print("No .jpg images found in the textures folder!")
        return

    print(f"Found {len(images)} images. Rotating them to landscape permanently...")
    for img_path in images:
        try:
            with Image.open(img_path) as img:
                # Rotate 90 degrees to make portrait images landscape
                # expand=True ensures the image dimensions are swapped (width becomes height)
                rotated = img.rotate(90, expand=True)
                rotated.save(img_path)
            print(f"Rotated {img_path.name}")
        except Exception as e:
            print(f"Error rotating {img_path.name}: {e}")

    # Now, let's fix the CSS so it doesn't use the CSS rotation hack anymore!
    CSS_FILE = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/index.css")
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    # Remove the CSS rotation hack completely
    hack_to_remove = """.texture-base::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  /* Use a tighter bounding box to prevent excessive zooming */
  width: 120vmax; height: 120vmax;
  transform: translate(-50%, -50%) rotate(90deg);
  background-position: center;
}"""
    
    if hack_to_remove in css:
        css = css.replace(hack_to_remove, "")
        
    # Also change the classes to apply the background directly to the div, not ::before
    css = css.replace("::before {", " {")

    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(css)

    print("Successfully rotated all images on disk and cleaned up the CSS!")

if __name__ == "__main__":
    install_pillow_and_rotate()
