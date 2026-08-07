import glob, json, os
# tree-removal FAQ range phrasing -> canonical $400-$5,000+
reps = [
    ("$300 for a small tree under 30 ft to $7,000+", "$400 for a small tree under 30 ft to $5,000+"),
    ("$300 for a small tree to $7,000+", "$400 for a small tree to $5,000+"),
    ("$300–$7,000+", "$400–$5,000+"), ("$300 – $7,000+", "$400 – $5,000+"),
    ("to $7,000+", "to $5,000+"),
    ("from $300 for", "from $400 for"),
]
n=0
for f in glob.glob("src/content/**/*__tree-removal.json", recursive=True)+["src/content/services/services__tree-removal.json"]:
    if not os.path.exists(f): continue
    t=open(f,encoding="utf-8").read(); o=t
    for a,b in reps: t=t.replace(a,b)
    if t!=o: open(f,"w",encoding="utf-8").write(t); n+=1
print(f"removal FAQ phrasing fixed in {n} files")
