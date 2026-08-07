"""QA8-B: remove pricing from 9 spokes whose prices aren't in the sheet.
Hero badge + all price-table rows -> 'Quoted on-site'. Then report any residual
$ tokens (prose/FAQ) for follow-up."""
import json, re, os

SPOKES = [
    "services/services__tree-trimming-pruning__ash-tree-disease-management.json",
    "services/services__tree-trimming-pruning__cedar-tree-health-maintenance.json",
    "services/services__tree-trimming-pruning__cherry-tree-pruning.json",
    "services/services__tree-trimming-pruning__elm-tree-preservation.json",
    "services/services__tree-trimming-pruning__fruit-tree-pruning-maintenance.json",
    "services/services__tree-trimming-pruning__maple-tree-maintenance.json",
    "services/services__land-clearing__brush-clearing.json",
    "services/services__land-clearing__lot-clearing.json",
    "services/services__firewood-delivery__bulk-firewood.json",
]
ROWP = re.compile(r'(<div class=\\?"price\\?">)([^<]*)(</div>)')
PRICE_TOK = re.compile(r'\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?(?:\s*(?:/|per)\s*\w+)?|\d{1,3}\s*[–—-]\s*\d{1,3}\s*%')

base = "src/content/"
for rel in SPOKES:
    f = base + rel
    d = json.load(open(f, encoding="utf-8"))
    for bi, b in enumerate(d.get("blocks", [])):
        h = b.get("html")
        if not isinstance(h, str):
            continue
        o = h
        # price-table rows -> Quoted on-site
        if "price-row" in h:
            h = ROWP.sub(lambda m: m.group(1) + "Quoted on-site" + m.group(3), h)
        # hero badge (b0) price token -> Quoted on-site
        if bi == 0 and ("hero" in h or "page-hero" in h):
            h = PRICE_TOK.sub("Quoted on-site", h, count=1)
        if h != o:
            b["html"] = h
    json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("de-priced 9 spokes (hero + tables). Residual $ tokens per file:")
for rel in SPOKES:
    t = open(base + rel, encoding="utf-8").read()
    toks = PRICE_TOK.findall(t)
    print(f"  {os.path.basename(rel)[:-5]:52} {len(toks)} left: {sorted(set(toks))[:6]}")
