"""Distinct price/percent strings per service across ALL surfaces (title, desc,
jsonld, all blocks), so we can build the QA8 wrong->right map."""
import json, glob, re, os
from collections import Counter

SVC = ["tree-removal", "tree-trimming-pruning", "stump-grinding",
       "land-clearing", "storm-damage-emergency", "firewood-delivery"]
PRICE = re.compile(r"\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?(?:\s*(?:/|per)\s*\w+)?"
                   r"|[+~]?\d{1,3}\s*[–—-]\s*\d{1,3}\s*%|\$\d+\s*/\s*inch|\$\d+\s*min\b")


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s


c = {s: Counter() for s in SVC}
for f in glob.glob("src/content/**/*.json", recursive=True):
    s = svc_of(f)
    if not s:
        continue
    t = open(f, encoding="utf-8").read()
    for m in PRICE.findall(t):
        c[s][re.sub(r"\s+", "", m)] += 1

import sys
for s in (sys.argv[1:] or SVC):
    print(f"=== {s} ===")
    for v, n in sorted(c[s].items(), key=lambda x: -x[1]):
        print(f"  {n:4} {v}")
