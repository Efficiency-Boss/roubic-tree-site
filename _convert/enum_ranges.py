import glob, re, os
from collections import Counter
SVC = ["tree-removal", "land-clearing", "storm-damage-emergency",
       "tree-trimming-pruning", "stump-grinding", "firewood-delivery"]


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s


RANGE = re.compile(r"\$[\d,]+\s*[–—-]\s*\$?[\d,]+\+?")
c = {s: Counter() for s in SVC}
for f in glob.glob("src/content/**/*.json", recursive=True):
    s = svc_of(f)
    if not s:
        continue
    t = open(f, encoding="utf-8").read()
    for m in RANGE.findall(t):
        c[s][re.sub(r"\s+", "", m)] += 1
import sys
for s in (sys.argv[1:] or SVC):
    print(f"=== {s} ===")
    for v, n in sorted(c[s].items(), key=lambda x: -x[1]):
        print(f"  {n:3} {v}")
