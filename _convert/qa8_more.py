import json, re
# services-index hub cards (all 6)
d = json.load(open("src/content/services/services.json", encoding="utf-8"))
print("=== /services/ hub cards ===")
for b in d["blocks"]:
    h = b.get("html", "")
    if "hub-card-price" in h:
        for name, price in re.findall(r"<h[23][^>]*>(.*?)</h[23]>.*?hub-card-price\">([^<]+)<", h, re.S):
            print(f"   {re.sub('<[^>]+>','',name).strip()[:28]:30} {price.strip()}")
        break
# homepage price-range + price-note
d = json.load(open("src/content/home/home.json", encoding="utf-8"))
print("=== homepage price-range / price-note (trimming area) ===")
for b in d["blocks"]:
    h = b.get("html", "")
    if "price-range" in h and "Trimming" in h:
        for m in re.findall(r'(?:price-range|price-note)\">([^<]+)<', h):
            print("   ", m.strip()[:70])
# gates-mills removal hero chip
d = json.load(open("src/content/pages/gates-mills-oh__tree-removal.json", encoding="utf-8"))
print("=== gates-mills removal hero chips ===")
h = d["blocks"][0].get("html", "")
for m in re.findall(r"<span>(?:<i[^>]*></i>)?([^<]+)</span>", h)[:8]:
    print("   ", m.strip()[:40])
