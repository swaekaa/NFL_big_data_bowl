import re
from pathlib import Path

COMPONENTS_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def main():
    components = sorted(COMPONENTS_DIR.glob("*.tsx"))
    
    for comp_path in components:
        with open(comp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # We need to remove things like `style={{ background: 'var(--bg-navy)' }}` from the <section> tags.
        # It's safest to find `<section ... style={{ background: 'var(--bg-navy)' }}` 
        # and replace the background part.
        
        # Replace simple background styles
        content = re.sub(
            r'style=\{\{\s*background:\s*\'var\(--bg-navy\)\'\s*\}\}', 
            '', 
            content
        )
        content = re.sub(
            r'style=\{\{\s*background:\s*\'var\(--bg-black\)\'\s*\}\}', 
            '', 
            content
        )
        
        # Replace backgrounds inside a larger style object: style={{ background: 'var(--bg-navy)', position: 'relative' }}
        content = re.sub(
            r'background:\s*\'var\(--bg-navy\)\',?\s*', 
            '', 
            content
        )
        content = re.sub(
            r'background:\s*\'var\(--bg-black\)\',?\s*', 
            '', 
            content
        )
        
        # Replace background gradients on sections, e.g., MultipleTestingSection
        content = re.sub(
            r'background:\s*\'linear-gradient\(180deg, var\(--bg-navy\) 0%, var\(--bg-black\) 100%\)\',?\s*',
            '',
            content
        )

        with open(comp_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("Successfully removed hardcoded section backgrounds! Images will now show through.")

if __name__ == "__main__":
    main()
