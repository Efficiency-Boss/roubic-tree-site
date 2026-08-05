"""Pricing propagation PASS 3 — sweep the OLD tier/headline values everywhere
they still live (JSON-LD schema, prose, cross-links), not just the visible
table. Raw whole-file text replace, scoped to each service's own files, so the
same old string maps to the right canonical value per service.
Longest strings first to avoid substring collisions; dash variants covered.
"""
import glob, os

MAPS = {
    "tree-removal": [
        ("$3,500–$7,000+", "$2,000–$5,000+"), ("$200–$10,000+", "$400–$5,000+"),
        ("$300–$4,000+", "$400–$5,000+"), ("$300–$7,000+", "$400–$5,000+"),
        ("$1,800–$3,500", "$1,200–$2,200"), ("$850–$2,000", "$1,200–$2,200"),
        ("$1,000–$2,500", "$700–$1,400"), ("$700–$1,800", "$700–$1,400"),
        ("$300–$700", "$400–$700"),
    ],
    "tree-trimming-pruning": [
        ("$3,500–$7,000+", "$1,800–$2,500+"), ("$300–$7,000+", "$150–$2,500+"),
        ("$1,800–$3,500", "$800–$1,800"), ("$700–$1,800", "$350–$800"),
        ("$300–$700", "$150–$350"),
    ],
    "storm-damage-emergency": [
        ("$3,500–$7,000+", "$2,500–$8,000+"), ("$300–$7,000+", "$500–$8,000+"),
        ("$800–$8,000+", "$2,500–$8,000+"), ("$1,800–$3,500", "$2,500–$8,000+"),
        ("$700–$1,800", "$1,500–$5,000"), ("$300–$700", "$500–$1,500"),
    ],
    "land-clearing": [
        ("$1,500–$15,000", "$1,500–$20,000+"),
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
    # ordered; spaced en-dash and hyphen/em-dash forms
    return [s, s.replace("–", " – "), s.replace("–", "-"),
            s.replace("–", " - "), s.replace("–", "—"), s.replace("–", " — ")]


log = []
for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    s = svc_of(f)
    if not s:
        continue
    txt = open(f, encoding="utf-8").read()
    orig = txt
    for old, new in MAPS[s]:
        for vold in variants(old):
            if vold in txt:
                # keep the SAME dash style as matched: build matching new variant
                if " – " in vold:
                    vnew = new.replace("–", " – ")
                elif " - " in vold:
                    vnew = new.replace("–", " - ")
                elif " — " in vold:
                    vnew = new.replace("–", " — ")
                elif "-" in vold and "–" not in vold and "—" not in vold:
                    vnew = new.replace("–", "-")
                elif "—" in vold:
                    vnew = new.replace("–", "—")
                else:
                    vnew = new
                txt = txt.replace(vold, vnew)
    if txt != orig:
        open(f, "w", encoding="utf-8").write(txt)
        log.append(os.path.basename(f)[:-5])

print(f"files swept: {len(log)}")
for l in sorted(log):
    print("  ", l)
