import { z } from 'astro:content';
import businessData from '../content/globals/business.json';

/** Global business facts — the ONE place NAP / review data / founding live. Parsed with zod at
 * import time so a bad business.json fails `astro build`. Content references `{{global.*}}`;
 * deepSubst() substitutes at render time so the JSON never carries a volatile literal. */
const globalsSchema = z.object({
  business_name: z.string().min(1),
  legal_name: z.string().min(1),
  phone: z.string().min(1),
  phone_href: z.string().min(1),
  review_rating: z.number(),
  review_count: z.number().int(),
  pricing_year: z.string().min(1),
  owner_name: z.string().min(1),
  founded_year: z.number().int(),
  radius_miles: z.number().int(),
  primary_county: z.string().min(1),
  tagline: z.string().min(1),
  domain: z.string().min(1),
  address: z.object({
    street: z.string().min(1), city: z.string().min(1),
    state: z.string().min(1), zip: z.string().min(1),
  }),
  cities_served: z.number().int(),
});
export const globals = globalsSchema.parse(businessData);
export type Globals = typeof globals;

export function phoneHref(phone: string = globals.phone): string {
  return globals.phone_href || `tel:+1${phone.replace(/\D/g, '')}`;
}
export function fullAddress(): string {
  const a = globals.address;
  return `${a.street}, ${a.city}, ${a.state} ${a.zip}`;
}

const TOKENS: Record<string, () => string> = {
  '{{global.business_name}}': () => globals.business_name,
  '{{global.legal_name}}': () => globals.legal_name,
  '{{global.phone}}': () => globals.phone,
  '{{global.phone_href}}': () => phoneHref(),
  '{{global.review_rating}}': () => String(globals.review_rating),
  '{{global.review_count}}': () => String(globals.review_count),
  '{{global.pricing_year}}': () => globals.pricing_year,
  '{{global.owner_name}}': () => globals.owner_name,
  '{{global.founded_year}}': () => String(globals.founded_year),
  '{{global.radius_miles}}': () => String(globals.radius_miles),
  '{{global.county}}': () => globals.primary_county,
  '{{global.city}}': () => globals.address.city,
  '{{global.state}}': () => globals.address.state,
  '{{global.zip}}': () => globals.address.zip,
  '{{global.street}}': () => globals.address.street,
  '{{global.address}}': () => fullAddress(),
  '{{global.tagline}}': () => globals.tagline,
  '{{global.domain}}': () => globals.domain,
  '{{global.cities_served}}': () => String(globals.cities_served),
};
export function subst(text: string): string {
  let out = text;
  for (const [t, v] of Object.entries(TOKENS)) out = out.split(t).join(v());
  return out;
}
export function deepSubst<T>(value: T): T {
  if (typeof value === 'string') return subst(value) as unknown as T;
  if (Array.isArray(value)) return value.map((v) => deepSubst(v)) as unknown as T;
  if (value && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const k of Object.keys(value as Record<string, unknown>))
      out[k] = deepSubst((value as Record<string, unknown>)[k]);
    return out as unknown as T;
  }
  return value;
}
