"""Pricing propagation PASS 1 — the unambiguous, exact-sheet parts only:
  * tree-removal  : hub table + all LSP tables + headline (title/meta/hero)
  * tree-trimming : hub table + all LSP tables + headline
  * land-clearing : hub table ("+" on top tier) + headline
Spokes (premium/per-sub-service pricing) and storm/firewood/stump (structural
mismatches vs sheet) are DELIBERATELY skipped — they need a human decision.
Nothing here invents a number; every value comes from Roubic_Pricing_Intake.xlsx.
"""
import json, glob, re, os

HEADLINE = {
    "tree-removal": "$400–$5,000+",
    "tree-trimming-pruning": "$150–$2,500+",
    "land-clearing": "$1,500–$20,000+",
}
# old headline-range strings that must collapse to the canonical headline
OLD_HEADLINES = {
    "tree-removal": ["$300–$7,000+", "$3,500–$15,000", "$400–$1,500", "$400–$5,000+"],
    "tree-trimming-pruning": ["$300–$7,000+"],
    "land-clearing": ["$1,500–$15,000"],
}
# LSP price-table: 4 price cells in row order (Small/Medium/Large/X-Large)
LSP_TIERS = {
    "tree-removal": ["$400–$700", "$700–$1,400", "$1,200–$2,200", "$2,000–$5,000+"],
    "tree-trimming-pruning": ["$150–$350", "$350–$800", "$800–$1,800", "$1,800–$2,500+"],
}
# hub table: exact old->new cell edits
HUB_CELLS = {
    "tree-removal": [("$400–$800", "$400–$700"), ("$650–$950", "$700–$1,400"),
                     ("$850–$2,000", "$1,200–$2,200")],
    "tree-trimming-pruning": [("$175–$400", "$150–$350"), ("$400–$900", "$350–$800"),
                              ("$900–$2,500", "$800–$2,500+"), ("10–15% off", "15–20% off")],
    "land-clearing": [("$5,000–$20,000 / acre", "$5,000–$20,000+ / acre")],
}
SVC = list(HEADLINE)


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s
    return None


def kind(f):
    b = os.path.basename(f)
    if b.startswith("services__"):
        return "HUB" if b.count("__") == 1 else "SPOKE"
    return "LSP"


def norm_dashes(s):
    return s.replace("—", "–").replace(" – ", "–").replace(" –", "–").replace("– ", "–")


log = []
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    s = svc_of(f)
    if not s:
        continue
    k = kind(f)
    if k == "SPOKE":
        continue  # held for decision
    d = json.load(open(f, encoding="utf-8"))
    base = os.path.basename(f)[:-5]
    changed = False

    # ---- headline in title + meta ----
    seo = d.get("seo") or {}
    for key in ("title", "description"):
        if key in seo and isinstance(seo[key], str):
            t = seo[key]
            for old in OLD_HEADLINES[s]:
                for variant in (old, old.replace("–", "-"), old.replace("–", "—")):
                    if variant in t and HEADLINE[s] not in variant:
                        t = t.replace(variant, HEADLINE[s])
            if t != seo[key]:
                seo[key] = t
                changed = True
    d["seo"] = seo

    # ---- blocks ----
    for bi, b in enumerate(d.get("blocks", [])):
        h = b.get("html")
        if not isinstance(h, str):
            continue
        orig = h
        # hero badge headline (block 0)
        if bi == 0:
            for old in OLD_HEADLINES[s]:
                for variant in (old, old.replace("–", "-"), old.replace("–", "—")):
                    h = h.replace(variant, HEADLINE[s])
        # hub table cells
        if k == "HUB":
            for old, new in HUB_CELLS[s]:
                for variant in (old, old.replace("–", "-"), old.replace("–", "—")):
                    h = h.replace(variant, new)
        # LSP positional table
        if k == "LSP" and s in LSP_TIERS and "price-row" in h and 'class="price"' in h:
            cells = re.findall(r'(<div class="price">)([^<]+)(</div>)', h)
            if len(cells) == 4:
                tiers = LSP_TIERS[s]
                idx = [0]
                def repl(m):
                    i = idx[0]; idx[0] += 1
                    return f'{m.group(1)}{tiers[i]}{m.group(3)}'
                h = re.sub(r'(<div class="price">)([^<]+)(</div>)', repl, h)
            else:
                log.append(f"SKIP-LSP-TABLE {base}: {len(cells)} price cells (expected 4)")
        if h != orig:
            b["html"] = h
            changed = True

    if changed:
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        log.append(f"OK {k:5} {s:22} {base}")

for l in log:
    print(l)
print(f"\nfiles changed: {sum(1 for l in log if l.startswith('OK'))}")
