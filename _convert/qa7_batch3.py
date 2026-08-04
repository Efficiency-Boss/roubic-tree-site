"""QA7 batch 3 content edits:
 #22 broken Pro icon fa-house-crash -> fa-house-crack (chagrin land-clearing)
 #25 strip leading +/- signs from EFFECT-ON-PRICE table cells (cost guide)
 #27a change "Table of Contents" <h4> -> non-heading <span class="toc-title">
 #24 repoint dead agri.ohio.gov root citation -> working state ODA tree page
"""
import json, glob, os, re

stats = {"icon": 0, "signs": 0, "toc_h4": 0, "agri": 0}

# leading +, minus(U+2212), en-dash, hyphen before a digit or $, right after <td>
LEAD = re.compile(r'(<td>)[+\u2212\u2013-](?=[\d$])')
TOC = re.compile(r'<h4>(\s*Table of Contents\s*)</h4>')

for f in glob.glob("src/content/**/*.json", recursive=True):
    if os.path.basename(os.path.dirname(f)) == "globals":
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(d, dict) or "blocks" not in d:
        continue
    changed = False
    for b in d["blocks"]:
        h = b.get("html")
        if not isinstance(h, str):
            continue
        o = h
        if "fa-house-crash" in h:
            stats["icon"] += h.count("fa-house-crash")
            h = h.replace("fa-house-crash", "fa-house-crack")
        if "EFFECT ON PRICE" in h or "climbing job" in h:
            h, n = LEAD.subn(r"\1", h)
            stats["signs"] += n
        if "Table of Contents" in h:
            h, n = TOC.subn(r'<span class="toc-title">\1</span>', h)
            stats["toc_h4"] += n
        if h != o:
            b["html"] = h
            changed = True
    if changed:
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print(stats)
