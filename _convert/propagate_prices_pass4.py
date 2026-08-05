"""Pricing propagation PASS 4 — the LSP cross-sell 'related-card' chips.
Each chip links to a sibling service and shows a mini price that must equal that
service's canonical headline. We rewrite the chip's <p class="price"> based on
the service in its href."""
import glob, re, os

CHIP = {
    "tree-removal": "$400–$5,000+",
    "tree-trimming-pruning": "$150–$2,500+",
    "stump-grinding": "$150–$800",
    "land-clearing": "$1,500–$20,000+/acre",
    "storm-damage-emergency": "$500–$8,000+",
    "firewood-delivery": "$180–$450/cord",
}
# match: <a class="related-card" href="/<city>/<service>/"> ... <p class="price">VALUE</p>
CARD = re.compile(
    r'(<a class=\\"related-card\\" href=\\"/[a-z0-9-]+/([a-z-]+)/\\">.*?'
    r'<p class=\\"price\\">)([^<]*)(</p>)',
    re.S)

n_files = 0
n_chips = 0
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    txt = open(f, encoding="utf-8").read()
    if "related-card" not in txt:
        continue

    def repl(m):
        global n_chips
        svc = m.group(2)
        if svc in CHIP:
            n_chips += 1
            return m.group(1) + CHIP[svc] + m.group(4)
        return m.group(0)

    new = CARD.sub(repl, txt)
    if new != txt:
        open(f, "w", encoding="utf-8").write(new)
        n_files += 1

print(f"chips rewritten: {n_chips} across {n_files} files")
