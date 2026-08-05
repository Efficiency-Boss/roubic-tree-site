"""Pricing audit: for each of the 6 services, collect every distinct price
token that appears (a) in the <title>, (b) in hero 'confirmed pricing' badges,
(c) in pricing-table scenario rows — across hub + spokes + LSP pages — so we can
see how badly the same service diverges page to page."""
import json, glob, re, os
from collections import defaultdict

SVC = ["tree-removal", "tree-trimming-pruning", "stump-grinding",
       "land-clearing", "storm-damage-emergency", "firewood-delivery"]

RANGE = re.compile(r"\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+\+?)?")


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s
    return None


title_ranges = defaultdict(lambda: defaultdict(list))   # svc -> range -> [files]
hero_ranges = defaultdict(lambda: defaultdict(list))
page_count = defaultdict(int)

for f in glob.glob("src/content/**/*.json", recursive=True):
    s = svc_of(f)
    if not s:
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    page_count[s] += 1
    base = os.path.basename(f)[:-5]
    # title money range
    t = (d.get("seo") or {}).get("title", "")
    for r in RANGE.findall(t):
        if "$" in r and ("–" in r or "-" in r or "—" in r):
            title_ranges[s][r.replace(" ", "")].append(base)
    # hero 'confirmed pricing' badge (first block)
    if d.get("blocks"):
        h0 = d["blocks"][0].get("html", "")
        for m in re.findall(r'class="[^"]*price[^"]*"[^>]*>([^<]*\$[^<]+)<', h0):
            for r in RANGE.findall(m):
                hero_ranges[s][r.replace(" ", "")].append(base)

for s in SVC:
    print(f"===== {s}  ({page_count[s]} pages) =====")
    print(f"  distinct <title> money-ranges: {len(title_ranges[s])}")
    for r, files in sorted(title_ranges[s].items(), key=lambda x: -len(x[1])):
        print(f"     {len(files):3}x  {r}")
    if hero_ranges[s]:
        print(f"  distinct hero-badge ranges: {len(hero_ranges[s])}")
        for r, files in sorted(hero_ranges[s].items(), key=lambda x: -len(x[1])):
            print(f"     {len(files):3}x  {r}   e.g. {files[0]}")
    print()
