import json, re
ROW = re.compile(r'(<div class="scenario">)(.*?)(</div>.*?<div class="price">)([^<]*)(</div>)', re.S)


def remap(path, fn):
    d = json.load(open(path, encoding="utf-8"))
    for b in d.get("blocks", []):
        h = b.get("html")
        if isinstance(h, str) and "price-row" in h:
            b["html"] = ROW.sub(lambda m: m.group(1) + m.group(2) + m.group(3)
                                + fn(re.sub("<[^>]+>", " ", m.group(2)).lower(), m.group(4)) + m.group(5), h)
    json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def storm(scen, cur):
    if "emergency" in scen or "after-hours" in scen:
        return "25–50% over scheduled rates"           # remove leading +
    if "full-property" in scen or "full property" in scen:
        return "Quoted on-site"                          # not in sheet
    return cur


def firewood(scen, cur):
    if "premium" in scen or "oak" in scen:
        return "$350–$450"
    return cur


remap("src/content/services/services__storm-damage-emergency.json", storm)
remap("src/content/services/services__firewood-delivery.json", firewood)
print("storm + firewood hub tables fixed")
# verify
for p, lbl in [("services__storm-damage-emergency", "STORM"), ("services__firewood-delivery", "FIREWOOD")]:
    d = json.load(open(f"src/content/services/{p}.json", encoding="utf-8"))
    for b in d["blocks"]:
        h = b.get("html", "")
        if "price-row" in h:
            print(f"-- {lbl} --")
            for sc, pr in re.findall(r'<div class="scenario">(.*?)</div>.*?<div class="price">([^<]+)<', h, re.S):
                print("   ", re.sub("<[^>]+>", " ", sc).strip()[:34], "->", pr.strip())
            break
