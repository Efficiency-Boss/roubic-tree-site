import json, re
CITIES = ["auburn-township-oh","pepper-pike-oh","chagrin-falls-oh","moreland-hills-oh","solon-oh"]
ROW = re.compile(r'(<div class="scenario">)([^<]*)(<small>.*?</small>\s*</div>\s*<div class="includes">.*?</div>\s*<div class="price">)([^<]*)(</div>)', re.S)
def price(main, cur):
    m = main.lower()
    if "face" in m or "partial" in m: return "$180–$240"
    if "premium" in m or "specialty" in m or "oak" in m: return "$350–$450"
    if "full cord" in m: return "$280–$380"
    return cur  # bulk/seasonal/stacking -> keep
for city in CITIES:
    p = f"src/content/pages/{city}__firewood-delivery.json"
    d = json.load(open(p, encoding="utf-8"))
    for b in d.get("blocks", []):
        h = b.get("html")
        if isinstance(h, str) and "price-row" in h:
            b["html"] = ROW.sub(lambda m: m.group(1)+m.group(2)+m.group(3)+price(m.group(2), m.group(4))+m.group(5), h)
    json.dump(d, open(p,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("firewood cords fixed (main-label match)")
