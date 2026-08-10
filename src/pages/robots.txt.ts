import type { APIRoute } from 'astro';

// Max AI-visibility robots.txt (GEO). Every Tier-1/2 answer-engine crawler is
// explicitly allowed; only the aggressive, low-value Bytespider is blocked.
// CMS admin + thank-you are kept out of the index. Sitemap points AI/search
// crawlers at the full URL set.
const ALLOW = [
  'GPTBot', 'OAI-SearchBot', 'ChatGPT-User',        // OpenAI (ChatGPT search + browsing)
  'ClaudeBot', 'anthropic-ai',                       // Anthropic (Claude)
  'PerplexityBot',                                   // Perplexity (referral traffic)
  'Google-Extended', 'GoogleOther',                  // Google (Gemini / AI Overviews)
  'Applebot-Extended',                               // Apple Intelligence
  'Amazonbot',                                       // Alexa / Amazon AI
  'FacebookBot',                                     // Meta AI
];

export const GET: APIRoute = ({ site }) => {
  const base = (site?.href || 'https://roubictreeservice.com/').replace(/\/$/, '');
  const allowBlocks = ALLOW.map((ua) => `User-agent: ${ua}\nAllow: /`).join('\n\n');
  const body = `User-agent: *
Allow: /
Disallow: /admin/
Disallow: /thank-you/

# AI / answer-engine crawlers — explicitly welcome (GEO)
${allowBlocks}

# Aggressive, low-value crawler — blocked
User-agent: Bytespider
Disallow: /

Sitemap: ${base}/sitemap-index.xml
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain' } });
};
