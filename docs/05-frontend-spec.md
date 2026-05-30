# 05 — Frontend Specification (Simple & Familiar)

> **Philosophy:** Classic Next.js e-commerce. No over-engineering.  
> One cart context, normal pages, Tailwind classes, fetch to API. That's it.

---

## Stack (Simple — What You're Used To)

| Package | Version | Why |
|---------|---------|-----|
| `next` | **14.x** | Stable App Router — familiar docs |
| `react` | **18.x** | Standard |
| `tailwindcss` | **3.4.x** | Classic config — `@tailwind base/components/utilities` |
| `react-hook-form` | 7.x | Checkout form |
| `zod` | 3.x | Phone validation |
| `lucide-react` | latest | Icons |
| `clsx` | latest | className helper |

**Do NOT add:** Zustand, Redux, MUI, Bootstrap, shadcn (unless you want — optional), React 19, Tailwind v4.

**Cart state:** `React Context` + `useReducer` — one `CartProvider` in `layout.tsx`. Everyone knows this pattern.

---

## Folder Structure (Flat — Easy to Navigate)

```
frontend/
├── app/
│   ├── layout.tsx              # RTL + CartProvider + Header + Footer
│   ├── page.tsx                  # Home
│   ├── globals.css               # Tailwind imports
│   ├── collection/page.tsx
│   ├── about/page.tsx
│   ├── contact/page.tsx
│   ├── products/[slug]/page.tsx
│   └── thank-you/[orderId]/page.tsx
├── components/
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── CartDrawer.tsx            # drawer + cross-sells
│   ├── CheckoutPopup.tsx         # name + phone form
│   ├── UpsellModal.tsx           # 99 SAR timer
│   ├── OfferSelector.tsx         # 199 / 279 / 349
│   ├── ProductCard.tsx
│   ├── TrustBadges.tsx
│   └── DeferredPixels.tsx
├── context/
│   └── CartContext.tsx           # ALL cart logic here
├── data/
│   └── products.ts               # products, prices, copy — one file
├── lib/
│   ├── pricing.ts
│   ├── phone.ts
│   ├── upsell.ts
│   └── pixels.ts
├── public/
│   └── placeholders/             # SVG until real images
├── tailwind.config.ts
├── next.config.js
├── package.json
├── Dockerfile
└── .env.example
```

**No `src/` folder. No 15 subfolders. One file per big UI piece.**

---

## Mental Model (Read This First)

```
User on PDP / Collection
  → picks offer → CTA → add to cart → /cart
  → cross-sells on cart + PDP bottom
  → "إتمام الطلب" → Checkout Popup
  → name + phone (05...) → Google Sheet → Thank You
```

**Cart = page `/cart`. Checkout = popup. No drawer. No upsell modal.**

---

## CartContext (Instead of Zustand)

```tsx
// context/CartContext.tsx
'use client';

import { createContext, useContext, useReducer, ReactNode } from 'react';

type CartItem = { slug: string; qty: number; sku: string };

type State = {
  items: CartItem[];
  isDrawerOpen: boolean;
  isCheckoutOpen: boolean;
  isUpsellOpen: boolean;
};

type Action =
  | { type: 'ADD'; slug: string; qty: number; sku: string }
  | { type: 'REMOVE'; slug: string }
  | { type: 'OPEN_DRAWER' }
  | { type: 'CLOSE_DRAWER' }
  | { type: 'OPEN_CHECKOUT' }
  | { type: 'OPEN_UPSELL' }
  | { type: 'CLOSE_ALL' };

const CartContext = createContext(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  // expose: addToCart, openDrawer, getTotal, etc.
  return (
    <CartContext.Provider value={{ state, dispatch, ...actions }}>
      {children}
      <CartDrawer />
      <CheckoutPopup />
      <UpsellModal />
    </CartContext.Provider>
  );
}

export const useCart = () => useContext(CartContext);
```

Mount `<CartProvider>` once in `app/layout.tsx`. Drawers/modals live inside provider — always available.

---

## Product Data — One File

```typescript
// data/products.ts — single source, easy to edit
export const PRODUCTS = [
  {
    slug: 'freshguard',
    sku: 'SS-FRESHGUARD-01',
    nameAr: 'فريش‌گارد — بروتوكول النفس الواثق من الداخل',
    nameEn: 'FreshGuard™',
    price: 199,
    // hero copy, sections, ingredients, reviews — all here
  },
  // heatshield, underguard...
];

export const TIERS = { 1: 199, 2: 279, 3: 349 } as const;
export const UPSELL_PRICE = 99;
```

Pages import from `data/products.ts`. No CMS v1. No API fetch for product content on first load (static = fast).

---

## Pages — Normal Next.js

| Route | File | Type |
|-------|------|------|
| `/` | `app/page.tsx` | Server Component |
| `/collection` | `app/collection/page.tsx` | Server Component |
| `/products/[slug]` | `app/products/[slug]/page.tsx` | Server Component + client OfferSelector |
| `/about` | `app/about/page.tsx` | Server Component |
| `/contact` | `app/contact/page.tsx` | Server Component |
| `/thank-you/[orderId]` | `app/thank-you/[orderId]/page.tsx` | Server Component |

**Client Components (`'use client'`) only for:**
- CartContext + drawer + popups
- OfferSelector + StickyATC
- Checkout form
- DeferredPixels

Everything else = server component. Simple rule.

---

## Pricing

```typescript
// lib/pricing.ts
export function getTierTotal(count: number): number {
  if (count === 1) return 199;
  if (count === 2) return 279;
  if (count === 3) return 349;
  return 199 * count;
}
```

Backend recalculates on submit — frontend is display only.

---

## Phone Validation

```typescript
// lib/phone.ts
// Accept: 05xxxxxxxx, 5xxxxxxxx, +9665xxxxxxxx
// Send to backend as: +9665XXXXXXXX
export function isValidKsaPhone(v: string): boolean;
export function toE164(v: string): string;
```

---

## API — Plain fetch

```typescript
// No axios, no fancy client
const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/orders`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload),
});
if (!res.ok) throw new Error('فشل الطلب');
return res.json();
```

---

## Tailwind Config (v3 — Classic)

```javascript
// tailwind.config.ts
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        sage: '#2D6A5A',
        gold: '#C4A265',
        cream: '#FAF7F2',
      },
      fontFamily: {
        arabic: ['IBM Plex Sans Arabic', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

html { direction: rtl; }
body { @apply bg-cream text-gray-900 font-arabic; }
```

---

## Layout

```tsx
// app/layout.tsx
import { CartProvider } from '@/context/CartContext';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import DeferredPixels from '@/components/DeferredPixels';

export default function RootLayout({ children }) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <CartProvider>
          <Header />
          <main>{children}</main>
          <Footer />
          <DeferredPixels />
        </CartProvider>
      </body>
    </html>
  );
}
```

---

## Product Page Pattern

Each PDP = map over section array from `data/products.ts`:

```tsx
// app/products/[slug]/page.tsx
import { getProduct } from '@/data/products';
import OfferSelector from '@/components/OfferSelector';

export default function ProductPage({ params }) {
  const product = getProduct(params.slug);
  return (
    <>
      <section className="grid md:grid-cols-2 gap-8">
        <img src={product.image} alt={product.nameAr} />
        <div>
          <h1>{product.nameAr}</h1>
          <OfferSelector slug={product.slug} />
        </div>
      </section>
      {product.sections.map((s, i) => (
        <section key={i} className={i % 2 ? 'md:flex-row-reverse' : ''}>
          {/* text + image alternating */}
        </section>
      ))}
    </>
  );
}
```

---

## Docker (Simple)

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_SITE_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_SITE_URL=$NEXT_PUBLIC_SITE_URL
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

```javascript
// next.config.js
module.exports = {
  output: 'standalone',
  images: { domains: ['safraskin.online'] },
};
```

---

## What NOT to Do

- No Zustand / Redux
- No `src/` nesting
- No 20 component subfolders
- No React 19 / Next 15 / Tailwind 4 (unless you know them well)
- No separate `/cart` or `/checkout` routes
- No fetching product copy from API on every page load

---

## SEO

- `metadata` export per page in Arabic
- `lang="ar"` · `dir="rtl"` on `<html>`
- OG tags on product pages

See also: [04-design-system.md](./04-design-system.md) · [08-checkout-funnel-cro.md](./08-checkout-funnel-cro.md)
