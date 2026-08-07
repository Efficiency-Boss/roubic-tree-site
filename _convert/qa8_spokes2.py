import json, re

base = "src/content/services/services__"
ROW = re.compile(r'(<div class="scenario">)(.*?)(</div>.*?<div class="price">)([^<]*)(</div>)', re.S)


def remap(f, fn):
    p = base + f
    d = json.load(open(p, encoding="utf-8"))
    for b in d.get("blocks", []):
        h = b.get("html")
        if isinstance(h, str) and "price-row" in h:
            b["html"] = ROW.sub(lambda m: m.group(1) + m.group(2) + m.group(3) + fn(re.sub("<[^>]+>", " ", m.group(2)).lower(), m.group(4)) + m.group(5), h)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


# residential: Large Residential -> $850-$2,000 (leave Small/Medium)
remap("tree-removal__residential-tree-removal.json",
      lambda s, cur: "$850–$2,000" if "large" in s else cur)
# seasoned firewood: cords per hub/sheet
def sf(s, cur):
    if "face" in s: return "$180–$240"
    if "half" in s: return "$230–$310"
    if "full" in s: return "$280–$380"
    return cur
remap("firewood-delivery__seasoned-firewood.json", sf)
print("residential Large + seasoned-firewood cords set")

# inspect emergency spoke table + FAQ
d = json.load(open(base + "tree-removal__emergency-tree-removal.json", encoding="utf-8"))
for bi, b in enumerate(d["blocks"]):
    h = b.get("html", "")
    if "price-row" in h:
        print(f"-- emergency table (b{bi}) --")
        for sc, pr in re.findall(r'<div class="scenario">(.*?)</div>.*?<div class="price">([^<]+)<', h, re.S):
            print("   ", re.sub("<[^>]+>", " ", sc).strip()[:40], "->", pr.strip())
    if "faq" in h.lower() and "$" in h:
        print(f"-- emergency FAQ (b{bi}) prices --")
        for m in re.findall(r"[^.>]*\$[\d,]+[^.<]*", h)[:4]:
            print("   ", re.sub("<[^>]+>", "", m).strip()[:100])
