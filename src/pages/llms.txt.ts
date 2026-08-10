import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { subst, globals, fullAddress } from '../lib/site';

// llms.txt (concise) — curated key pages + Key Facts + Contact, per the llms.txt
// standard. The exhaustive page list lives in /llms-full.txt. Derived from the live
// collections + globals so it can never drift from what shipped.

type Item = { title: string; desc: string; path: string };
const clean = (t: string) => subst(t).split(' | ')[0].trim();
const trim = (d: string) => { const s = subst(d); return s.length > 160 ? s.slice(0, 157).trimEnd() + '…' : s; };

export const GET: APIRoute = async ({ site }) => {
  const base = (site?.href || 'https://roubictreeservice.com/').replace(/\/$/, '');
  const g = globals;

  const map = (e: any): Item => ({
    title: clean(e.data.seo.title),
    desc: trim(e.data.seo.description || ''),
    path: '/' + e.data.seo.canonicalPath.replace(/^\/+|\/+$/g, ''),
  });
  const indexable = (e: any) => !e.data.seo?.noindex;

  const services = (await getCollection('services'))
    .filter(indexable)
    .filter((e: any) => /^\/services\/[^/]+\/?$/.test(e.data.seo.canonicalPath))   // hubs only
    .map(map).sort((a, b) => a.path.localeCompare(b.path));
  const resources = (await getCollection('resources')).filter(indexable).map(map);
  const general = (await getCollection('general')).filter(indexable).map(map)
    .filter((i) => /(about|contact|service-areas)/.test(i.path));
  const blogIndex = (await getCollection('blog'))
    .filter((e: any) => e.data.seo.canonicalPath === '/blog/').map(map)[0];

  const line = (i: Item) => `- [${i.title}](${base}${i.path})${i.desc ? ': ' + i.desc : ''}`;
  const section = (h: string, items: Item[]) =>
    items.length ? `## ${h}\n${items.map(line).join('\n')}\n` : '';

  const body = `# ${g.legal_name}

> Family-owned tree service in ${g.address.city}, ${g.address.state} serving ${g.cities_served} Northeast Ohio cities since ${g.founded_year} — removal, trimming, stump grinding, land clearing, storm & emergency response, and firewood delivery.

${section('Services', services)}
${section('Resources', resources)}
${blogIndex ? `## Blog\n${line({ ...blogIndex, desc: '38 tree-care guides — cost breakdowns, seasonal timing, species care, and stump/storm know-how for NE Ohio.' })}\n` : ''}
${section('Company', general)}
## Key Facts
- Family-owned and operated since ${g.founded_year}; owner-operator ${g.owner_name} walks every estimate
- Headquarters: ${fullAddress()} (${g.primary_county} County)
- Serves ${g.cities_served} Northeast Ohio cities within a ${g.radius_miles}-mile radius of ${g.address.city}
- Services: tree removal, tree trimming & pruning, stump grinding, land clearing, storm & emergency response, firewood delivery
- 24/7 live-answer emergency line; free on-site estimates; ${g.review_rating.toFixed(1)}★ across ${g.review_count} reviews

## Contact
- Website: ${base}/
- Phone: ${g.phone}
- Address: ${fullAddress()}
- Full page index: ${base}/llms-full.txt
`;

  return new Response(body.replace(/\n{3,}/g, '\n\n').trimEnd() + '\n', {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
