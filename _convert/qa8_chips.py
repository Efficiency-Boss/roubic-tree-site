"""QA8-C/D: update cross-sell 'related-card' chips (LSP + hub) to current
canonical prices. Also strip lot-clearing's residual own-price."""
import glob, re, os

CHIP = {
    "tree-removal": "$400–$5,000+",
    "tree-trimming-pruning": "$250–$2,500+",
    "stump-grinding": "$275 min",
    "land-clearing": "$1,500–$20,000+/acre",
    "storm-damage-emergency": "$500–$8,000+",
    "firewood-delivery": "$180–$450/cord",
}
CARD = re.compile(
    r'(<a class=\\?"related-card\\?" href=\\?"/[a-z0-9-]+/([a-z-]+)/\\?">.*?'
    r'<p class=\\?"price\\?">)([^<]*)(</p>)', re.S)

n_chips = n_files = 0
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    t = open(f, encoding="utf-8").read()
    if "related-card" not in t:
        continue

    def repl(m):
        global n_chips
        svc = m.group(2)
        if svc in CHIP:
            n_chips += 1
            return m.group(1) + CHIP[svc] + m.group(4)
        return m.group(0)
    nt = CARD.sub(repl, t)
    if nt != t:
        open(f, "w", encoding="utf-8").write(nt)
        n_files += 1

# lot-clearing residual own-price -> quoted
lc = "src/content/services/services__land-clearing__lot-clearing.json"
t = open(lc, encoding="utf-8").read()
for v in ("$1,500–$20,000+", "$1,500 – $20,000+", "$1,500-$20,000+"):
    t = t.replace(v, "quoted on-site")
open(lc, "w", encoding="utf-8").write(t)

print(f"chips updated: {n_chips} across {n_files} files; lot-clearing residual cleared")
