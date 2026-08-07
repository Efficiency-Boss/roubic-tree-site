"""Strip the 9 de-price spokes' OWN price ranges from prose/FAQ, replacing with
'quoted on-site'. Excludes the sibling cross-sell chip headlines ($400-$5,000+,
$150-$800, $1,500-$20,000+, $500-$8,000+, $180-$450) which must stay."""
import json, re, os

KEEP = {"$400–$5,000+", "$150–$800", "$1,500–$20,000+/acre", "$500–$8,000+", "$180–$450"}
# per-file signature ranges/percbrands to neutralise
SIG = {
    "ash-tree-disease-management": ["$192–$360 per cycle", "$192–$360", "$8–$15 per inch", "$8–$15", "25–30%"],
    "cedar-tree-health-maintenance": ["$200–$600 per tree", "$200–$600/Tree", "$200–$600"],
    "cherry-tree-pruning": ["$200–$600 per tree", "$200–$600"],
    "elm-tree-preservation": ["$10–$20 per inch", "$10–$20", "$400–$1,500 per visit", "$400–$1,500"],
    "fruit-tree-pruning-maintenance": ["$375–$500 per tree", "$375–$500/Tree", "$375–$500"],
    "maple-tree-maintenance": ["$300–$1,200 per tree", "$300–$1,200/Tree", "$300–$1,200",
                                "$300–$550", "$550–$900", "$900–$1,200"],
    "brush-clearing": ["$500–$5,000"],
    "lot-clearing": ["$25,000+", "$25,000"],
    "bulk-firewood": ["$40–$80 per cord", "$40–$80"],
}
DIRS = {"ash-tree-disease-management": "services/services__tree-trimming-pruning__",
        "cedar-tree-health-maintenance": "services/services__tree-trimming-pruning__",
        "cherry-tree-pruning": "services/services__tree-trimming-pruning__",
        "elm-tree-preservation": "services/services__tree-trimming-pruning__",
        "fruit-tree-pruning-maintenance": "services/services__tree-trimming-pruning__",
        "maple-tree-maintenance": "services/services__tree-trimming-pruning__",
        "brush-clearing": "services/services__land-clearing__",
        "lot-clearing": "services/services__land-clearing__",
        "bulk-firewood": "services/services__firewood-delivery__"}


def variants(s):
    return [s, s.replace("–", " – "), s.replace("–", "-"), s.replace("–", "—")]


for key, sigs in SIG.items():
    f = "src/content/" + DIRS[key] + key + ".json"
    t = open(f, encoding="utf-8").read()
    # longest first to avoid partial overlaps
    for s in sorted(sigs, key=len, reverse=True):
        if s in KEEP:
            continue
        for v in variants(s):
            t = t.replace(v, "quoted on-site")
    open(f, "w", encoding="utf-8").write(t)
print("prose/FAQ de-priced on 9 spokes")
