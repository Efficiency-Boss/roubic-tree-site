"""QA7 #19: give each location-hub / LSP story-img a distinct, context-relevant
work photo (root-absolute inline background) instead of the single shared
pepper-pike photo. Caption removal is handled in client_custom.css."""
import json, glob, os, re

IMGDIR = "public/images"
have = {os.path.basename(p)[:-5] for p in glob.glob(IMGDIR + "/*.webp")}  # strip .webp


def img(name):
    n = "roubic-" + name + "-hero"
    assert n in have, n
    return "/images/" + n + ".webp"


# generic work photos rotated across location hubs (distinct per city)
HUB_POOL = [img(x) for x in [
    "large-tree-removal", "dangerous-dead-tree-removal", "fallen-tree-removal",
    "land-clearing", "stump-grinding", "tree-trimming-pruning", "oak-tree-care",
    "commercial-tree-removal", "emergency-tree-removal", "residential-tree-removal",
    "ash-tree-disease-management",
]]

# service -> candidate photos (rotated by city index for per-city variation)
SVC = {
    "tree-removal": ["large-tree-removal", "dangerous-dead-tree-removal",
                     "fallen-tree-removal", "residential-tree-removal",
                     "commercial-tree-removal"],
    "tree-trimming-pruning": ["tree-trimming-pruning", "oak-tree-care"],
    "stump-grinding": ["stump-grinding"],
    "land-clearing": ["land-clearing"],
    "storm-damage-emergency": ["storm-damage-emergency", "fallen-tree-removal",
                               "emergency-tree-removal"],
    "firewood-delivery": ["firewood-delivery", "seasoned-firewood"],
}
SVC = {k: [img(x) for x in v] for k, v in SVC.items()}

DIV_RE = re.compile(r'(<div\b[^>]*?class=\\?"story-img\\?"[^>]*?)(\s*/?>)')


def set_bg(html, url):
    """inject/replace an inline background-image on the story-img div"""
    def repl(m):
        head, close = m.group(1), m.group(2)
        head = re.sub(r'\s*style=\\?"[^"]*\\?"', "", head)  # drop any prior style
        return f'{head} style=\\"background-image:url(\'{url}\')\\"{close}'
    new, n = DIV_RE.subn(repl, html)
    return new, n


def apply(path, url):
    d = json.load(open(path, encoding="utf-8"))
    total = 0
    for b in d.get("blocks", []):
        h = b.get("html")
        if isinstance(h, str) and "story-img" in h:
            nh, n = set_bg(h, url)
            if n:
                b["html"] = nh
                total += n
    if total:
        json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return total

# --- location hubs ---
hubs = sorted(p for p in glob.glob("src/content/locations/*.json")
              if "service-areas" not in p)
hcount = 0
for i, p in enumerate(hubs):
    hcount += apply(p, HUB_POOL[i % len(HUB_POOL)])

# --- LSP pages: src/content/pages/{city}__{service}.json ---
lsps = sorted(glob.glob("src/content/pages/*__*.json"))
# group by service to rotate candidates per city
by_svc = {}
for p in lsps:
    base = os.path.basename(p)[:-5]
    svc = base.split("__", 1)[1]
    by_svc.setdefault(svc, []).append(p)
lcount = 0
for svc, paths in by_svc.items():
    cands = SVC.get(svc)
    if not cands:
        continue
    for i, p in enumerate(sorted(paths)):
        lcount += apply(p, cands[i % len(cands)])

print(f"story-img backgrounds set: {hcount} hub divs, {lcount} lsp divs")
