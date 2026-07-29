import type { APIRoute, GetStaticPaths } from 'astro';
import integrations from '../content/globals/integrations.json';

// Serves the IndexNow key file at /<key>.txt when a key is configured in the CMS.
// Empty key => no route generated.
export const getStaticPaths: GetStaticPaths = () => {
  const key = (integrations.indexnow_key ?? '').trim();
  return key ? [{ params: { indexnow: key } }] : [];
};

export const GET: APIRoute = ({ params }) =>
  new Response(String(params.indexnow), { headers: { 'Content-Type': 'text/plain' } });
