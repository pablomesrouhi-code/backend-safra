# 16 — Google Sheets Integration

## Sheet

**Ops sheet:** https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit

Tab name: **`Orders`**

Import [sheets/order-template.csv](./sheets/order-template.csv) as row 1 headers:

`DATE | ORDERID | COUNTRY | NAME | PHONE | PRODUCT | SKU | QUANTITY | TOTAL PRICE | CURRENCE | STATUS`

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
| DATE | Casablanca `dd/mm/yyyy` | `01/05/2026` |
| ORDERID | `nama` + random | `nama8k2m9x1p` |
| COUNTRY | fixed | `MAROC` |
| NAME | checkout form | `سارة بنعلي` |
| PHONE | local 06/07 | `0682767535` |
| PRODUCT | Arabic names, `/` separated | `كريم تفتيح الوجه/زيت تساقط الشعر · 60 مل` |
| SKU | product SKUs, `/` separated | `SK482917CL/SK156820CP` |
| QUANTITY | qty per line, `/` separated | `2` or `2/1` or `2/2/2` |
| TOTAL PRICE | grand total | `438` |
| CURRENCE | fixed | `DH` |
| STATUS | **empty** on insert | |

### Product SKUs

| Slug | SKU | Arabic name |
|------|-----|-------------|
| clarelia | `SK482917CL` | كريم تفتيح الوجه |
| femmelia | `SK739405FM` | زيادة المناطق الأنثوية · 60 كبسولة |
| capilys | `SK156820CP` | زيت تساقط الشعر · 60 مل |
| luminora | `SK904371LM` | كولاجين بحري · 30 كبسولة |
| pack-4 | `SK618204P4` | الروتين الكامل |
| pack-3 | `SK275839P3` | روتين الوجه والشعر |

Legacy SKUs (`SK-CLAR-01`, etc.) still accepted by the API for old carts.

## Backend webhook payload

Built in `app/services/sheets.py`:

```json
{
  "date": "01/05/2026",
  "orderid": "nama8k2m9x1p",
  "country": "MAROC",
  "name": "سارة بنعلي",
  "phone": "0682767535",
  "product": "كريم تفتيح الوجه/زيت تساقط الشعر · 60 مل",
  "sku": "SK482917CL/SK156820CP",
  "quantity": "2/2",
  "total_price": 438,
  "currency": "DH",
  "status": ""
}
```

Env: `GOOGLE_SHEETS_WEBHOOK_URL` — Apps Script deployment URL only (no secret).

## Apps Script deploy

1. Open your **order safraskin** Google Sheet
2. Tab **Orders** → headers from `order-template.csv`
3. **Extensions → Apps Script** → paste [sheets/google-apps-script.js](./sheets/google-apps-script.js) → **Save**
4. Run `testAppendRow` once to authorize
5. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
6. Copy URL (ends with `/exec`) → Easypanel backend env:

```env
GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
ORDER_NUMBER_PREFIX=nama
```

7. Open the `/exec` URL in a browser → `{"status":"ok","sheet":"Orders"}`

## Retry

If sheet sync fails: `orders.sheets_synced = false`, error logged. Order still saved in DB.

## Ops workflow

1. New row appears in Sheet (status empty)
2. Team calls customer to confirm COD
3. Update **status** manually in the sheet
