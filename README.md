# Safra Skin Backend

Minimal FastAPI API for Safra Skin checkout: tier pricing, KSA phone validation, MaxMind GeoIP, SQLite/Postgres, and optional Google Sheets / CAPI.

**Frontend store:** https://github.com/pablomesrouhi-code/frontend-safra  
**Project docs:** [`docs/`](./docs/) (specs, playbook, env templates)

## Quick start

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: `GET http://localhost:8000/health`
- Products: `GET http://localhost:8000/api/v1/products`
- Orders: `POST http://localhost:8000/api/v1/orders`
- OpenAPI: `http://localhost:8000/docs`

Point the frontend at `NEXT_PUBLIC_API_URL=http://localhost:8000`.

## Create order

```json
{
  "customer_name": "فاطمة",
  "customer_phone": "+966501234567",
  "items": [{ "sku": "SK847291CY", "qty": 2 }],
  "upsell_sku": "SK716408CB",
  "upsell_price_sar": 99
}
```

Tier totals (unique SKUs): 1 → 199 SAR, 2 → 279 SAR, 3 → 349 SAR. Upsell adds 99 SAR when `upsell_sku` is set.

Response includes `order_id` like `nama8k2m9x1p`. Each order is also POSTed to Google Sheets when `GOOGLE_SHEETS_WEBHOOK_URL` is set (see `docs/16-google-sheets-integration.md`).

## Easypanel deploy

| Setting | Value |
|---------|--------|
| Repo | `https://github.com/pablomesrouhi-code/backend-safra` |
| Dockerfile | `Dockerfile` (repo root) |
| Port | `8000` |
| Health check | `GET /health` |

Paste env vars from `.env.example`. **Required for production:**

- `DATABASE_URL` → Postgres internal URL (`safraskin_database:5432`)
- `CORS_ORIGINS` → `https://safraskin.online,https://www.safraskin.online`

Optional: Sheets webhook + CAPI tokens (API works without them).

## Environment

Copy `.env.example` to `.env`. SQLite is the default for local dev. Leave `GOOGLE_SHEETS_WEBHOOK_URL` and pixel tokens empty to run without external integrations.

## Docker

```bash
docker build -t safraskin-api .
docker run -p 8000:8000 --env-file .env safraskin-api
```
