"""QA8-D: set each location-hub .cs-card price line to canonical (Ammar strings).
Operates on parsed block HTML (regular quotes)."""
import json, glob, os, re

TXT = {
    "tree-removal": "$400–$5,000+",
    "tree-trimming-pruning": "$250–$2,500+",
    "stump-grinding": "$275 min",
    "land-clearing": "$1,500–$20,000+/acre",
    "storm-damage-emergency": "$500–$8,000+ by scope",
    "firewood-delivery": "$180–$450 per cord",
}
CARD = re.compile(
    r'(<a class="cs-card" href="/[a-z0-9-]+/([a-z-]+)/">.*?<p[^>]*>)([^<]*)(</p>\s*<span)',
    re.S)

n = files = 0
for f in sorted(glob.glob("src/content/locations/*.json")):
    if os.path.basename(f) == "service-areas.json":
        continue
    d = json.load(open(f, encoding="utf-8"))
    changed = False
    for b in d.get("blocks", []):
        h = b.get("html")
        if not isinstance(h, str) or "cs-card" not in h:
            continue

        def repl(m):
            global n
            svc = m.group(2)
            if svc in TXT:
                n += 1
                return m.group(1) + TXT[svc] + m.group(4)
            return m.group(0)
        nh = CARD.sub(repl, h)
        if nh != h:
            b["html"] = nh
            changed = True
    if changed:
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        files += 1

print(f"cs-card prices set: {n} across {files} location hubs")
