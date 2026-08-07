"""Dump every price token per file with its enclosing element, so we can build
exact QA8 replacements. Usage: python _convert/qa8_dump.py <path-substring>"""
import json, glob, re, os, sys

PRICE = re.compile(r"\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?|[+~]?\d{1,3}\s*[–—-]\s*\d{1,3}\s*%|\$?\d+\s*/\s*inch|\$?\d+\s*min\b")
FILT = sys.argv[1] if len(sys.argv) > 1 else ""


def enclosing(h, pos):
    pre = h[max(0, pos - 70):pos]
    m = re.findall(r'class=\\?"([a-z0-9 _-]+)\\?"[^>]*>[^<]*$', pre)
    if m:
        return m[-1]
    m2 = re.findall(r"<([a-z0-9]+)[^>]*>[^<]*$", pre)
    return "<" + m2[-1] + ">" if m2 else "?"


for f in sorted(glob.glob("src/content/**/*.json", recursive=True)):
    if FILT and FILT not in f:
        continue
    d = json.load(open(f, encoding="utf-8"))
    if not isinstance(d, dict):
        continue
    hits = []
    seo = d.get("seo") or {}
    for k in ("title", "description"):
        for m in PRICE.finditer(seo.get(k, "")):
            hits.append((f"seo.{k}", m.group(0).strip()))
    jl = d.get("jsonld", "")
    if isinstance(jl, str):
        for m in PRICE.finditer(jl):
            hits.append(("jsonld", m.group(0).strip()))
    for bi, b in enumerate(d.get("blocks", [])):
        h = b.get("html", "")
        if not isinstance(h, str):
            continue
        for m in PRICE.finditer(h):
            hits.append((f"b{bi}:{enclosing(h, m.start())}", m.group(0).strip()))
    if hits:
        print(f"### {os.path.basename(f)}")
        for loc, val in hits:
            print(f"   {loc:34} {val}")
