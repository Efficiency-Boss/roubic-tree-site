import json
def fix(path, reps):
    t = open(path, encoding="utf-8").read()
    n = 0
    for a, b in reps:
        c = t.count(a)
        if c:
            t = t.replace(a, b); n += c
    open(path, "w", encoding="utf-8").write(t)
    return n

# services index: trimming hub card -> $250-$2,500+
n1 = fix("src/content/services/services.json", [("$375–$800", "$250–$2,500+")])
# homepage: detailed price-range + note
n2 = fix("src/content/home/home.json", [
    ("<div class=\\\"price-range\\\">$375–$800</div>", "<div class=\\\"price-range\\\">$250–$2,500+</div>"),
    ("Mid-size deciduous $500–$800", "Mid-size deciduous $450–$800"),
])
# gates-mills removal hero chip -> removal headline
n3 = fix("src/content/pages/gates-mills-oh__tree-removal.json", [("$650–$950/tree", "$400–$5,000+")])
print(f"services-index:{n1}  home:{n2}  gates-mills:{n3}")
