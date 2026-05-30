# 16 — Google Sheets Integration

## Flow

```
Frontend → POST api.safraskin.online/api/v1/orders
  → Backend saves Postgres
  → Backend POST → Google Apps Script Web App URL
  → Apps Script appends row to Sheet
  → Ops team calls customer for COD confirmation (manual v1)
```

## Sheet Template

Import [sheets/order-template.csv](./sheets/order-template.csv) as header row in Google Sheet tab `Orders`.

## Column Definitions

| Column | Source | Example |
|--------|--------|---------|
| order_id | backend | SS-20260529-A1B2 |
| created_at | ISO8601 | 2026-05-29T14:30:00Z |
| customer_name | form | فاطمة |
| customer_phone | E.164 | +966501234567 |
| items_json | JSON string | [{"slug":"freshguard","qty":2}] |
| items_display | human AR | فريش‌گارد ×2 |
| tier_count | int | 2 |
| tier_total_sar | int | 279 |
| upsell_accepted | YES/NO | YES |
| upsell_product | AR name | أندر‌گارد |
| upsell_price_sar | int | 99 |
| grand_total_sar | int | 378 |
| payment | COD | COD |
| status | pending_confirmation | |
| utm_source | | tiktok |
| utm_campaign | | freshguard_may |
| event_id | uuid | dedup ref |
| notes | | |

## Backend Webhook Payload

```python
# services/sheets.py
async def sync_order_to_sheet(order: Order) -> bool:
    payload = {
        "secret": settings.GOOGLE_SHEETS_SECRET,
        "order_id": order.order_number,
        "created_at": order.created_at.isoformat(),
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "items_json": json.dumps(order.items),
        "items_display": format_items_ar(order.items),
        "tier_count": order.tier_count,
        "tier_total_sar": order.tier_total_sar,
        "upsell_accepted": order.upsell_accepted,
        "upsell_product": order.upsell_slug,
        "upsell_price_sar": order.upsell_price_sar or 0,
        "grand_total_sar": order.grand_total_sar,
        "payment": "COD",
        "status": order.status,
        "utm_source": order.utm_source,
        "utm_campaign": order.utm_campaign,
        "event_id": order.event_id,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(settings.GOOGLE_SHEETS_WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
```

## Apps Script

Deploy [sheets/google-apps-script.js](./sheets/google-apps-script.js):

1. Open Google Sheet → Extensions → Apps Script
2. Paste script
3. Set `SECRET` constant to match `GOOGLE_SHEETS_SECRET`
4. Deploy → Web app → Execute as: Me → Anyone
5. Copy URL → `GOOGLE_SHEETS_WEBHOOK_URL` in backend env

## Retry Logic

If sheet sync fails:
- Set `orders.sheets_synced = false`
- Log error
- Optional cron retry (v2)

## Ops Workflow

1. New row appears in Sheet
2. Team calls customer to confirm order (manual v1)
3. Update status column manually or via admin v2

## Security

- Validate `secret` in Apps Script before append
- Do not expose webhook URL publicly
- Sheet access restricted to ops team Google accounts
