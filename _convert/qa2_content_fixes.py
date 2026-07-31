#!/usr/bin/env python
"""QA round 2 content fixes: make phone/email tap-to-call/email, add the
#pricing anchor id. Idempotent + safe (only touches specific patterns)."""
import json, re, glob, os

files = glob.glob('src/content/**/*.json', recursive=True)
stat = {'phone': 0, 'email': 0, 'pricing': 0}
for f in files:
    if os.path.basename(os.path.dirname(f)) == 'globals':
        continue
    d = json.loads(open(f, encoding='utf-8').read())
    if not isinstance(d, dict) or 'blocks' not in d:
        continue
    changed = False
    for b in d['blocks']:
        h = b.get('html')
        if not h:
            continue
        orig = h
        h2 = re.sub(r'(<i class="fa-solid fa-phone"></i>)\s*(\{\{global\.phone\}\})(?!</a>)',
                    r'\1<a href="{{global.phone_href}}">\2</a>', h)
        stat['phone'] += (h2 != h); h = h2
        h2 = re.sub(r'(<i class="fa-solid fa-envelope"></i>)\s*(info@\{\{global\.domain\}\})(?!</a>)',
                    r'\1<a href="mailto:\2">\2</a>', h)
        stat['email'] += (h2 != h); h = h2
        h2 = h.replace('<section class="pricing">', '<section class="pricing" id="pricing">')
        stat['pricing'] += (h2 != h); h = h2
        if h != orig:
            b['html'] = h; changed = True
    if changed:
        open(f, 'w', encoding='utf-8').write(json.dumps(d, indent=1, ensure_ascii=False))
print(stat)
