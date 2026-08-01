#!/usr/bin/env python
"""QA round 3: location hubs AND city+service (LSP) pages repeated the city-hero
photo across every service/related card + project card (up to 9x the same image
on one page). Give each service/related card its matching service photo
(city-specific if it exists, else the generic service hero) and each project card
a distinct real work photo, so no image repeats on a page."""
import json, re, os, glob
from collections import Counter

IMG = 'public/images'
AVAIL = {p[:-5] for p in os.listdir(IMG) if p.endswith('.webp')}
PROJECT_IMGS = ['roubic-fallen-tree-removal-hero',
                'roubic-oak-tree-care-hero',
                'roubic-emergency-tree-removal-hero']

def set_bg(fragment, cls, new_img):
    return re.sub(
        r'(' + cls + r'"\s+style="background-image:\s*url\(\')/images/[a-z0-9-]+\.webp',
        r'\1/images/' + new_img + '.webp', fragment, count=1)

def fix_service_grid(html, city, card_cls, thumb_cls):
    def repl(m):
        card = m.group(0)
        hm = re.search(r'href="/(?:' + re.escape(city) + r'|services)/([a-z-]+)/"', card)
        if not hm:
            return card
        service = hm.group(1)
        cand = f'roubic-{city}-{service}-hero'
        img = cand if cand in AVAIL else f'roubic-{service}-hero'
        if img not in AVAIL:
            return card
        return set_bg(card, thumb_cls, img)
    return re.sub(r'<a class="' + card_cls + r'".*?</a>', repl, html, flags=re.S)

def fix_projects(html):
    idx = [0]
    def repl(m):
        i = idx[0]; idx[0] += 1
        if i >= len(PROJECT_IMGS) or PROJECT_IMGS[i] not in AVAIL:
            return m.group(0)
        return set_bg(m.group(0), 'project-img', PROJECT_IMGS[i])
    return re.sub(r'<div class="project-img"[^>]*>', repl, html)

def city_of(path):
    base = os.path.basename(path)[:-5]
    return base.split('__')[0]  # LSP: city__service -> city ; hub: city

changed = 0
for f in glob.glob('src/content/locations/*.json') + glob.glob('src/content/pages/*.json'):
    d = json.load(open(f, encoding='utf-8'))
    city = city_of(f)
    ch = False
    for b in d.get('blocks', []):
        h = b.get('html')
        if not h:
            continue
        if 'cs-card' in h:
            nh = fix_service_grid(h, city, 'cs-card', 'cs-thumb')
            if nh != h: b['html'] = nh; h = nh; ch = True
        if 'related-card' in h:
            nh = fix_service_grid(h, city, 'related-card', 'related-thumb')
            if nh != h: b['html'] = nh; h = nh; ch = True
        if 'project-img' in h:
            nh = fix_projects(h)
            if nh != h: b['html'] = nh; ch = True
    if ch:
        json.dump(d, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        changed += 1

print(f'files changed: {changed}')
print('--- remaining on-page dups (locations + pages) ---')
left = 0
for f in sorted(glob.glob('src/content/locations/*.json') + glob.glob('src/content/pages/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    imgs = []
    for b in d.get('blocks', []):
        imgs += re.findall(r'/images/([a-z0-9-]+)\.webp', b.get('html', ''))
    dups = [(i, c) for i, c in Counter(imgs).items() if c > 1]
    if dups:
        left += 1
        print(f'  {os.path.basename(f)}: {dups}')
print('ALL CLEAN' if left == 0 else f'{left} pages still have dups')
