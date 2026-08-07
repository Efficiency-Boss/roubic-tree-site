"""Align stale JSON-LD Offer priceRange (and the trimming '$175' prose) with the
visible canonical prices. Only touches trimming hub, stump pages, brush-clearing."""
import glob

# --- trimming hub: schema offers + prose ---
p = "src/content/services/services__tree-trimming-pruning.json"
t = open(p, encoding="utf-8").read()
t = t.replace("$175–$400", "$375–$500").replace("$400–$900", "$450–$800").replace("$900–$2,500", "$800–$2,500+")
t = t.replace("a $175 small ornamental", "a $375 small ornamental").replace("$175 small ornamental", "$375 small ornamental")
open(p, "w", encoding="utf-8").write(t)

# --- stump pages: schema offer priceRanges match the restructured tables ---
STUMP = [
    ('\\"$150\\"', '\\"$275\\"'),                 # Minimum Visit offer value
    ("$150+", "$275+"),
    ("$275 minimum of diameter", "$2,000+"),      # commercial single -> commercial price
    ("30–50% below per-stump residential rates", "$2,000+"),
    ("$150–$250", "Quoted on-site"),
    ("$200–$300", "Quoted on-site"),
    ("$200–$400", "Quoted on-site"),
    ("$400–$800", "Quoted on-site"),
    ("$500–$1,000", "Quoted on-site"),
    ("$50–$150 off", "Quoted on-site"),
    ("From $250", "Quoted on-site"),
    ("$700–$1,200", "Quoted on-site"),
]
n = 0
for f in glob.glob("src/content/**/*stump*.json", recursive=True):
    t = open(f, encoding="utf-8").read(); o = t
    for a, b in STUMP:
        t = t.replace(a, b)
    if t != o:
        open(f, "w", encoding="utf-8").write(t); n += 1

# --- brush-clearing de-priced spoke: schema -> quoted ---
bc = "src/content/services/services__land-clearing__brush-clearing.json"
t = open(bc, encoding="utf-8").read()
t = t.replace("From $500", "Quoted on-site").replace("Up to $5,000", "Quoted on-site")
open(bc, "w", encoding="utf-8").write(t)

print(f"schema aligned: trimming hub + {n} stump files + brush-clearing")
