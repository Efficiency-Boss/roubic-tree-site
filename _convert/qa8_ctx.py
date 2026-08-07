import json, re
for f, label in [("home/home.json", "home"),
                 ("services/services.json", "services-index"),
                 ("pages/gates-mills-oh__tree-removal.json", "gm-removal")]:
    t = json.dumps(json.load(open("src/content/" + f, encoding="utf-8")))
    for pat in ["$375–$800", "$375-$800", "$650–$950/tree", "$650-$950/tree"]:
        for m in re.finditer(re.escape(pat), t):
            s = m.start()
            seg = re.sub(r"<[^>]+>", " ", t[s - 75:s + 30])
            seg = re.sub(r"\s+", " ", seg).strip()
            print(f"[{label}] ...{seg[-95:]}")
