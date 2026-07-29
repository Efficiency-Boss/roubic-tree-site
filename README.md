# Roubic Tree & Landscape — Astro + Netlify + Sveltia CMS

Converted from the Skill 6 approved static site (EB v9, Skill 7). The built `dist/` reproduces the
approved static pixel-for-pixel; the content is a typed collection model (not one `body_html` per page).

## Develop
```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # -> dist/
npm run verify     # build + content/URL audit
```

## Structure
- `src/content/` — typed content collections (`home`, `general`, `services`, `locations`,
  `pages` [LSP], `resources`, `blog`) + `globals/` (`business.json`, `integrations.json`).
  Each page = `{ seo, bodyClass, jsonld[], blocks[] }`. Blocks: typed `faq` / `ctaband`, and a
  per-section `raw` (verbatim HTML) escape hatch for bespoke sections (see `_FIDELITY_REPORT.md`).
- `src/content.config.ts` — Zod schema (fails `astro build` on incomplete content).
- `src/pages/[...slug].astro` — routes every page from `seo.canonicalPath` (LSP files are flat
  `city__service.json`; canonicalPath nests to `/city/service/` so no `__` reaches a URL).
- `src/layouts/Base.astro` + `src/lib/chrome.ts` — head + verbatim site chrome.
- `public/images/` — webp (served) + avif twins. `public/admin/` — Sveltia CMS.

## Deploy
Netlify: build = `npm run build && node scripts/build-redirects.mjs`, publish = `dist`.
CI (`.github/workflows/audit.yml`) builds + audits + walks redirects on every push/PR.
Analytics/GSC/IndexNow are CMS-managed (Site Settings → Integrations). Skill 8 owns launch config.
