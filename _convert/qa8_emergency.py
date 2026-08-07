import json, re
p = "src/content/services/services__tree-removal__emergency-tree-removal.json"
d = json.load(open(p, encoding="utf-8"))
ROWP = re.compile(r'(<div class="price">)([^<]*)(</div>)')
PT = re.compile(r"\$[\d,]+(?:\s*[–—-]\s*\$?[\d,]+)?\+?")
for bi, b in enumerate(d["blocks"]):
    h = b.get("html")
    if not isinstance(h, str):
        continue
    o = h
    if bi == 0:
        h = PT.sub("+25–50% over standard", h, count=1)
    if "price-row" in h:
        h = ROWP.sub(lambda m: m.group(1) + ("+25–50% over standard" if "$" in m.group(2) else m.group(2)) + m.group(3), h)
    h = h.replace("land between $1,200 and $5,000+", "run about 25–50% over standard removal rates")
    h = h.replace("between $1,200 and $5,000+", "25–50% over standard removal rates")
    h = h.replace("can exceed $5,000+", "carry the same 25–50% emergency premium")
    if h != o:
        b["html"] = h
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("emergency reframed")
for bi, b in enumerate(d["blocks"]):
    h = b.get("html", "")
    for m in re.findall(r"[^.>]*25–50%[^.<]*", h)[:3]:
        print("   ", re.sub("<[^>]+>", "", m).strip()[:95])
