// Compile the CMS-managed redirect list (src/data/redirects.json) into dist/_redirects.
// Run after `astro build` (netlify.toml build command + CI).
import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(root, 'src', 'data', 'redirects.json');
const distDir = join(root, 'dist');
const out = join(distDir, '_redirects');

if (!existsSync(distDir)) { console.error('dist/ not found — run astro build first.'); process.exit(1); }
const rows = JSON.parse(readFileSync(src, 'utf8'));
const lines = rows.map((r) => `${r.from}  ${r.to}  ${r.status || 301}`);
// Astro serves pretty URLs directly; these are only the CMS-managed 301s.
const body = lines.join('\n') + (lines.length ? '\n' : '');
// Append (don't clobber) in case a static public/_redirects was emitted.
if (existsSync(out)) appendFileSync(out, body); else writeFileSync(out, body);
console.log(`build-redirects: wrote ${lines.length} redirect(s) to dist/_redirects`);
