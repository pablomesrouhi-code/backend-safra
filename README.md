# Safra Skin Backend

Minimal FastAPI API for Safra Skin checkout: tier pricing, KSA phone validation, SQLite persistence, and optional Google Sheets / CAPI stubs.

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
  "items": [{ "sku": "SS-FRESHGUARD-01", "qty": 1 }],
  "upsell_sku": "SS-UNDERGUARD-03",
  "upsell_price_sar": 99
}
```

Tier totals (unique SKUs): 1 → 199 SAR, 2 → 279 SAR, 3 → 349 SAR. Upsell adds 99 SAR when `upsell_sku` is set.

Response includes `order_id` like `SS-20260530-A1B2C3`.

## Environment

Copy `.env.example` to `.env`. SQLite is the default (`sqlite:///./safraskin.db`). Leave `GOOGLE_SHEETS_WEBHOOK_URL` and pixel tokens empty to run without external integrations.

## Docker

```bash
docker build -t safraskin-api .
docker run -p 8000:8000 --env-file .env safraskin-api
```
