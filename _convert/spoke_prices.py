import json, glob, re, os
from collections import defaultdict

SVC = ["tree-removal", "tree-trimming-pruning", "stump-grinding",
       "storm-damage-emergency", "firewood-delivery", "land-clearing"]


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s
    return None


def kind(f):
    b = os.path.basename(f)
    return ("HUB" if b.count("__") == 1 else "SPOKE") if b.startswith("services__") else "LSP"


MONEY = re.compile(r"\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?(?:\s*(?:/|per)\s*\w+)?"
                   r"|[+~]?\d{1,3}(?:\s*[–—-]\s*\d{1,3})?\s*%")

# which service + kind to inspect from argv
import sys
want_kind = sys.argv[1] if len(sys.argv) > 1 else "SPOKE"
want_svcs = sys.argv[2].split(",") if len(sys.argv) > 2 else SVC

pat = defaultdict(lambda: defaultdict(list))
for f in glob.glob("src/content/**/*.json", recursive=True):
    s = svc_of(f)
    if not s or s not in want_svcs or kind(f) != want_kind:
        continue
    t = open(f, encoding="utf-8").read()
    base = os.path.basename(f)[:-5]
    for m in set(MONEY.findall(t)):
        pat[s][m.strip()].append(base)

for s in want_svcs:
    if not pat[s]:
        continue
    print(f"=== {s} {want_kind} — distinct price strings ===")
    for v, files in sorted(pat[s].items(), key=lambda x: -len(x[1])):
        eg = "" if len(files) > 3 else "  " + ",".join(sorted(set(files)))
        print(f"   {len(files):2}x {v}{eg}")
    print()
