import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/* ============================================================================
   Typed content model (v9 — typed per-field, NOT one body_html per page).
   Every page: { seo, bodyClass, blocks[] }. `blocks` is an ordered, typed array;
   composition is data. High-value universal structures (page-hero, faq, cta-band)
   are fully typed and CMS-editable. Bespoke / prose sections carry a per-section
   `raw` block (verbatim inner HTML, {{global.*}}-tokenized) — the disclosed escape
   hatch (atlas pattern; see _FIDELITY_REPORT.md). Renderers emit the approved
   static's exact section classes so dist/ matches the static pixel-for-pixel.
   ========================================================================== */

const cta = z.object({
  cls: z.string().default('btn btn-primary'),
  label: z.string(),
  href: z.string(),
  shine: z.boolean().default(false),
  icon: z.string().optional(),          // fa icon class, rendered AFTER label unless icon_before
  icon_before: z.boolean().default(false),
  label_span: z.boolean().default(false), // wrap label + icon in separate <span>s (btn-primary-inv style)
});

const crumb = z.object({ label: z.string(), href: z.string().optional() });

const heroChip = z.object({
  cls: z.string().default('hero-chip'),   // e.g. "hero-chip gold"
  icon: z.string().optional(),
  lbl: z.string().optional(),
  val: z.string(),
});

const faqBlock = z.object({
  type: z.literal('faq'),
  section_class: z.string().default('faq'),
  name: z.string().default('faq'),        // <details name> group
  eyebrow: z.string().optional(),
  h2: z.string(),
  intro: z.string().optional(),
  items: z.array(z.object({ q: z.string(), a_html: z.string() })),
});

const ctabandBlock = z.object({
  type: z.literal('ctaband'),
  section_class: z.string().default('cta-band'),
  section_id: z.string().optional(),
  h2: z.string(),
  p: z.string().optional(),
  ctas: z.array(cta).default([]),
});

const rawBlock = z.object({
  type: z.literal('raw'),
  html: z.string(),                        // verbatim <section>…</section>, tokenized
});

const block = z.discriminatedUnion('type', [faqBlock, ctabandBlock, rawBlock]);
export type Block = z.infer<typeof block>;

const pageSchema = z.object({
  seo: z.object({
    title: z.string(),
    description: z.string(),
    canonicalPath: z.string(),
    ogType: z.string().default('website'),
    noindex: z.boolean().default(false),
    ogImage: z.string().optional(),
  }),
  bodyClass: z.string(),                    // pt-{type} — drives the scoped CSS
  activeNav: z.string().nullable().default(null),  // desktop-nav href to highlight (current section)
  jsonld: z.array(z.string()).default([]),  // raw per-page JSON-LD script bodies (tokenized)
  blocks: z.array(block),
});

const mk = (dir: string) => defineCollection({
  loader: glob({ pattern: '**/*.json', base: `./src/content/${dir}` }),
  schema: pageSchema,
});

export const collections = {
  home: mk('home'),
  general: mk('general'),
  services: mk('services'),      // hubs + spokes (nested filenames)
  locations: mk('locations'),    // city hubs + service-areas index
  pages: mk('pages'),            // LSP: flat city__service filenames -> nested canonicalPath
  resources: mk('resources'),
  blog: mk('blog'),
};
