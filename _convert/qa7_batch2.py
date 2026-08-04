"""QA7 batch 2: #17 remove city-since badges, #21 fabricated years->1982,
#24/#26/#28 fix broken EAB links -> aphis /eab."""
import json, glob, os, re

EAB_GOOD = "https://www.aphis.usda.gov/plant-pests-diseases/eab"
EAB_BAD = [
    "https://www.aphis.usda.gov/plant-pests-diseases/emerald-ash-borer",
    "https://agri.ohio.gov/divisions/plant-health/invasive-pests/eab",
]

stats = {"city_since_removed": 0, "years_fixed": 0, "eab_links_fixed": 0, "files": 0}

for f in glob.glob("src/content/**/*.json", recursive=True):
    if os.path.basename(os.path.dirname(f)) == "globals":
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(d, dict) or "blocks" not in d:
        continue
    changed = False
    for b in d["blocks"]:
        h = b.get("html")
        if not isinstance(h, str):
            continue
        orig = h
        # #17 remove city-since badge spans entirely (fabricated per-city years)
        n17 = len(re.findall(r'<span class=\\?"city-since\\?">[^<]*</span>', h))
        if n17:
            h = re.sub(r'\s*<span class=\\?"city-since\\?">[^<]*</span>', "", h)
            stats["city_since_removed"] += n17
        # #21 fabricated founding/serving years -> 1982 (company/market claims only)
        for bad in ("1985", "1992"):
            for cased in ("Since " + bad, "since " + bad):
                if cased in h:
                    stats["years_fixed"] += h.count(cased)
                    h = h.replace(cased, cased[:-4] + "1982")
        # #24/#26/#28 broken EAB links
        for bad in EAB_BAD:
            if bad in h:
                stats["eab_links_fixed"] += h.count(bad)
                h = h.replace(bad, EAB_GOOD)
        if h != orig:
            b["html"] = h
            changed = True
    if changed:
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        stats["files"] += 1

print(stats)
