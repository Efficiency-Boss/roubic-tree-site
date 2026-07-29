// Redirect walk (CI): every redirect `to` target must resolve to a real built page in dist/.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const rows = JSON.parse(readFileSync(join(root, 'src', 'data', 'redirects.json'), 'utf8'));
if (!existsSync(dist)) { console.error('dist/ missing.'); process.exit(1); }

const fails = [];
for (const r of rows) {
  if (String(r.status).startsWith('3')) {
    const target = r.to.replace(/^\/+|\/+$/g, '');
    const ok = target === '' ? existsSync(join(dist, 'index.html'))
                             : existsSync(join(dist, target, 'index.html')) || existsSync(join(dist, target));
    if (!ok) fails.push(`${r.from} -> ${r.to} (target not built)`);
  }
}
console.log(`redirect walk: ${rows.length} rule(s)`);
if (fails.length) { console.error('BROKEN REDIRECTS:\n  ' + fails.join('\n  ')); process.exit(1); }
console.log('redirect walk: PASS');
