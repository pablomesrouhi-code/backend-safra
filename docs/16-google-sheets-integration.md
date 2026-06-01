# 16 — Google Sheets Integration

## Sheet

**Ops sheet:** https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit

Tab name: **`Orders`**

Import [sheets/order-template.csv](./sheets/order-template.csv) as row 1 headers:

`date | orderid | country | name | phone | product | sku | quantity | total_price | currency | status`

## Flow

```
Frontend → POST api.safraskin.online/api/v1/orders
  → Backend saves DB
  → Backend POST JSON → Google Apps Script Web App URL (no secret)
  → Apps Script appends one row
  → Ops calls customer for COD confirmation
```

## Row format (one row per order)

| Column | Source | Example |
|--------|--------|---------|
| date | KSA `dd/mm/yyyy` | `01/05/2026` |
| orderid | backend `ORDER_NUMBER_PREFIX` + random | `nama8k2m9x1p` |
| country | fixed | `KSA` |
| name | checkout form | `فاطمة` |
| phone | E.164 without `+` | `96650475233` |
| product | Arabic names, `/` separated | `هدوء الدورة/فلورا الفم` |
| sku | product SKUs, `/` separated | `SK847291CY/SK295103OR` |
| quantity | qty per line, `/` separated | `2` or `2/1` or `2/2/2` |
| total_price | grand total SAR | `378` |
| currency | fixed | `SAR` |
| status | **empty** on insert | |

### Product SKUs

| Slug | SKU | Arabic name |
|------|-----|-------------|
| cyclecalm | `SK847291CY` | هدوء الدورة |
| oralflora | `SK295103OR` | فلورا الفم |
| clearbalance | `SK716408CB` | توازن البشرة |

Legacy SKUs (`BL-CYCLE-01`, etc.) still accepted by the API for old carts.

## Backend webhook payload

Built in `app/services/sheets.py`:

```json
{
  "date": "01/05/2026",
  "orderid": "nama8k2m9x1p",
  "country": "KSA",
  "name": "فاطمة",
  "phone": "96650475233",
  "product": "هدوء الدورة/فلورا الفم",
  "sku": "SK847291CY/SK295103OR",
  "quantity": "2/1",
  "total_price": 378,
  "currency": "SAR",
  "status": ""
}
```

Env: `GOOGLE_SHEETS_WEBHOOK_URL` — Apps Script deployment URL only (no secret).

## Apps Script deploy

1. Open the [Google Sheet](https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit)
2. Tab **Orders** → headers from `order-template.csv`
3. **Extensions → Apps Script** → paste [sheets/google-apps-script.js](./sheets/google-apps-script.js) → **Save**
4. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Copy URL (ends with `/exec`) → Easypanel backend env:

```env
GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
ORDER_NUMBER_PREFIX=nama
```

6. Test: open the deployment URL in browser → `{"status":"Safra Skin order webhook active",...}`

## Retry

If sheet sync fails: `orders.sheets_synced = false`, error logged. Order still saved in DB.

## Ops workflow

1. New row appears in Sheet (status empty)
2. Team calls customer to confirm COD
3. Update **status** manually in the sheet
