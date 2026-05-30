# 12 — Pages Structure (v2)

## Global Layout

Every page includes:
- `Header` (logo, nav, cart link with count)
- `Footer`
- `CheckoutPopup` (global — opened from Cart page)
- `DeferredPixels`

**Not in v2:** CartDrawer · UpsellModal · About in nav · Quiz · Subscriptions · WhatsApp · SMS

---

## Site Map

| Route | Page |
|-------|------|
| `/` | Home |
| `/collection` | Collection |
| `/products/freshguard` | PDP |
| `/products/heatshield` | PDP |
| `/products/underguard` | PDP |
| `/cart` | **Cart** |
| `/contact` | Contact |
| `/legal/terms` | Terms |
| `/legal/privacy` | Privacy |
| `/legal/returns` | Returns |
| `/thank-you/[orderId]` | Thank You |

---

## Homepage `/`

| # | Section |
|---|---------|
| 1 | Hero — brand + CTA → collection |
| 2 | Trust bar |
| 3 | 3 product cards |
| 4 | Why Safra Skin |
| 5 | Social proof |
| 6 | FAQ |
| 7 | Final CTA |

---

## Collection `/collection`

| Block | Content |
|-------|---------|
| H1 | مجموعة الثقة الكاملة |
| Bundle CTA | Add all 3 → `/cart` |
| Product grid | Each card: **أضيف للسلة** → `/cart` |
| Trust badges | |

---

## Product PDP `/products/[slug]`

| # | Section |
|---|---------|
| 1 | Hero — stars, H1, offer selector, CTA → add + `/cart` |
| 2–N | Alternating content sections |
| N+1 | **CrossSellSection** — bottom of page |
| | Trust badges |

---

## Cart `/cart`

| Block | Content |
|-------|---------|
| Items list | Remove · qty · image |
| Total | Tier pricing + savings |
| Cross-sells | Products not in cart @ 199 |
| Trust | COD · discreet · guarantee |
| CTA | Opens Checkout Popup |

---

## Contact `/contact`

| Field | Detail |
|-------|--------|
| Email | support@safraskin.online |
| Hours | Sun–Thu 9am–6pm Riyadh |
| Form | Name · Phone · Message (optional v1: mailto) |

**No WhatsApp.**

---

## Thank You `/thank-you/[orderId]`

See [08-checkout-funnel-cro.md](./08-checkout-funnel-cro.md) — CRO blocks + cross-sells.

---

## Legal Pages

| Page | Path |
|------|------|
| Terms | `/legal/terms` |
| Privacy | `/legal/privacy` |
| Returns | `/legal/returns` |

---

## Navigation

| Label (AR) | URL |
|------------|-----|
| الرئيسية | `/` |
| المجموعة | `/collection` |
| السلة | `/cart` |
| تواصل | `/contact` |

Footer: products + legal links.

---

## Mobile

Hamburger → same links + cart count badge.
