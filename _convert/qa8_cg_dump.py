import json, re
d = json.load(open("src/content/resources/tree-service-cost-guide.json", encoding="utf-8"))
h = d["blocks"][2]["html"]
# split by service section headings (h2 or section) and show label|amt rows
# rows look like: <div ...><span class="lbl?">LABEL</span>...<span class="amt">PRICE</span>
rows = re.findall(r'<(?:div|li|tr)[^>]*>(?:(?!</(?:div|li|tr)>).)*?class="amt">([^<]+)</[^>]*>', h)
# better: capture each row block containing an .amt
for m in re.finditer(r'([A-Z][A-Za-z0-9 &/\'\-–—\"()+.,]{3,60}?)\s*(?:</[a-z0-9]+>\s*)*<[^>]*class="amt">([^<]+)<', h):
    lbl = re.sub(r"\s+", " ", m.group(1)).strip()
    print(f"   {lbl[:52]:54} | {m.group(2).strip()}")
