# 08 — Checkout Funnel & CRO (v2 — Simplified)

## Scope (Locked v2)

**In scope:**
- Home · Collection · 3 PDPs · Cart page · Contact · Legal pages · Thank You
- Header + Footer professional
- Cross-sells (PDP bottom · after add · Cart · Thank You)
- Checkout **Popup** (not a page)
- COD · Google Sheet webhook

**Out of scope (v2 — do NOT build):**
- Subscriptions
- WhatsApp
- SMS
- Quiz / off-site funnels
- Upsell modal @ 99
- About page (not in nav)
- Cart drawer as primary UX

---

## Funnel Diagram

```
PDP / Collection → CTA "أضيف للسلة"
  → Product added to Cart
  → Redirect /cart (or cross-sells visible on PDP bottom)
  → Cross-sells @ 199 (optional add)
  → Cart page → "إتمام الطلب" CTA
  → Checkout Popup (order summary + name + phone)
  → Valid submit → POST /api/v1/orders → Google Sheet
  → Thank You page (+ cross-sells for new order)
```

---

## Pricing (Locked)

| Items in cart (total qty) | Total SAR |
|---------------------------|-----------|
| 1 piece | **199** |
| 2 pieces | **279** |
| 3 pieces | **349** |

Cross-sells always **199** each — tier recalculates when cart hits 2 or 3 items.

Backend validates totals — frontend is display only.

---

## Cart Page `/cart`

### Contents (top → bottom)

1. Line items + remove + qty display
2. Tier total + savings callout (if 2–3 items)
3. **Cross-sell cards** — products not in cart @ 199
4. Trust row: COD · Halal · 14-day · discreet packaging
5. Sticky mobile CTA: **"إتمام الطلب — الدفع عند الاستلام"**

### Empty state

- Message: السلة فارغة
- CTA → `/collection`

---

## Cross-sells — Where

| Location | When |
|----------|------|
| **PDP bottom** | Always show products not in cart |
| **After CTA add** | Redirect to `/cart` where cross-sells appear |
| **Cart page** | Between items and checkout CTA |
| **Thank You** | Products not in completed order — new purchase |

Copy: *"أكملي بروتوكولك — [Product] · 199 ر.س"*

---

## Checkout Popup

Triggered from Cart page CTA. **Not a separate route.**

### Layout

```
┌─────────────────────────────────────────┐
│  ✕                                      │
│  📋 ملخص طلبك                           │
│  [items + total + COD]                  │
├─────────────────────────────────────────┤
│  ⭐ social proof · ⏳ scarcity          │
│  ✓ COD · ✓ تغليف سري · ✓ ضمان 14 يوم   │
├─────────────────────────────────────────┤
│  الاسم الكامل: [____________]           │
│  رقم الجوال:   [05________]            │
│  مثال: 0501234567                       │
├─────────────────────────────────────────┤
│  [  تأكيد طلبي — COD  ]                 │
└─────────────────────────────────────────┘
```

### Phone rules

- Input starts with **0** (display format)
- Accept: `05xxxxxxxx`, `5xxxxxxxx`
- Normalize to E.164 for backend: `+9665XXXXXXXX`
- Show example below field: **مثال: 0501234567**
- CTA disabled until name ≥ 2 chars + valid KSA phone

### CRO in popup

- Order summary repeated (reduces COD confusion)
- Social proof: *"847+ طلب هذا الأسبوع"*
- Scarcity (ethical): *"الشحن اليوم للطلبات قبل 4م"* (Riyadh time)
- Trust micro-copy — **no WhatsApp, no SMS**

### Submit

On valid CTA → POST order → clear cart → redirect `/thank-you/[orderId]`

**No upsell modal. No intermediate steps.**

---

## Thank You Page — CRO for Confirmation & Delivery

`/thank-you/[orderId]`

### Goal

Increase **COD confirmation rate** and **delivery success** — not just "order placed."

### Blocks

| # | Block | Purpose |
|---|-------|---------|
| 1 | ✓ Success + order # | Reassurance |
| 2 | **"ماذا يحدث الآن؟"** 3 steps | Sets expectation → fewer cancellations |
| 3 | **"تأكدي أن هاتفك متاح"** | Confirmation rate ↑ |
| 4 | Order summary + total COD | Memory anchor |
| 5 | Discreet packaging note | Reduces delivery refusal |
| 6 | **Cross-sells** — buy again | AOV on second order |
| 7 | Link → collection / home | |

### "ماذا يحدث الآن؟" copy

1. **تأكيد الطلب** — فريقنا يراجع طلبك خلال ساعات
2. **التجهيز** — تغليف سري وآمن
3. **التوصيل** — الدفع عند الاستلام فقط

### Cross-sells on Thank You

Show products **not in this order** with CTA → add to cart → `/cart` for new order.

---

## Confirmation / Delivery (No SMS/WhatsApp)

| Tactic | Implementation |
|--------|----------------|
| Phone field validated | KSA format only |
| TY page: keep phone available | Copy on thank you |
| Clear Arabic product names in Sheet | Ops can call manually |
| Discreet packaging | Checkout popup + TY |
| Order ID visible | Customer can reference if contacted |

---

## Pages List (v2)

| Route | Page |
|-------|------|
| `/` | Home |
| `/collection` | Collection |
| `/products/[slug]` | 3 product PDPs |
| `/cart` | **Cart** |
| `/contact` | Contact |
| `/legal/terms` | Terms |
| `/legal/privacy` | Privacy |
| `/legal/returns` | Returns |
| `/thank-you/[orderId]` | Thank You |

**Not in v2 nav:** `/about`, quiz, subscriptions

---

## AOV Targets

| Scenario | Total |
|----------|-------|
| 1 product | 199 |
| 2 products (cross-sell) | 279 |
| 3 products | 349 |
| **Blended target** | **250–320 SAR** |
