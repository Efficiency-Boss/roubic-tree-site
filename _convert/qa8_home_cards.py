import json, re
d = json.load(open("src/content/home/home.json", encoding="utf-8"))
for bi, b in enumerate(d["blocks"]):
    h = b.get("html", "")
    if "service-card" in h and "Trimming" in h:
        print(f"block {bi}")
        # each card: <h3>NAME</h3> ... price text
        for card in re.findall(r"<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|</section|$)", h, re.S):
            name = re.sub(r"<[^>]+>", "", card[0]).strip()
            prices = re.findall(r"\$[\d,]+[^<\"]*", card[1])
            print(f"   {name[:30]:32} {prices[:2]}")
        break
