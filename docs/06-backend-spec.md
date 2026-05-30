# 06 — Backend Specification (FastAPI)

## Stack

| Package | Purpose |
|---------|---------|
| `fastapi` | API framework |
| `uvicorn[standard]` | ASGI server |
| `sqlalchemy` | ORM |
| `alembic` | Migrations |
| `asyncpg` / `psycopg2-binary` | Postgres driver |
| `pydantic` v2 | Schemas |
| `httpx` | Async HTTP (CAPI, Sheets) |
| `python-dotenv` | Env |
| `phonenumbers` | KSA phone validate |

## Folder Structure

```
backend/
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── alembic/
│   └── versions/
└── app/
    ├── main.py
    ├── core/
    │   ├── config.py
    │   ├── database.py
    │   └── startup.py          # run migrations on start
    ├── models/
    │   └── order.py
    ├── schemas/
    │   ├── order.py
    │   └── product.py
    ├── api/
    │   └── routes/
    │       ├── health.py
    │       ├── products.py
    │       └── orders.py
    └── services/
        ├── pricing.py          # server-side tier validation
        ├── orders.py
        ├── sheets.py           # Google webhook
        ├── phone.py
        └── capi/
            ├── meta.py
            ├── tiktok.py
            ├── snapchat.py
            └── hashing.py        # SHA256 normalize
```

## Startup — Migrations on Boot

```python
# app/core/startup.py
import subprocess
from app.core.config import settings

def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)

# app/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield
```

## Config (pydantic-settings)

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    CORS_ORIGINS: str = "https://safraskin.online,https://www.safraskin.online"
    GOOGLE_SHEETS_WEBHOOK_URL: str
    GOOGLE_SHEETS_SECRET: str = ""

    # Meta CAPI
    META_PIXEL_ID: str = ""
    META_ACCESS_TOKEN: str = ""
    META_TEST_EVENT_CODE: str = ""

    # TikTok Events API
    TIKTOK_PIXEL_ID: str = ""
    TIKTOK_ACCESS_TOKEN: str = ""

    # Snapchat CAPI
    SNAP_PIXEL_ID: str = ""
    SNAP_ACCESS_TOKEN: str = ""

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
```

## POST `/api/v1/orders` — Create Order

### Request Body

```json
{
  "customer_name": "فاطمة العتيبي",
  "customer_phone": "+966501234567",
  "items": [
    { "slug": "freshguard", "sku": "SS-FRESHGUARD-01", "quantity": 2 }
  ],
  "upsell": {
    "accepted": true,
    "slug": "underguard",
    "sku": "SS-UNDERGUARD-03",
    "price_sar": 99
  },
  "client_total_sar": 378,
  "event_id": "uuid-from-frontend",
  "utm_source": "tiktok",
  "utm_campaign": "freshguard_may",
  "fbc": "...",
  "fbp": "...",
  "ttclid": "...",
  "user_agent": "...",
  "client_ip": "..." 
}
```

### Server Logic

1. Validate KSA phone → normalize E.164
2. Recalculate tier total from **unique slugs** (never trust `client_total_sar`)
3. If upsell accepted: add 99 SAR + validate upsell product is complementary
4. Insert order + line items in Postgres
5. POST to Google Sheets webhook
6. Fire Meta + TikTok + Snap CAPI `Purchase` with hashed PII + same `event_id`
7. Return `{ order_id, grand_total_sar, thank_you_url }`

### Response

```json
{
  "order_id": "SS-20260529-A1B2C3",
  "grand_total_sar": 378,
  "tier_total_sar": 279,
  "upsell_total_sar": 99,
  "status": "pending_confirmation",
  "thank_you_path": "/thank-you/SS-20260529-A1B2C3"
}
```

## Pricing Service (authoritative)

```python
TIER_PRICES = {1: 199, 2: 279, 3: 349}
UPSELL_PRICE = 99

def calculate_tier(unique_slugs: list[str]) -> int:
    count = len(set(unique_slugs))
    return TIER_PRICES.get(count, 199)

def calculate_grand_total(items, upsell_accepted: bool) -> int:
    tier = calculate_tier([i.slug for i in items])
    upsell = UPSELL_PRICE if upsell_accepted else 0
    return tier + upsell
```

## Products Route (static JSON or DB seed)

`GET /api/v1/products` — return 3 products with Arabic names, slugs, SKUs, cross-sell slugs.

## Rate Limiting

Simple in-memory or Redis: max 5 orders/IP/minute.

## Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## OpenAPI

FastAPI auto-generates `/docs` — disable in production or protect with auth.

## Error Responses

```json
{ "detail": "رقم الجوال غير صالح", "code": "INVALID_PHONE" }
{ "detail": "المجموع غير صحيح", "code": "PRICE_MISMATCH" }
```
