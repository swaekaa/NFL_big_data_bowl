import re
from pathlib import Path

COMPONENTS_DIR = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def main():
    components = sorted(COMPONENTS_DIR.glob("*.tsx"))
    
    idx = 6 # start from 6 since 0-5 are used by the first 6 files that already have it, though we can just overwrite all of them to be safe
    
    for comp_path in components:
        with open(comp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # If it doesn't have texture-base, inject it right after the section tag!
        if 'className="texture-base' not in content:
            # Find the section tag. It looks like: <section className="section" id="ridge" ref={ref}>
            # We want to insert <div className="texture-base texture-X" /> right after it.
            
            # Using regex to find the section open tag
            def replacer(match):
                nonlocal idx
                tag = match.group(0)
                insertion = f'\n      <div className="texture-base texture-{idx % 12}" />'
                idx += 1
                return tag + insertion
            
            # Match <section ... > 
            content, count = re.subn(r'<section\b[^>]*>', replacer, content, count=1)
            
            if count > 0:
                with open(comp_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Injected texture into {comp_path.name}")
            else:
                print(f"Could not find <section> tag in {comp_path.name}")

if __name__ == "__main__":
    main()
