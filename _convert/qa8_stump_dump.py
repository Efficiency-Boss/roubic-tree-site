import json, glob, re, os
ROW = re.compile(r'<div class=\\?"scenario\\?">(.*?)</div>.*?<div class=\\?"price\\?">([^<]+)<', re.S)
for f in sorted(glob.glob("src/content/**/*stump*.json", recursive=True)) + ["src/content/resources/tree-service-cost-guide.json"]:
    if not os.path.exists(f):
        continue
    d = json.load(open(f, encoding="utf-8"))
    for bi, b in enumerate(d.get("blocks", [])):
        h = b.get("html", "")
        if "price-row" in h and "scenario" in h:
            rows = ROW.findall(h)
            if rows:
                print(f"### {os.path.basename(f)}  (block {bi})")
                for sc, pr in rows:
                    sc = re.sub(r"<[^>]+>", " ", sc)
                    sc = re.sub(r"\s+", " ", sc).strip()
                    print(f"     {sc[:44]:46} | {pr.strip()}")
