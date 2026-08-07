"""QA8 Batch A — trimming hero/headline + multi-tree %, storm/firewood hero,
stump per-inch removal. Surgical, scoped by file + surface."""
import json, glob, re, os

PRICE = re.compile(r"\$[\d,]+\s*[–—-]\s*\$?[\d,]+\+?")


def is_trim_hub_or_lsp(f):
    b = os.path.basename(f)
    return (b == "services__tree-trimming-pruning.json"
            or b.endswith("__tree-trimming-pruning.json") and "__tree-trimming-pruning__" not in b
            and b.startswith(("services__")) is False)  # LSP form city__trim


def trim_target(f):
    b = os.path.basename(f)
    if b == "services__tree-trimming-pruning.json":
        return True                                   # hub
    if b.endswith("__tree-trimming-pruning.json") and not b.startswith("services__"):
        return True                                   # LSP city page
    return False


stats = {"trim_hero": 0, "trim_meta": 0, "multi_pct": 0, "storm_hero": 0,
         "fw_hero": 0, "stump_perinch": 0, "files": 0}

for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    b = os.path.basename(f)
    txt = open(f, encoding="utf-8").read()
    d = json.loads(txt)
    changed = False

    # ---- TRIMMING hub + LSP: hero badge (b0) + meta headline -> $250-$2,500+ ----
    if trim_target(f):
        seo = d.get("seo") or {}
        for k in ("title", "description"):
            if isinstance(seo.get(k), str):
                new = PRICE.sub("$250–$2,500+", seo[k], count=1) if PRICE.search(seo[k]) else seo[k]
                # only replace the first (headline) range
                if new != seo[k]:
                    seo[k] = new; stats["trim_meta"] += 1; changed = True
        d["seo"] = seo
        if d.get("blocks"):
            h0 = d["blocks"][0].get("html", "")
            n0 = PRICE.subn("$250–$2,500+", h0)
            if n0[1]:
                d["blocks"][0]["html"] = n0[0]; stats["trim_hero"] += n0[1]; changed = True

    # ---- multi-tree maintenance %: 10-15% -> 15-20% (trimming files only) ----
    if "tree-trimming-pruning" in b:
        for old in ("10–15%", "10-15%", "10—15%"):
            if old in txt and old in json.dumps(d, ensure_ascii=False):
                pass
        def fixpct(o):
            if isinstance(o, str):
                return o.replace("10–15%", "15–20%").replace("10-15%", "15–20%").replace("10—15%", "15–20%")
            if isinstance(o, dict):
                return {k: fixpct(v) for k, v in o.items()}
            if isinstance(o, list):
                return [fixpct(v) for v in o]
            return o
        nd = fixpct(d)
        if json.dumps(nd, ensure_ascii=False) != json.dumps(d, ensure_ascii=False):
            d = nd; stats["multi_pct"] += 1; changed = True

    # ---- STORM hub hero -> $500-$8,000+ ----
    if b == "services__storm-damage-emergency.json" and d.get("blocks"):
        h0 = d["blocks"][0].get("html", "")
        n = PRICE.subn("$500–$8,000+", h0)
        if n[1]:
            d["blocks"][0]["html"] = n[0]; stats["storm_hero"] += n[1]; changed = True

    # ---- FIREWOOD hub hero -> $180-$450 / cord ----
    if b == "services__firewood-delivery.json" and d.get("blocks"):
        h0 = d["blocks"][0].get("html", "")
        n = PRICE.subn("$180–$450", h0)
        if n[1]:
            d["blocks"][0]["html"] = n[0]; stats["fw_hero"] += n[1]; changed = True

    # ---- STUMP per-inch text removal (all stump files) ----
    if "stump-grinding" in b:
        def strip_perinch(o):
            if isinstance(o, str):
                s = o
                s = re.sub(r"\s*[+–—-]?\s*\$8\s*/\s*inch(?:\s+after)?", "", s)
                s = re.sub(r"\s*\$8\s*[–—-]\s*\$15\s*per\s*inch", "", s)
                s = re.sub(r"\s*\+?\s*\$8\s*per\s*inch(?:\s+after)?", "", s)
                s = re.sub(r"\s*\$275\s*min\s*\+\s*\$8/inch", "$275 min", s)
                return s
            if isinstance(o, dict):
                return {k: strip_perinch(v) for k, v in o.items()}
            if isinstance(o, list):
                return [strip_perinch(v) for v in o]
            return o
        nd = strip_perinch(d)
        if json.dumps(nd, ensure_ascii=False) != json.dumps(d, ensure_ascii=False):
            d = nd; stats["stump_perinch"] += 1; changed = True

    if changed:
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        stats["files"] += 1

print(stats)
