import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    try:
        from PIL import Image
    except ImportError:
        print("Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image

    ROOT_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027")
    SRC_DIR = ROOT_DIR / "texture"
    DEST_DIR = ROOT_DIR / "frontend/public/textures"
    
    if not SRC_DIR.exists():
        print(f"Error: {SRC_DIR} not found.")
        return

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    print("Copying new textures and rotating them to landscape...")
    count = 0
    for file_path in SRC_DIR.iterdir():
        if file_path.is_file():
            # If the file has no extension (like '10'), assume it's a jpg
            dest_name = file_path.name
            if "." not in dest_name:
                dest_name += ".jpg"
            
            dest_path = DEST_DIR / dest_name
            
            # Copy to public folder
            shutil.copy(file_path, dest_path)
            
            # Rotate it to landscape permanently
            try:
                with Image.open(dest_path) as img:
                    rotated = img.rotate(90, expand=True)
                    rotated.save(dest_path)
                print(f"Updated and rotated: {dest_name}")
                count += 1
            except Exception as e:
                print(f"Error processing {dest_name}: {e}")

    print(f"\nSuccess! {count} new textures have been applied and rotated.")

if __name__ == "__main__":
    main()
