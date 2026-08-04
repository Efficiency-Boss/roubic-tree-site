#!/usr/bin/env python
"""QA5: (A) restore the Auburn HQ tile photo on the homepage; (D) Tier-3 city
cards on service pages linked to the generic hub with no image -> give them the
city photo and link them to the city hub."""
import json, re, glob, os

IMG = 'public/images'
AVAIL = {p[:-5] for p in os.listdir(IMG) if p.endswith('.webp')}
NAME2SLUG = {
    'Auburn Township': 'auburn-township-oh', 'Pepper Pike': 'pepper-pike-oh',
    'Chagrin Falls': 'chagrin-falls-oh', 'Moreland Hills': 'moreland-hills-oh',
    'Solon': 'solon-oh', 'Gates Mills': 'gates-mills-oh', 'Beachwood': 'beachwood-oh',
    'Orange': 'orange-oh', 'Bainbridge Twp': 'bainbridge-township-oh',
    'Bainbridge Township': 'bainbridge-township-oh', 'Shaker Heights': 'shaker-heights-oh',
    'Chesterland': 'chesterland-oh', 'Mayfield': 'mayfield-oh', 'South Russell': 'south-russell-oh',
}

def media(slug, label):
    return (f'<span class="city-media"><img src="/images/roubic-{slug}-hero.webp" '
            f'alt="{label}, OH tree service" loading="lazy" width="240" height="120"/></span>')

# --- A) homepage HQ tile: re-add the media ---
hp = 'src/content/home/home.json'
d = json.load(open(hp, encoding='utf-8'))
for b in d['blocks']:
    h = b.get('html', '')
    if 'city-card hq' in h and 'city-card hq" href="/auburn-township-oh/"><i' in h:
        b['html'] = h.replace(
            '<a class="city-card hq" href="/auburn-township-oh/"><i',
            '<a class="city-card hq" href="/auburn-township-oh/">' + media('auburn-township-oh', 'Auburn Township') + '<i')
json.dump(d, open(hp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('HQ tile media re-added:', 'city-card hq"' in open(hp,encoding='utf-8').read() and 'hq" href="/auburn-township-oh/"><span' in open(hp,encoding='utf-8').read())

# --- D) service pages: city cards linking to /services/... with no image ---
fixed = 0
for f in glob.glob('src/content/services/*.json'):
    d = json.load(open(f, encoding='utf-8'))
    ch = False
    for b in d.get('blocks', []):
        h = b.get('html', '')
        if 'tier-block' not in h or 'city-card' not in h:
            continue
        def repl(m):
            nonlocal_ch = m.group(0)
            full, href, inner = m.group(0), m.group(1), m.group(2)
            if not href.startswith('/services/') or 'city-media' in inner:
                return full
            name = re.sub(r'<[^>]+>', '', inner).strip()
            slug = NAME2SLUG.get(name)
            if not slug or f'roubic-{slug}-hero' not in AVAIL:
                return full
            new_href = f'/{slug}/'
            new_inner = media(slug, name) + inner
            return f'<a class="city-card" href="{new_href}">{new_inner}</a>'
        nh = re.sub(r'<a class="city-card"[^>]*href="([^"]+)">(.*?)</a>', repl, h, flags=re.S)
        if nh != h:
            b['html'] = nh; ch = True
    if ch:
        json.dump(d, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); fixed += 1
print('service pages with tier-3 cards fixed:', fixed)
