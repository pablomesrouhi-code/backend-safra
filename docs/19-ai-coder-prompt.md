# 19 — AI Coder Master Prompt

Copy everything below the line and paste to your AI coder to start building.

---

## PROMPT START

You are building **Safra Skin (سفرا جلد)** — a premium DTC e-commerce store for KSA women. Arabic RTL, COD-only, high-AOV funnel optimized for Snapchat/TikTok traffic.

### Your Mission

Build a complete production-ready codebase with two folders:

```
/
├── frontend/     # Next.js 14 + React 18 + Tailwind 3.4 (simple, familiar)
├── backend/      # Python FastAPI + SQLAlchemy + Alembic
└── docs/         # READ ALL SPECS BEFORE CODING
```

**Do not guess.** Follow every spec in `docs/`. Start with `docs/00-INDEX.md`.

### Documentation (Read in Order)

| Priority | File | What to implement |
|----------|------|-------------------|
| 1 | `docs/00-INDEX.md` | Overview + build order |
| 2 | `docs/01-architecture.md` | Monorepo structure, API contracts |
| 3 | `docs/07-database-schema.md` | Postgres schema + Alembic |
| 4 | `docs/06-backend-spec.md` | FastAPI routes, services, CAPI |
| 5 | `docs/04-design-system.md` | Colors, fonts, header, footer |
| 6 | `docs/05-frontend-spec.md` | Next.js setup, libraries, components |
| 7 | `docs/02-brand-positioning.md` | Brand voice, authority, trust |
| 8 | `docs/03-icp-messaging.md` | KSA women ICP, emotional hooks |
| 9 | `docs/10-copy-guidelines-ksa-dialect.md` | Saudi dialect copy rules |
| 10 | `docs/11-product-pages-spec.md` | 3 PDP sections + copy |
| 11 | `docs/12-pages-structure.md` | Home, Collection, About, Contact |
| 12 | `docs/08-checkout-funnel-cro.md` | Cart drawer, checkout popup, upsell |
| 13 | `docs/17-products-catalog.md` | SKUs, pricing, cross-sell matrix |
| 14 | `docs/09-tracking-pixels.md` | Deferred web pixels + CAPI dedup |
| 15 | `docs/16-google-sheets-integration.md` | Order → Sheet webhook |
| 16 | `docs/13-deployment-docker.md` | Docker + Easypanel deploy |
| 17 | `docs/14-env-variables.md` | All env vars |
| 18 | `docs/15-coding-rules.md` | Code standards |
| 19 | `docs/18-placeholder-images.md` | SVG placeholders |

**Assets to copy into project:**

- `docs/env/frontend.env.example` → `frontend/.env.example`
- `docs/env/backend.env.example` → `backend/.env.example`
- `docs/sheets/google-apps-script.js` → deploy separately to Google Sheet
- `docs/sheets/order-template.csv` → import as Sheet headers

### Brand & Domain (Locked)

| Field | Value |
|-------|-------|
| Arabic brand | **سفرا جلد** |
| English brand | **Safra Skin** |
| Frontend | `https://safraskin.online` |
| Backend API | `https://api.safraskin.online` |
| Database | PostgreSQL `safraskin` |
| Payment | **COD only** |

### Header (RTL)

Right side: circle with **S** in sage `#2D6A5A` → text logo **سفرا جلد** + **Safra Skin** below → menu → cart icon.

### Products (Locked)

| Slug | Arabic Name | SKU |
|------|-------------|-----|
| `freshguard` | فريش‌گارد — بروتوكول النفس الواثق من الداخل | SS-FRESHGUARD-01 |
| `heatshield` | هيت‌شield — بودرة درع الحر للجسم | SS-HEATSHIELD-02 |
| `underguard` | أندر‌گارد — نظام ثقة الإبط الطبيعي | SS-UNDERGUARD-03 |

### Pricing (Locked — Backend Must Recalculate)

| Offer | Price SAR |
|-------|-----------|
| 1 piece | 199 |
| 2 pieces | 279 |
| 3 pieces | 349 |
### Funnel (v2 — Locked)

1. **PDP / Collection:** CTA → add to cart → redirect **`/cart`**
2. **PDP bottom:** Cross-sells always visible
3. **Cart page:** Items + cross-sells + CTA → **checkout popup**
4. **Checkout popup:** Summary + name + phone (starts with 0, example below) → submit
5. Backend → Google Sheet webhook
6. **Thank You page:** CRO for confirmation/delivery + cross-sells for new order

**No:** cart drawer · upsell modal · WhatsApp · SMS · quiz · subscriptions · About page

### Pages Required

- `/` — Home
- `/collection` — Collection
- `/products/[slug]` — 3 PDPs
- `/cart` — **Cart page**
- `/contact` — Contact
- `/thank-you/[orderId]` — Thank You (CRO optimized)
- Legal: `/legal/terms`, `/legal/privacy`, `/legal/returns`

**Checkout = popup only** (not a route).

### Tracking

- Meta, TikTok, Snapchat **web pixels — deferred** (requestIdleCallback)
- **CAPI from backend** with SHA256 hashing
- **event_id** dedup between browser and server
- Meta/Snap phone hash: digits only, no `+` (e.g. `966501234567`)
- TikTok phone hash: E.164 **with** `+` (e.g. `+966501234567`)
- See `docs/09-tracking-pixels.md` for full payloads

### Backend Requirements

- FastAPI with `/api/v1/orders` POST endpoint
- **Alembic migrations run on container startup**
- Price validation server-side — never trust client totals
- CAPI fire-and-forget async after order save
- Google Sheets sync via webhook (see `docs/sheets/google-apps-script.js`)
- CORS for `safraskin.online`

### Frontend Requirements (Keep It Simple)

- **Next.js 14** App Router · **React 18** · **Tailwind CSS 3.4**
- **React Context** for cart (`context/CartContext.tsx`) — NOT Zustand
- **No `src/` folder** — flat `app/`, `components/`, `data/`, `lib/`
- **One file** `data/products.ts` for all product copy + prices
- React Hook Form + Zod for checkout
- Plain `fetch()` to backend API
- Full RTL Arabic (`dir="rtl"`, `lang="ar"`)
- Responsive mobile-first
- Alternating section layout (text/image flip per section)
- SVG placeholder images until real assets
- All copy in Saudi dialect per `docs/10-copy-guidelines-ksa-dialect.md`
- Read `docs/05-frontend-spec.md` — follow the simple mental model

### Docker & Deploy

- `frontend/Dockerfile` + `backend/Dockerfile`
- `docker-compose.yml` for local dev
- `.env.example` in each folder (from docs/env/)
- Ready for Easypanel GitHub deploy
- Backend startup: `alembic upgrade head && uvicorn ...`

### Database

Internal URL (Easypanel):
```
postgres://postgres:s4eagoems3oueizu0h00@safraskin_database:5432/safraskin?sslmode=disable
```

Schema in `docs/07-database-schema.md`.

### Deliverables Checklist

- [ ] `frontend/` — complete Next.js app
- [ ] `backend/` — complete FastAPI app
- [ ] Docker files for both
- [ ] `.env.example` files
- [ ] Alembic migrations
- [ ] Placeholder SVG images in `frontend/public/placeholders/`
- [ ] All pages with real Arabic copy (not lorem ipsum)
- [ ] Cart **page** + checkout popup + thank you (no drawer, no upsell modal)
- [ ] Pixels deferred + CAPI with dedup
- [ ] Google Sheet webhook integration
- [ ] KSA phone validation
- [ ] README in each folder with setup instructions

### What NOT to Do

- No payment gateway (COD only)
- No checkout page route (popup only)
- No upsell modal · WhatsApp · SMS · quiz · subscriptions
- No medical cure claims in copy
- No secrets in frontend env
- No Zustand / Redux / over-engineered state

Build the full codebase now. Start with architecture and database, then backend API, then frontend. Test the complete order flow locally with docker-compose.

## PROMPT END
