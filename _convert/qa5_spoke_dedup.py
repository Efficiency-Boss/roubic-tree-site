#!/usr/bin/env python
"""QA5 #C: hub spoke-cards + spoke sib-cards mostly reused the parent hero photo
('almost all the same'). No new client photos available, so distribute the
existing real photos so each card on a page is unique — keeping the good
thematic matches (oak->oak-care, ash->ash-disease, and the spoke's own hero)."""
import json, re, glob, os

IMG = 'public/images'
AVAIL = {p[:-5] for p in os.listdir(IMG) if p.endswith('.webp')}
# real tree/work photos (no city heroes, portraits, placeholders, logos)
POOL = [x for x in [
    'roubic-oak-tree-care-hero','roubic-ash-tree-disease-management-hero',
    'roubic-large-tree-removal-hero','roubic-dangerous-dead-tree-removal-hero','roubic-residential-tree-removal-hero',
    'roubic-commercial-tree-removal-hero','roubic-fallen-tree-removal-hero','roubic-emergency-tree-removal-hero',
    'roubic-arborist-guide-hero','roubic-ohio-tree-species-guide-hero','roubic-storm-preparation-checklist-hero',
    'roubic-homepage-hero-before','roubic-seasoned-firewood-hero',
    'roubic-pepper-pike-oh-tree-trimming-pruning-hero','roubic-pepper-pike-oh-tree-removal-hero',
    'roubic-pepper-pike-oh-stump-grinding-hero','roubic-pepper-pike-oh-land-clearing-hero',
    'roubic-pepper-pike-oh-storm-damage-emergency-hero','roubic-pepper-pike-oh-firewood-delivery-hero',
] if x in AVAIL]

def dedup(html, card_cls):
    anchors = re.findall(r'<a class="' + card_cls + r'"[^>]*href="([^"]+)">', html)
    if len(anchors) < 2:
        return html
    slugs = [h.rstrip('/').split('/')[-1] for h in anchors]
    # pass 1: reserve thematic matches
    used = set()
    assign = {}
    for i, s in enumerate(slugs):
        m = f'roubic-{s}-hero'
        if m in AVAIL:
            assign[i] = m; used.add(m)
    # pass 2: unmatched get next unused pool image
    pi = 0
    for i in range(len(slugs)):
        if i in assign:
            continue
        while pi < len(POOL) and POOL[pi] in used:
            pi += 1
        img = POOL[pi] if pi < len(POOL) else POOL[i % len(POOL)]
        assign[i] = img; used.add(img); pi += 1
    # apply: replace the first image url inside each anchor
    idx = [0]
    def repl(m):
        i = idx[0]; idx[0] += 1
        inner = m.group(2)
        new = re.sub(r'(/images/)[a-z0-9-]+(\.webp)', r'\1' + assign[i] + r'\2', inner, count=1)
        return f'<a class="{card_cls}" href="{m.group(1)}">' + new
    return re.sub(r'<a class="' + card_cls + r'"[^>]*href="([^"]+)">((?:(?!</a>).)*)', repl, html, flags=re.S)

changed = 0
for f in glob.glob('src/content/services/*.json'):
    d = json.load(open(f, encoding='utf-8'))
    ch = False
    for b in d.get('blocks', []):
        h = b.get('html')
        if not h:
            continue
        for cls in ['spoke-card', 'sib-card']:
            if cls in h:
                nh = dedup(h, cls)
                if nh != h:
                    b['html'] = nh; h = nh; ch = True
    if ch:
        json.dump(d, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); changed += 1
print('service pages deduped:', changed)
# verify trimming hub
d = json.load(open('src/content/services/services__tree-trimming-pruning.json', encoding='utf-8'))
for b in d['blocks']:
    if 'spoke-card' in b.get('html', ''):
        imgs = re.findall(r'<a class="spoke-card".*?/images/([a-z0-9-]+)\.webp', b['html'], re.S)
        print('trimming spoke images: %d unique of %d' % (len(set(imgs)), len(imgs)))
        break
