import re
from pathlib import Path

COMPONENTS_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")
CSS_FILE = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/index.css")

def main():
    # 1. Remove inline opacity styles from all components
    components = sorted(COMPONENTS_DIR.glob("*.tsx"))
    for comp_path in components:
        with open(comp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove things like `style={{ opacity: 0.3 }}` from the texture-base div
        # Regex to find: className="texture-base texture-X" style={{ opacity: Y }}
        content = re.sub(
            r'(className="texture-base texture-\d+")\s*style=\{\{\s*opacity:\s*0\.\d+\s*\}\}', 
            r'\1', 
            content
        )

        with open(comp_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 2. Fix the zoom level in index.css
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()
    
    # Replace the 200% zoom with 120vh/120vw for a much tighter fit that doesn't zoom in crazy amounts
    # Actually, let's use 100vh and 100vw but anchored
    old_css = """.texture-base::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  transform: rotate(90deg);
  background-position: center;
}"""

    new_css = """.texture-base::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  /* Use a tighter bounding box to prevent excessive zooming */
  width: 120vmax; height: 120vmax;
  transform: translate(-50%, -50%) rotate(90deg);
  background-position: center;
}"""
    
    css = css.replace(old_css, new_css)
    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(css)

    print("Fixed opacity across all slides and reduced the zoom level on the backgrounds!")

if __name__ == "__main__":
    main()
