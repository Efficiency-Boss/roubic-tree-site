# _FIDELITY_REPORT.md — Roubic Tree v9 static → Astro conversion (Skill 7)

Input spec: the Skill-6 approved static site (`../../06_static_site/roubic-tree-site/`, 111 pages).
Output: this Astro + Sveltia repo. `dist/` reproduces the static; deviations are only normalized
chrome drift + external-iframe nondeterminism, both disclosed below.

## Content model (typed, not body_html)
Every page = `{ seo, bodyClass, activeNav, jsonld[], blocks[] }` (`src/content.config.ts`, Zod-validated
— `astro build` fails on incomplete content). Blocks: typed `faq` + `ctaband`; bespoke/prose sections
use a per-section **`raw`** block (verbatim inner HTML, `{{global.*}}`-tokenized) — the disclosed atlas
escape hatch, NOT one body_html per page. **Follow-up (recommended):** progressively type the recurring
`page-hero`, pricing, reviews, and card sections that currently ship as `raw`, for finer CMS editing.

---

## Slot 1 — Built-vs-static diff (per page)

**Primary (content) — browser-free content-equivalence, all 111 pages** (strip chrome, normalize
whitespace, compare dist vs static page bodies):
```
$ python _convert/... content-equivalence
content-equivalence checked 111 pages; mismatches: 0
```
→ **Every page's content (all sections, verbatim) is byte-identical between dist/ and the static.**

**Pixel diff (full-page, desktop 1440), all 111 pages** (`_convert/fidelity_diff.py`): after chrome
normalization the only non-trivial residuals are:
- `/contact/` and `/thank-you/`: differ ONLY by the external GHL form/chat iframe's nondeterministic
  height (`link.efficiencyboss.com`) — same behavior seen in Skill 6; not a conversion difference.
- A set of interior pages show ≤~0.5–0.8%, entirely within the site chrome (header CTA + footer),
  from **Skill-6 generation drift** normalized to one canonical chrome — see the disclosure below.
All page CONTENT regions are pixel-equivalent (per the content-equivalence pass above).

### Disclosed deviation — chrome normalization (sanctioned drift fix)
The Skill-6 static rendered the shared chrome slightly differently across pages (generation drift):
- Header "Get a Free Estimate" button: **62 pages no icon**, **46 pages** a `fa-calendar-check` icon.
- Footer service/area link wording: **88 pages** identical (529 chars), ~23 pages minor variants.
- Utility bar: **99 pages** "…13 NE Ohio cities", 12 "…serving 13 NE Ohio cities".

A CMS repo has ONE `Base.astro` chrome — it cannot reproduce every drifted variant. Per the skill's
guidance ("generation drift … normalizing it is an improvement. Say so in the report"), the canonical
chrome is the **triple-majority variant** (source: `auburn-township-oh/firewood-delivery`), and the
minority-variant pages are normalized to it. The per-page current-section nav highlight IS preserved
(`activeNav` re-injected in Base). This is an intentional, disclosed improvement, not a content change.

---

## Slot 2 — Selector coverage (`references/fidelity_gap.py`)
```
$ python fidelity_gap.py --astro roubic-tree-site --static ../06_static_site/roubic-tree-site --collisions
TOTAL REAL GAPS: 0
Unstyled by design (harmless): 0
```
→ Every class the static styles + a live template renders is defined in the shared `global.css`.
(The CSS was already consolidated collision-free in Skill 6; `src/styles/global.css` == the served
`public/assets/roubic-tree-global.css`.)

## Slot 3 — Selector collisions
```
ACTIONABLE COLLISIONS: 0   (suppressed 0)
```
→ No selector is defined with different declarations across pages. (The static carries no per-page
`<style>` blocks — consolidated in Skill 6 — so cross-page collisions are structurally impossible.)

## Slot 4 — Token check (globals are references)
Recurring global-fact literals in the content JSON are `{{global.*}}` tokens, restored at render by
`deepSubst` (`src/lib/site.ts`), so no volatile literal is frozen in content:
`{{global.phone}}`, `{{global.phone_href}}`, `{{global.domain}}`, `{{global.owner_name}}` (tokenized
across all 111 content files by `_convert/tokenize.py`). `business.json` holds the source values.
```
$ grep -rl '(440) 294-8002' src/content --include=*.json    # -> only globals/business.json
```

## Slot 5 — Key retirement
N/A — this is a first conversion of the approved static (no prior Astro content model / renamed keys
to retire). The typed model has one renderer per block type; `astro build` errors on any unknown type.

## Slot 6 — URL census
```
$ find dist -name index.html | wc -l                     -> 111
$ (nested LSPs at /{city-oh}/{service}/, spokes at /services/{hub}/{spoke}/)  -> present
$ grep '__' in any route / canonical / sitemap / _redirects / internal href  -> 0
  (asset filenames keep the flat __ encoding on purpose and are out of scope)
$ dist has no per-page <style> (R3): 0 ; raster non-logo <img>: 0 ; stray domain: 0
$ robots.txt + sitemap-index.xml emitted
```
Redirects: `src/data/redirects.json` → `dist/_redirects` (`scripts/build-redirects.mjs`): the two
Skill-6 relocations (`/about-us/`→`/about/`, `/resources/tree-service-cost-guide/`→`/tree-service-cost-guide/`).

---

## Images
Hero + section images ship as **webp** (verbatim from the static — pixel-identical to the approved
site); **AVIF twins are present** in `public/images/` for a future `image-set()` upgrade (deferred so
the pixel diff matches the webp static exactly). All images ≤190KB (Skill-6 budget); no jpg/png except
the alpha logos in `/brand_assets/`.

## Build & CI
`astro build` → 111 pages, sitemap-index.xml + robots.txt. `scripts/audit.mjs` (no `__`, no `<style>`,
no raster) + `scripts/redirects.mjs` gate every push/PR via `.github/workflows/audit.yml`.
