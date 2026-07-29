// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// `site` drives canonical URLs + the sitemap. Netlify injects URL / DEPLOY_PRIME_URL
// at build time; prefer an explicit SITE_URL env, then Netlify's URL, then production.
const SITE_URL =
  process.env.SITE_URL || process.env.URL || 'https://roubictree.com';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/admin/') && !page.includes('/thank-you/'),
    }),
  ],
});
