"""QA8-C: firewood LSP cord repricing + storm LSP scenario relabel.
Cities: auburn, pepper-pike, chagrin-falls, moreland-hills, solon."""
import json, re

CITIES = ["auburn-township-oh", "pepper-pike-oh", "chagrin-falls-oh",
          "moreland-hills-oh", "solon-oh"]
ROW = re.compile(r'(<div class="scenario">)(.*?)(</div>\s*<div class="includes">.*?</div>\s*<div class="price">)([^<]*)(</div>)', re.S)


def fw_price(scen_lower, cur):
    if "full cord" in scen_lower:
        return "$280–$380"
    if "face" in scen_lower or "partial" in scen_lower:
        return "$180–$240"
    if "premium" in scen_lower or "oak" in scen_lower:
        return "$350–$450"
    return cur  # bulk / stacking -> keep (quoted)


# storm scenario relabel by row order (prices already sheet-correct, keep them)
STORM = [
    ("Storm Cleanup", "No structure damage"),
    ("Leaning / Uprooted", "Pre-failure removal"),
    ("Tree on Structure", "Roof, garage, vehicle"),
    ("Crane / After-Hours", "Structure proximity or nights"),
]

for city in CITIES:
    # --- firewood ---
    fwp = f"src/content/pages/{city}__firewood-delivery.json"
    d = json.load(open(fwp, encoding="utf-8"))
    for b in d.get("blocks", []):
        h = b.get("html")
        if isinstance(h, str) and "price-row" in h:
            b["html"] = ROW.sub(lambda m: m.group(1) + m.group(2) + m.group(3)
                                + fw_price(re.sub("<[^>]+>", " ", m.group(2)).lower(), m.group(4)) + m.group(5), h)
    json.dump(d, open(fwp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # --- storm: relabel scenario by position, keep price ---
    stp = f"src/content/pages/{city}__storm-damage-emergency.json"
    d = json.load(open(stp, encoding="utf-8"))
    for b in d.get("blocks", []):
        h = b.get("html")
        if not isinstance(h, str) or "price-row" not in h:
            continue
        idx = [0]
        def relbl(m):
            i = idx[0]; idx[0] += 1
            if i < len(STORM):
                name, sub = STORM[i]
                newscen = f'{name}<small>{sub}</small>'
                return m.group(1) + newscen + m.group(3) + m.group(4) + m.group(5)
            return m.group(0)
        h = ROW.sub(relbl, h)
        # header "Tree Size" -> "Storm Scenario"
        h = h.replace(">Tree Size<", ">Storm Scenario<")
        b["html"] = h
    json.dump(d, open(stp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("firewood repriced + storm relabeled across 5 cities")
