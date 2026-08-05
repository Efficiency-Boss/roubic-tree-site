"""PASS 5 — correct to the CLIENT-CONFIRMED Roubic prices (signed sheet 2026-06-04).
My earlier overhaul used the Industry-benchmark column because the Roubic columns
were blank; they're now filled. Rows marked "industry bm" keep the benchmark
(already correct). Scoped per service to avoid cross-contamination."""
import glob, os

MAPS = {
    # tree removal: benchmark tiers I published -> client-confirmed tiers
    "tree-removal": [
        ("$700–$1,400", "$650–$950"),    # medium
        ("$1,200–$2,200", "$850–$2,000"), # large
        ("$400–$700", "$400–$800"),       # small
        # very large $2,000–$5,000+ and headline $400–$5,000+ unchanged
    ],
    # trimming: only small-ornamental + mid-size were confirmed different
    "tree-trimming-pruning": [
        ("$150–$2,500+", "$250–$2,500+"), # headline floor (deadwood bm $250 is lowest)
        ("$150–$350", "$375–$500"),        # small ornamental (hub + LSP Small tier)
        ("$150–$400", "$375–$500"),        # fruit-tree spoke = small ornamental
        ("$350–$800", "$450–$800"),        # mid-size deciduous
    ],
    # stump: client minimum is $275 (not $150)
    "stump-grinding": [
        ("$150 min", "$275 min"),
        ("$150 Min", "$275 min"),
    ],
}
SVC = list(MAPS)


def svc_of(f):
    b = os.path.basename(f)
    for s in SVC:
        if (b == f"services__{s}.json" or b.endswith(f"__{s}.json")
                or f"__{s}__" in b or f"services__{s}__" in b):
            return s


def variants(s):
    return [s, s.replace("–", " – "), s.replace("–", "-"),
            s.replace("–", " - "), s.replace("–", "—"), s.replace("–", " — ")]


log = []
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    s = svc_of(f)
    if not s:
        continue
    txt = open(f, encoding="utf-8").read()
    o = txt
    for old, new in MAPS[s]:
        for vold in variants(old):
            if vold in txt:
                if " – " in vold:   vnew = new.replace("–", " – ")
                elif " - " in vold: vnew = new.replace("–", " - ")
                elif " — " in vold: vnew = new.replace("–", " — ")
                elif "—" in vold:   vnew = new.replace("–", "—")
                elif "-" in vold and "–" not in vold: vnew = new.replace("–", "-")
                else: vnew = new
                txt = txt.replace(vold, vnew)
    if txt != o:
        open(f, "w", encoding="utf-8").write(txt)
        log.append(os.path.basename(f)[:-5])

print(f"files corrected: {len(log)}")
