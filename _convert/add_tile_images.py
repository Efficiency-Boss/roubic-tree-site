#!/usr/bin/env python
"""Design-QA round 1 (2026-07-31): client asked for photos on the city tiles
(.city-card, service hub/spoke pages) and the nearby-city cards (.adj-card,
location + LSP pages). Idempotent: only inserts a <span>...<img></span> where
one isn't already present AND the matching city hero webp exists."""
import json, re
from pathlib import Path

ROOT = Path('src/content')
IMGDIR = Path('public/images')
AVAIL = {p.stem for p in IMGDIR.glob('*.webp')}

def city_from_href(href):
    m = re.match(r'/([a-z-]+-oh)(?:/[a-z-]+)?/$', href)
    return m.group(1) if m else None

def make_inserter(card_cls, media_cls, alt_suffix):
    pat = re.compile(r'(<a class="' + card_cls + r'[^"]*" href="([^"]+)">)(?!<span class="' + media_cls + r'")')
    def repl(m):
        full, href = m.group(0), m.group(2)
        city = city_from_href(href)
        img = f'roubic-{city}-hero' if city else None
        if not city or img not in AVAIL:
            return full
        alt = city.replace('-oh', '').replace('-', ' ').title()
        media = (f'<span class="{media_cls}"><img src="/images/{img}.webp" '
                 f'alt="{alt}{alt_suffix}" loading="lazy" width="240" height="120"/></span>')
        return full + media
    return lambda html: pat.sub(repl, html)

ins_city = make_inserter('city-card', 'city-media', ', OH tree service')
ins_adj  = make_inserter('adj-card',  'adj-media',  ', OH')

stats = {'city_files': 0, 'city_imgs': 0, 'adj_files': 0, 'adj_imgs': 0}
for f in ROOT.rglob('*.json'):
    if f.parent.name == 'globals':
        continue
    d = json.loads(f.read_text(encoding='utf-8'))
    if not isinstance(d, dict) or 'blocks' not in d:
        continue
    changed = False
    cf = af = 0
    for b in d['blocks']:
        h = b.get('html')
        if not h:
            continue
        if 'class="city-card' in h and 'tier-block' in h:
            nh = ins_city(h)
            if nh != h:
                added = nh.count('city-media') - h.count('city-media')
                b['html'] = nh; changed = True; cf += added
        if 'class="adj-card' in h:
            nh = ins_adj(h)
            if nh != h:
                added = nh.count('adj-media') - h.count('adj-media')
                b['html'] = nh; changed = True; af += added
    if changed:
        f.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding='utf-8')
        if cf: stats['city_files'] += 1; stats['city_imgs'] += cf
        if af: stats['adj_files'] += 1; stats['adj_imgs'] += af

print(stats)
