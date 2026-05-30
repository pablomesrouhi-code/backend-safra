# 01 — System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│  safraskin.online (Next.js 14 · RTL Arabic)                  │
│  Cart Drawer · Checkout Popup · Pixels (deferred)           │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  api.safraskin.online (FastAPI · Python 3.12)                 │
│  Orders · Events (CAPI) · Webhook → Google Sheets           │
└──────────┬─────────────────────────────┬────────────────────┘
           │                             │
           ▼                             ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│  PostgreSQL          │    │  Google Sheets (Apps Script) │
│  safraskin           │    │  Order backup + ops view       │
└──────────────────────┘    └──────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Meta / TikTok /     │
│  Snapchat CAPI       │
└──────────────────────┘
```

## Repository Structure

```
/
├── docs/                    ← This documentation
├── frontend/                ← Next.js 14 App Router (no src/)
│   ├── Dockerfile
│   ├── .env.example
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── app/                 ← Pages
│   ├── components/          ← Flat — Header, CartDrawer, etc.
│   ├── context/             ← CartContext (React Context)
│   ├── data/                ← products.ts — all copy + prices
│   ├── lib/                 ← pricing, phone, pixels
│   └── public/placeholders/
├── backend/                 ← FastAPI
│   ├── Dockerfile
│   ├── .env.example
│   ├── requirements.txt
│   ├── alembic/
│   └── app/
│       ├── main.py
│       ├── api/routes/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       │   ├── orders.py
│       │   ├── sheets.py
│       │   └── capi/        ← Meta, TikTok, Snap
│       └── core/            ← config, db, migrations
└── README.md
```

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| **Frontend** | Next.js 14 (App Router) | Stable, familiar, Easypanel |
| **UI** | React 18 + Tailwind CSS 3.4 | Classic setup everyone knows |
| **State** | React Context + useReducer | Cart drawer — no extra libs |
| **Forms** | React Hook Form + Zod | KSA phone validation |
| **Fonts** | `next/font` — IBM Plex Sans Arabic + Inter | Premium Arabic |
| **Backend** | FastAPI 0.115+ | Async, OpenAPI, CAPI webhooks |
| **ORM** | SQLAlchemy 2 + Alembic | Migrations on startup |
| **DB** | PostgreSQL 16 | Easypanel existing |
| **HTTP client** | httpx | CAPI + Sheets webhook |

## Key Architectural Rules

1. **No `/cart` page** — Cart Drawer only.
2. **No separate checkout page** — Checkout Popup from drawer.
3. **COD only** — no payment gateway v1.
4. **All prices computed server-side** on order submit (never trust client totals).
5. **CAPI fired from backend** on `Purchase` with hashed PII.
6. **Web pixels deferred** — load after `requestIdleCallback` or interaction.
7. **Event dedup** — shared `event_id` (UUID) between browser pixel and CAPI.
8. **RTL default** — `dir="rtl"` · Arabic primary language.
9. **Migrations run on backend container start** before accepting traffic.

## API Endpoints (Backend)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/products` | Product catalog |
| `GET` | `/api/v1/products/{slug}` | Single product |
| `POST` | `/api/v1/orders` | Create order + CAPI + Sheets |
| `POST` | `/api/v1/events/pageview` | Optional server-side logging |
| `GET` | `/api/v1/orders/{id}` | Thank-you page data |

## Internal DB Connection (Easypanel)

```
postgres://postgres:s4eagoems3oueizu0h00@safraskin_database:5432/safraskin?sslmode=disable
```

Use as `DATABASE_URL` in backend env (internal network).  
Public frontend uses `NEXT_PUBLIC_API_URL=https://api.safraskin.online`.

## Security

- CORS: allow only `https://safraskin.online` (+ `www`)
- Rate limit orders: 5/min per IP
- Validate KSA phone server-side
- Sanitize all text fields
- Never expose DB credentials to frontend
- Webhook secret for Google Sheets optional HMAC

## Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| CLS | < 0.1 |
| TTI | < 3.5s mobile |
| Pixel load | After idle (defer) |
