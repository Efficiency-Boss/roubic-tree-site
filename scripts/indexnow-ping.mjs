// IndexNow ping (post-deploy CI step, default-branch only). Submits the built
// URL set to IndexNow. No-ops safely when no key is configured (greenfield) so
// the step is wired and ready without ever failing a build. Best-effort: any
// error logs and exits 0 — a ping failure must never block deploys.
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative, sep } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const SITE = (process.env.SITE_URL || process.env.URL || 'https://roubic-tree-site.netlify.app').replace(/\/$/, '');

// key: CMS field first, then any agency static key file public/<key>.txt
function resolveKey() {
  try {
    const j = JSON.parse(readFileSync(join(root, 'src', 'content', 'globals', 'integrations.json'), 'utf8'));
    if (j.indexnow_key?.trim()) return j.indexnow_key.trim();
  } catch {}
  try {
    const f = readdirSync(join(root, 'public')).find((n) => /^[a-f0-9]{8,}\.txt$/i.test(n));
    if (f) return f.replace(/\.txt$/i, '');
  } catch {}
  return '';
}

const key = resolveKey();
if (!key) { console.log('IndexNow: no key configured — skipping (wire a key in integrations.json to activate).'); process.exit(0); }
if (!existsSync(dist)) { console.log('IndexNow: dist/ missing — skipping.'); process.exit(0); }

// collect URLs from built index.html files
const urls = [];
const walk = (d) => {
  for (const e of readdirSync(d, { withFileTypes: true })) {
    const p = join(d, e.name);
    if (e.isDirectory()) { if (!['admin'].includes(e.name)) walk(p); }
    else if (e.name === 'index.html') {
      const rel = relative(dist, dirname(p)).split(sep).join('/');
      if (rel.includes('thank-you')) continue;
      urls.push(rel ? `${SITE}/${rel}/` : `${SITE}/`);
    }
  }
};
walk(dist);

const payload = { host: new URL(SITE).host, key, keyLocation: `${SITE}/${key}.txt`, urlList: urls };
try {
  const res = await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify(payload),
  });
  console.log(`IndexNow: submitted ${urls.length} URL(s) — HTTP ${res.status}`);
} catch (err) {
  console.log(`IndexNow: ping failed (non-blocking): ${err?.message || err}`);
}
process.exit(0);
