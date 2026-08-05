"""Pricing propagation PASS 2 — remaining services, sheet-aligned.
Per Amer: premium spokes DROP to sheet ($2,000–$5,000+). Trimming spokes are
left as-is (legitimately per-sub-service, already within the sheet range).
Replacements are scoped to each service's own files.

Two replacement kinds:
  RANGE  — full "$a–$b" strings, plain replace (safe, not substrings of others)
  STAND  — standalone "$N"/"$N+" numbers, regex with boundaries so we never edit
           a number embedded inside a larger range (e.g. the 8,000 in $2,500–$8,000+)
"""
import json, glob, re, os

RANGE = {
    "tree-removal": [
        ("$3,500–$15,000", "$2,000–$5,000+"), ("$1,200–$8,000", "$2,000–$5,000+"),
        ("$400–$1,500", "$400–$5,000+"), ("$1,800–$4,000", "$1,200–$2,200"),
        ("$850–$1,500", "$700–$1,400"), ("$650–$950", "$700–$1,400"),
        ("$400–$800", "$400–$700"), ("$300–$600", "$400–$700"),
    ],
    "storm-damage-emergency": [
        ("+50% over scheduled rates", "+25–50% over scheduled rates"),
        ("$800–$5,000", "$2,500–$8,000+"), ("$1,500–$10,000+", "$1,500–$5,000"),
        ("$1,200–$8,000", "$2,500–$8,000+"),
    ],
    "firewood-delivery": [
        ("$175–$250", "$180–$240"), ("$250–$400", "$230–$310"), ("$400–$650", "$280–$380"),
    ],
    "stump-grinding": [
        ("$150–$200", "$150–$250"), ("$300–$500", "$400–$800"),
        ("$450–$900+", "$400–$800"), ("$200–$450", "$200–$400"),
    ],
}
STAND = {  # standalone number -> replacement (regex-guarded)
    "tree-removal": [("$8,000", "$5,000+"), ("$10,000", "$5,000+")],
    "storm-damage-emergency": [("$10,000", "$8,000+")],
}
STORM_LSP_TIERS = ["$500–$1,500", "$1,500–$5,000", "$2,500–$8,000+", "$2,500–$8,000+"]
STORM_HEADLINE = "$500–$8,000+"

SVC = ["tree-removal", "storm-damage-emergency", "firewood-delivery", "stump-grinding"]


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


def dash_variants(s):
    return [s, s.replace("–", "-"), s.replace("–", "—"),
            s.replace("–", " – "), s.replace("–", " — ")]


def apply_str(text, s):
    for old, new in RANGE.get(s, []):
        for v in dash_variants(old):
            text = text.replace(v, new)
    for old, new in STAND.get(s, []):
        num = re.escape(old)  # e.g. \$10,000
        # match standalone $N optionally followed by '+', NOT preceded by a range dash
        # or digit, and NOT part of a bigger number
        text = re.sub(rf"(?<![–—\-\d]){num}\+?(?!\d)", new, text)
    return text


def walk(o, s):
    if isinstance(o, str):
        return apply_str(o, s)
    if isinstance(o, dict):
        return {k: walk(v, s) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v, s) for v in o]
    return o


log = []
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    s = svc_of(f)
    if not s:
        continue
    k = kind(f)
    before = open(f, encoding="utf-8").read()
    d = json.loads(before)

    d = walk(d, s)

    # storm LSP structural: positional size-tier table -> severity tiers + headline
    if s == "storm-damage-emergency" and k == "LSP":
        for b in d.get("blocks", []):
            h = b.get("html")
            if isinstance(h, str) and "price-row" in h and 'class="price"' in h:
                cells = re.findall(r'(<div class="price">)([^<]+)(</div>)', h)
                if len(cells) == 4:
                    idx = [0]
                    def repl(m):
                        i = idx[0]; idx[0] += 1
                        return f'{m.group(1)}{STORM_LSP_TIERS[i]}{m.group(3)}'
                    b["html"] = re.sub(r'(<div class="price">)([^<]+)(</div>)', repl, h)
        seo = d.get("seo") or {}
        for key in ("title", "description"):
            if isinstance(seo.get(key), str):
                for v in dash_variants("$300–$7,000+"):
                    seo[key] = seo[key].replace(v, STORM_HEADLINE)
        d["seo"] = seo
        if d.get("blocks"):
            h0 = d["blocks"][0].get("html", "")
            for v in dash_variants("$300–$7,000+"):
                h0 = h0.replace(v, STORM_HEADLINE)
            d["blocks"][0]["html"] = h0

    after = json.dumps(d, ensure_ascii=False)
    if after != json.dumps(json.loads(before), ensure_ascii=False):
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        base = os.path.basename(f)[:-5]
        log.append(f"OK {k:5} {s:22} {base}")

for l in log:
    print(l)
print(f"\nfiles changed: {len(log)}")
