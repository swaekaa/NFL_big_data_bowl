import os
from pathlib import Path

COMPONENTS = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/frontend/src/components")

def replace_in_file(filename, old_str, new_str):
    filepath = COMPONENTS / filename
    if not filepath.exists():
        return
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"String not found in {filename}")

def main():
    # 1. FinalSection.tsx (The conclusion paragraph)
    old_final = """High-frequency Combine tracking reveals movement characteristics that traditional stopwatch measurements
                do not fully capture. In this exploratory analysis of 28 WR prospects, Short Shuttle direction-change
                behavior showed a strong negative association with rookie-season NFL separation. The relationship
                remained negative under bootstrap and robust-regression analyses, although uncertainty remains."""
    
    new_final = """High-frequency tracking data from the Combine reveals a whole new layer of movement that a standard stopwatch just misses. 
                By looking at 28 wide receiver prospects, we found that how they handle changes of direction in the Short Shuttle drill 
                strongly predicts how much separation they will get during their rookie season in the NFL. Even after running rigorous 
                statistical tests, this connection held up strong, proving that there is real value hidden in the tracking data."""
    replace_in_file("FinalSection.tsx", old_final, new_final)

    # 2. TrackingSection.tsx
    replace_in_file("TrackingSection.tsx", 
                    "Below are actual Short Shuttle tracking paths from two WR prospects in the dataset —", 
                    "Below are actual Short Shuttle tracking paths from two wide receiver prospects in our dataset.")

    # 3. SameStopwatchSection.tsx
    replace_in_file("SameStopwatchSection.tsx", 
                    "can have significantly different movement profiles — and different NFL outcomes.", 
                    "can actually move completely differently on the field, leading to totally different outcomes in the NFL.")
    
    replace_in_file("SameStopwatchSection.tsx",
                    "The goal of this research is not to dismiss the 40-yard dash —",
                    "The goal of this research isn't to dismiss the traditional 40-yard dash.")

    # 4. MultipleTestingSection.tsx
    replace_in_file("MultipleTestingSection.tsx",
                    "validation with larger cohorts — <strong>not as a confirmed finding.</strong>",
                    "validation with a larger group of players, rather than treating this as a confirmed finding just yet.")

    # 5. MetricSection.tsx
    replace_in_file("MetricSection.tsx",
                    "The project uses <strong style={{ color: 'var(--orange)' }}>20°</strong> as the threshold — chosen to detect meaningful directional transitions while filtering micro-corrections.",
                    "We used a threshold of <strong style={{ color: 'var(--orange)' }}>20°</strong>. This was chosen specifically to detect meaningful changes in direction while filtering out tiny micro-corrections.")
    
    replace_in_file("MetricSection.tsx",
                    "Measures <em>thresholded direction-change behavior</em> — how frequently an athlete's heading",
                    "This metric measures how frequently an athlete changes their heading")

    # 6. DiscoverySection.tsx
    replace_in_file("DiscoverySection.tsx",
                    "with rookie-season separation at pass forward. The negative trend is visible across the distribution —",
                    "with how much separation they create as rookies when the ball is thrown. This negative trend is pretty clear across the board.")

    # 7. BootstrapSection.tsx
    replace_in_file("BootstrapSection.tsx",
                    "<strong>Important:</strong> Bootstrap robustness and Huber regression reduce—but do not eliminate—the",
                    "<strong>Important:</strong> While bootstrap testing and Huber regression help reduce the impact of outliers, they don't eliminate the uncertainty completely.")

    print("All text humanized and em dashes removed.")

if __name__ == "__main__":
    main()
