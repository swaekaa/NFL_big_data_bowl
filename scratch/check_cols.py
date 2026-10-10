import pandas as pd
from pathlib import Path
p = Path("c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/data/processed/combine_features.parquet")
df = pd.read_parquet(p)
print([c for c in df.columns if "direction" in c.lower()])
print([c for c in df.columns if "change" in c.lower()])
