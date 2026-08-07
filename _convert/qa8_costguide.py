"""QA8-E + stump-in-cost-guide: fix tree-service-cost-guide sections."""
p = "src/content/resources/tree-service-cost-guide.json"
t = open(p, encoding="utf-8").read()
reps = [
    # STUMP: strip per-inch formula, size prices -> Quoted on-site
    ("plus $8 per inch of stump diameter, ", ""),
    ("$275 + $8/inch after 12\\\"", "quoted by stump size"),
    ("$275 + $8/inch", "quoted by stump size"),
    ("$8/inch", ""),
    ("$8 per inch", ""),
    (">$275–$375<", ">Quoted on-site<"),
    (">$275-$375<", ">Quoted on-site<"),
    (">$375–$465<", ">Quoted on-site<"),
    (">$375-$465<", ">Quoted on-site<"),
    # FIREWOOD: face + full cord per sheet
    ("$180–$220", "$180–$240"),
    (">$350–$450<", ">$280–$380<"),   # full-cord row (was premium price)
    # STORM: tree-on-structure per sheet
    ("$1,500–$4,000", "$2,500–$8,000+"),
    # LAND: medium density per sheet
    ("$3,000–$8,000/acre", "$3,000–$5,000/acre"),
]
n = 0
for a, b in reps:
    c = t.count(a)
    if c:
        t = t.replace(a, b)
        n += c
open(p, "w", encoding="utf-8").write(t)
print(f"cost-guide: {n} replacements applied")
