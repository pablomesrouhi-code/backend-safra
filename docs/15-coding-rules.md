# 15 — Coding Rules

## General

1. **TypeScript strict** on frontend — no `any` except third-party gaps.
2. **Python type hints** on all backend functions.
3. **Arabic RTL first** — test every component in RTL.
4. **Mobile first** — design for 390px width minimum.
5. **Cart page at `/cart`** — no cart drawer.
6. **No `/checkout` page** — popup only.
6. **Server validates prices** — frontend display is never authoritative.
7. **event_id** on all purchase-related pixel events.
8. **No secrets in frontend** — CAPI tokens backend only.

## Frontend Conventions (Keep It Simple)

```
app/          → pages (App Router)
components/   → PascalCase, one file per UI block (Header.tsx, CartDrawer.tsx)
context/      → CartContext.tsx only
data/         → products.ts — all product copy + prices in ONE file
lib/          → small utils (pricing, phone, pixels)
```

- **Cart:** React Context — NOT Zustand, NOT Redux
- **Stack:** Next 14 · React 18 · Tailwind 3.4 — NOT v15/v19/v4
- **No `src/` folder** — flat `frontend/app/` at root
- `'use client'` only on: CartContext, drawer, popups, forms, pixels
- Product content lives in `data/products.ts` — not scattered, not API-fetched v1
- Plain `fetch()` to backend — no axios
- Images: `<img>` or `next/image` with SVG placeholders

## Backend Conventions

- Routes in `api/routes/` — thin handlers
- Business logic in `services/`
- Pydantic schemas for all request/response
- Async routes where DB/HTTP async
- Log order creation + CAPI response status (not PII in logs)

## Git Commits

```
feat(frontend): add cart drawer cross-sells
fix(backend): meta phone hash normalization
docs: update pricing tier logic
```

## Error Handling

- Frontend: toast on API error with Arabic message
- Backend: HTTP 422 validation · 400 price mismatch · 429 rate limit

## Testing Minimum

- `pricing.test.ts` — tier 1/2/3 + upsell
- `phone.test.ts` — KSA formats
- `hashing.test.py` — Meta vs TikTok phone hash
- `upsell.test.ts` — selection logic

## Performance

- Lazy load checkout popup and upsell modal
- Defer pixels — see [09-tracking-pixels.md](./09-tracking-pixels.md)
- No heavy carousel libraries
- SVG placeholders — not large PNG

## Accessibility

- `aria-label` on cart icon, close buttons
- Focus trap in modals
- Color contrast WCAG AA minimum

## Do Not

- Add Stripe/payment gateway v1
- Add `/checkout` page route
- Add upsell modal · WhatsApp · SMS · quiz · subscriptions
- Use before/after body images
- Claim medical cures in copy
