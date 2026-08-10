import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { subst, globals, fullAddress } from '../lib/site';

// llms-full.txt — the comprehensive AI/answer-engine index: every indexable page,
// grouped by section. Derived from the same routed collections + globals as the
// sitemap, so it can never drift from what shipped. Concise variant: /llms.txt.

type Item = { title: string; desc: string; path: string };
const clean = (t: string) => subst(t).split(' | ')[0].trim();
const trim = (d: string) => { const s = subst(d); return s.length > 170 ? s.slice(0, 167).trimEnd() + '…' : s; };

export const GET: APIRoute = async ({ site }) => {
  const base = (site?.href || 'https://roubictreeservice.com/').replace(/\/$/, '');
  const g = globals;

  const grab = async (name: string): Promise<Item[]> => {
    const entries = await getCollection(name as any);
    return entries
      .filter((e: any) => !e.data.seo?.noindex)
      .map((e: any) => ({
        title: clean(e.data.seo.title),
        desc: trim(e.data.seo.description || ''),
        path: '/' + e.data.seo.canonicalPath.replace(/^\/+|\/+$/g, ''),
      }))
      .sort((a: Item, b: Item) => a.path.localeCompare(b.path));
  };

  const [services, locations, lsps, resources, blog, general] = await Promise.all(
    ['services', 'locations', 'pages', 'resources', 'blog', 'general'].map(grab)
  );

  const section = (heading: string, items: Item[]) =>
    items.length
      ? `## ${heading}\n` + items.map((i) => `- [${i.title}](${base}${i.path})${i.desc ? ': ' + i.desc : ''}`).join('\n') + '\n'
      : '';

  const body = `# ${g.legal_name} — Full Site Index

> Family-owned tree service in ${g.address.city}, ${g.address.state} serving ${g.cities_served} Northeast Ohio cities since ${g.founded_year}. Complete page index for AI systems. Concise summary: ${base}/llms.txt

Contact: ${g.phone} · ${fullAddress()} · free estimates within ${g.radius_miles} miles · 24/7 emergency line.

${section('Services', services)}
${section('Service Areas', locations)}
${section('Local Service Pages', lsps)}
${section('Resources', resources)}
${section('Blog', blog)}
${section('Company & Info', general)}`;

  return new Response(body.replace(/\n{3,}/g, '\n\n').trimEnd() + '\n', {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
