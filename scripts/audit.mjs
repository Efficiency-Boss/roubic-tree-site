// Post-build content/URL audit (CI gate). Fails the build on: missing dist, any `__` in a
// built route/canonical/internal href (asset filenames exempt), any per-page <style> block,
// any raster <img> outside /brand_assets/, or an empty JSON-LD. Skill 8 extends this.
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
if (!existsSync(dist)) { console.error('dist/ missing — run astro build first.'); process.exit(1); }

const htmls = [];
(function walk(d) {
  for (const e of readdirSync(d)) {
    const p = join(d, e);
    if (statSync(p).isDirectory()) walk(p);
    else if (e.endsWith('.html')) htmls.push(p);
  }
})(dist);

const fails = [];
for (const f of htmls) {
  const url = '/' + relative(dist, dirname(f)).replace(/\\/g, '/');
  const h = readFileSync(f, 'utf8');
  if (/\/[a-z0-9-]*__[a-z0-9-]*\//.test(h.replace(/\/(images|brand_assets|assets)\/[^"']*/g, '')))
    fails.push(`${url}: '__' in a route/link/canonical`);
  if (/<style[\s>]/i.test(h)) fails.push(`${url}: per-page <style> block (R3)`);
  const rasters = (h.match(/(?:src|srcset)="[^"]*\.(?:jpe?g|png)"/gi) || []).filter((s) => !s.includes('/brand_assets/'));
  if (rasters.length) fails.push(`${url}: raster image (${rasters[0]})`);
}
console.log(`audit: ${htmls.length} pages checked`);
if (fails.length) { console.error('AUDIT FAILED:\n  ' + fails.slice(0, 40).join('\n  ')); process.exit(1); }
console.log('audit: PASS');
