"""QA8-F stump restructure: price ONLY the 3 client services (Minimum $275,
Commercial/multi-stump $2,000+, Chip/haul $150-$500); every other row ->
'Quoted on-site'. Set each stump hero badge to '$275 min'. Applies to all stump
pages (hub, LSPs, commercial + stump-removal spokes)."""
import json, glob, re, os

ROW = re.compile(r'(<div class=\\?"scenario\\?">)(.*?)(</div>.*?<div class=\\?"price\\?">)([^<]*)(</div>)', re.S)
PRICE_TOK = re.compile(r'\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?(?:\s*min)?')


def new_price(scen_html):
    s = re.sub(r"<[^>]+>", " ", scen_html).lower()
    if "minimum" in s or re.search(r"\bmin\b", s):
        return "$275 min"
    if "commercial" in s or "multi-stump" in s or "multi stump" in s or "full-scope" in s:
        return "$2,000+"
    if "chip" in s or "haul" in s:
        return "$150–$500"
    return "Quoted on-site"


files = sorted(set(glob.glob("src/content/**/*stump*.json", recursive=True)))
n_rows = 0
n_files = 0
for f in files:
    d = json.load(open(f, encoding="utf-8"))
    changed = False
    for bi, b in enumerate(d.get("blocks", [])):
        h = b.get("html")
        if not isinstance(h, str):
            continue
        if "price-row" in h and "scenario" in h:
            def repl(m):
                global n_rows
                np = new_price(m.group(2))
                if np != m.group(4).strip():
                    n_rows += 1
                return m.group(1) + m.group(2) + m.group(3) + np + m.group(5)
            nh = ROW.sub(repl, h)
            if nh != h:
                b["html"] = nh
                changed = True
        # hero badge (block 0) -> "$275 min"
        if bi == 0 and ("hero" in h or "page-hero" in h):
            nh = PRICE_TOK.sub("$275 min", h, count=1) if PRICE_TOK.search(h) else h
            if nh != h:
                b["html"] = nh
                changed = True
    if changed:
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        n_files += 1

print(f"stump: {n_rows} row prices remapped across {n_files} files")
