import json, re
d = json.load(open("src/content/resources/tree-service-cost-guide.json", encoding="utf-8"))
h = d["blocks"][2]["html"]
for kw in ("Stump", "Firewood", "Storm"):
    i = h.find(kw)
    while i != -1 and ("<h2" not in h[max(0, i-40):i] and "eyebrow" not in h[max(0, i-60):i]):
        i = h.find(kw, i + 1)
    if i == -1:
        i = h.find(kw)
    seg = h[i - 40:i + 620]
    seg = re.sub(r"\s+", " ", re.sub(r"<([a-z0-9]+)[^>]*>", r"‹\1›", seg))
    print(f"===== {kw} =====")
    print(seg[:620])
    print()
