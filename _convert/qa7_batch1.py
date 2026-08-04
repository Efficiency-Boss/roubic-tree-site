#!/usr/bin/env python
"""QA7 batch 1: broken FA icons (site-wide) + chrome.ts (headings->plain,
menu Storm/Firewood, footer logo link, sitemap link)."""
import json, re, glob, os

# --- broken FA6-free icons -> valid replacements (content + chrome) ---
ICON_FIX = {'fa-shield-check': 'fa-shield-halved', 'fa-crane': 'fa-arrows-up-to-line'}
n_icons = 0
for f in glob.glob('src/content/**/*.json', recursive=True):
    if os.path.basename(os.path.dirname(f)) == 'globals':
        continue
    d = json.loads(open(f, encoding='utf-8').read())
    if not isinstance(d, dict) or 'blocks' not in d:
        continue
    ch = False
    for b in d['blocks']:
        h = b.get('html')
        if not h: continue
        for bad, good in ICON_FIX.items():
            if bad in h: h = h.replace(bad, good); ch = True; n_icons += 1
        b['html'] = h
    if ch:
        json.dump(d, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('content icon fixes (files touched-ish):', n_icons)

# --- chrome.ts ---
cf = 'src/lib/chrome.ts'
c = open(cf, encoding='utf-8').read()
for bad, good in ICON_FIX.items():
    c = c.replace(bad, good)
# #2/#3 mega + footer column headings -> plain (div.col-head)
c = re.sub(r'<h4>(.*?)</h4>', r'<div class="col-head">\1</div>', c)
# modal h3 -> p
c = c.replace('<h3>Free Auburn Township Firewood Quote</h3>',
              '<p class="modal-h">Free Auburn Township Firewood Quote</p>')
# #7 sitemap link
c = c.replace('href="/sitemap.xml"', 'href="/sitemap-index.xml"')
# #6 footer logo -> link to home
c = c.replace(
    '<img alt="Roubic Tree &amp; Landscape LLC" src="/brand_assets/ROUBIC TREE ALL GOLD.png"/>',
    '<a href="/" aria-label="Roubic Tree home"><img alt="Roubic Tree &amp; Landscape LLC" src="/brand_assets/ROUBIC TREE ALL GOLD.png"/></a>')
# #5 add Storm & Firewood column to the Services mega (after Grinding & Clearing col)
anchor = '<li><a href="/services/land-clearing/brush-clearing/">Brush Clearing</a></li>\n</ul>\n</div>'
newcol = anchor + '''
<div class="mega-col">
<div class="col-head">Storm & Firewood</div>
<ul>
<li><a class="hub-link" href="/services/storm-damage-emergency/">Storm Damage & Emergency →</a></li>
<li><a href="/services/storm-damage-emergency/24-7-emergency-tree-service/">24/7 Emergency Service</a></li>
<li><a href="/services/storm-damage-emergency/fallen-tree-removal/">Fallen Tree Removal</a></li>
<li><a class="hub-link" href="/services/firewood-delivery/">Firewood Delivery →</a></li>
<li><a href="/services/firewood-delivery/seasoned-firewood/">Seasoned Firewood</a></li>
</ul>
</div>'''
c = c.replace(anchor, newcol, 1)
open(cf, 'w', encoding='utf-8').write(c)
print('chrome.ts: h4->col-head:', c.count('col-head'), '| sitemap-index:', '/sitemap-index.xml' in c,
      '| footer logo link:', 'aria-label="Roubic Tree home"' in c, '| storm col:', 'Storm & Firewood' in c)
