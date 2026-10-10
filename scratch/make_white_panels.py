import re
from pathlib import Path

COMPONENTS_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")
CSS_FILE = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/index.css")

def main():
    # 1. Update index.css to make .glass white and add drop shadows to text
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    css = css.replace(
        "  background: var(--bg-card);\n  border: 1px solid var(--border);\n",
        "  background: rgba(255, 255, 255, 0.95);\n  border: 1px solid rgba(0, 0, 0, 0.1);\n  color: #122311;\n"
    )
    
    # Let's also add a strong text shadow to normal text so it's readable over the pictures
    if "/* Global text shadow for readability */" not in css:
        css += """
/* Global text shadow for readability */
p {
  text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
  font-weight: 500;
}
.glass p {
  text-shadow: none; /* No shadow needed inside white panels */
}
"""
    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(css)

    # 2. Update all components
    for comp_path in COMPONENTS_DIR.glob("*.tsx"):
        with open(comp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Change dark inline panels to white panels
        content = re.sub(r'background:\s*\'rgba\(6,8,16,0\.9[0-9]\)\'', "background: 'rgba(255,255,255,0.95)'", content)
        content = content.replace("background: 'var(--bg-card)'", "background: 'rgba(255,255,255,0.95)'")
        
        # Change white borders to dark borders for panels
        content = re.sub(r'border:\s*\'1px solid rgba\(255,255,255,0\.[0-9]+\)\'', "border: '1px solid rgba(0,0,0,0.1)'", content)
        
        # Change white text to dark text inside panels
        content = content.replace("color: 'var(--white)'", "color: '#122311'")
        content = content.replace('color: "var(--white)"', "color: '#122311'")
        
        # Change chart grid lines to dark
        content = content.replace('stroke="rgba(255,255,255,0.04)"', 'stroke="rgba(0,0,0,0.1)"')
        content = content.replace("stroke: 'rgba(255,255,255,0.04)'", "stroke: 'rgba(0,0,0,0.1)'")
        
        # Change chart axis ticks to dark
        content = content.replace("fill: 'rgba(245,245,247,0.5)'", "fill: '#444'")
        content = content.replace("fill: 'rgba(245,245,247,0.35)'", "fill: '#666'")
        content = content.replace("fill: 'rgba(245,245,247,0.3)'", "fill: '#666'")
        
        with open(comp_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("Updated all panels to be white and rounded, and fixed text colors for readability!")

if __name__ == "__main__":
    main()
