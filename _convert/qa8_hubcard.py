import json, re
d = json.load(open("src/content/locations/auburn-township-oh.json", encoding="utf-8"))
for bi, b in enumerate(d["blocks"]):
    h = b.get("html", "")
    if "Tree Removal" in h and "Firewood" in h and "Stump" in h:
        sec = re.search(r'<section class="([^"]+)"', h)
        print(f"block {bi} section={sec.group(1) if sec else '?'}")
        i = h.find("Tree Removal")
        seg = h[max(0, i - 120):i + 900]
        seg = re.sub(r"\s+", " ", re.sub(r"<([a-z0-9]+)[^>]*>", r" <\1> ", seg))
        print(seg[:900])
        break
