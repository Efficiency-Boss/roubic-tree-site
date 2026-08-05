"""Full price inventory: dump every price token across service + resource pages,
tagged by WHERE it lives (title / desc / hero-badge / table-row / prose), so we
can design exact replacements and verify afterward."""
import json, glob, re, os
from collections import defaultdict

SVC = ["tree-removal", "tree-trimming-pruning", "stump-grinding",
       "land-clearing", "storm-damage-emergency", "firewood-delivery"]
MONEY = re.compile(r"\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?(?:\s*/\s*\w+)?|"
                   r"[+~]?\d{1,3}(?:\s*[–—-]\s*\d{1,3})?\s*%")


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s
    return None


def kind(f):
    b = os.path.basename(f)
    if b.startswith("services__") and b.count("__") == 1:
        return "HUB"
    if b.startswith("services__") and b.count("__") == 2:
        return "SPOKE"
    return "LSP"


rows = []
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    s = svc_of(f)
    if not s:
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    base = os.path.basename(f)[:-5]
    k = kind(f)
    seo = d.get("seo") or {}
    for loc, txt in (("title", seo.get("title", "")), ("desc", seo.get("description", ""))):
        for m in MONEY.findall(txt):
            rows.append((s, k, base, loc, m.strip()))
    for bi, b in enumerate(d.get("blocks", [])):
        h = b.get("html", "")
        if not isinstance(h, str):
            continue
        # table scenario -> price rows
        for sc, pr in re.findall(r'class="scenario">([^<]+)<.*?class="price[^"]*">([^<]*\$[^<]*)<', h, re.S):
            rows.append((s, k, base, f"table:{sc.strip()[:30]}", pr.strip()))
        # generic td price cells in a pricing table
        for pr in re.findall(r"<td[^>]*>([^<]*\$[\d][^<]*)</td>", h):
            rows.append((s, k, base, f"td/b{bi}", pr.strip()))
        # hero badge
        if bi == 0:
            for pr in re.findall(r'class="[^"]*price[^"]*"[^>]*>([^<]*\$[^<]+)<', h):
                rows.append((s, k, base, "HERO-badge", pr.strip()))

# summarize
print(f"TOTAL price tokens: {len(rows)}\n")
for s in SVC:
    sub = [r for r in rows if r[0] == s]
    print(f"===== {s}  ({len(sub)} tokens) =====")
    byloc = defaultdict(lambda: defaultdict(int))
    for _, k, base, loc, val in sub:
        key = loc.split(":")[0] if loc.startswith("table") else loc.split("/")[0]
        byloc[key][val] += 1
    for loc in sorted(byloc):
        vals = byloc[loc]
        print(f"  [{loc}] {len(vals)} distinct:")
        for v, c in sorted(vals.items(), key=lambda x: -x[1])[:12]:
            print(f"       {c:3}x  {v}")
    print()
