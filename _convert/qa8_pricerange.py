import glob, re, os
from collections import defaultdict
d = defaultdict(list)
for f in glob.glob("src/content/**/*.json", recursive=True):
    t = open(f, encoding="utf-8").read()
    for m in re.finditer(r'priceRange\\?"\s*:\s*\\?"([^"\\]+)', t):
        d[m.group(1).strip()].append(os.path.basename(f)[:-5])
for v, files in sorted(d.items(), key=lambda x: -len(x[1])):
    print(f"{len(files):3}  {v:24}  e.g. {files[0]}")
