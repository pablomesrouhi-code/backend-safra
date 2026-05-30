# 09 — Tracking Pixels (Web + CAPI)

## Overview

| Platform | Browser Pixel | Server CAPI | Dedup Key |
|----------|---------------|-------------|-----------|
| Meta (Facebook) | fbq — **deferred** | Graph API `/events` | `event_id` |
| TikTok | ttq — **deferred** | Events API | `event_id` |
| Snapchat | snaptr — **deferred** | Conversions API v3 | `event_id` (client dedup id) |

**Rule:** Browser sends event with `eventID`. Backend CAPI sends same `event_id`. Platforms deduplicate.

---

## Web Pixels — Deferred Loading

**Do NOT load pixels in `<head>` synchronously.**

```tsx
// components/tracking/DeferredPixels.tsx
'use client';
import { useEffect } from 'react';

export function DeferredPixels() {
  useEffect(() => {
    const load = () => {
      import('@/lib/pixels/meta').then(m => m.initMetaPixel());
      import('@/lib/pixels/tiktok').then(m => m.initTikTokPixel());
      import('@/lib/pixels/snapchat').then(m => m.initSnapPixel());
    };

    if ('requestIdleCallback' in window) {
      requestIdleCallback(load, { timeout: 3000 });
    } else {
      setTimeout(load, 2000);
    }
  }, []);

  return null;
}
```

**Alternative trigger:** Load on first scroll or first click (even faster LCP).

### Environment Variables (Frontend)

```
NEXT_PUBLIC_META_PIXEL_ID=
NEXT_PUBLIC_TIKTOK_PIXEL_ID=
NEXT_PUBLIC_SNAP_PIXEL_ID=
```

---

## Event Map

| Event | When | Browser | CAPI |
|-------|------|---------|------|
| `PageView` | Route change | ✅ | Optional |
| `ViewContent` | PDP view | ✅ | ✅ |
| `AddToCart` | Add + drawer open | ✅ | ✅ |
| `InitiateCheckout` | Checkout popup open | ✅ | ✅ |
| `Purchase` | Order success | ✅ | ✅ **required** |

---

## event_id Generation

```typescript
import { v4 as uuidv4 } from 'uuid';

export function generateEventId(): string {
  return uuidv4();
}

// Store in checkout flow — pass to backend on order submit
```

---

## Meta (Facebook)

### Browser — NO hashing

```javascript
fbq('track', 'Purchase', {
  value: 279,
  currency: 'SAR',
  content_ids: ['SS-FRESHGUARD-01'],
  content_type: 'product',
}, { eventID: eventId });
```

### CAPI — SHA256 hashing REQUIRED

Normalize before hash (Meta spec):

| Field | Normalization | Hash |
|-------|---------------|------|
| `em` (email) | lowercase, trim | sha256 — N/A v1 (no email collected) |
| `ph` (phone) | digits only, country code, **no +, no spaces, no leading zeros** | sha256 |
| `fn` (first name) | lowercase, a-z only | sha256 |
| `ln` (last name) | lowercase, a-z only | sha256 — optional |

**KSA Phone for Meta CAPI hashing:**

```
Input:  0501234567 or +966501234567
Step 1: Remove all non-digits → 966501234567 or 0501234567
Step 2: If starts with 0, replace with 966 → 966501234567
Step 3: Must NOT include + sign in hashed value
Step 4: sha256("966501234567")
```

```python
# backend/app/services/capi/hashing.py
import hashlib
import re

def normalize_phone_meta(phone_e164: str) -> str:
    """Meta: lowercase not applicable; digits only with country code, no +"""
    digits = re.sub(r'\D', '', phone_e164)
    if digits.startswith('0'):
        digits = '966' + digits[1:]
    if not digits.startswith('966'):
        digits = '966' + digits.lstrip('0')
    return digits

def sha256_hash(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode('utf-8')).hexdigest()

def hash_phone_meta(phone_e164: str) -> str:
    return sha256_hash(normalize_phone_meta(phone_e164))
```

### Meta CAPI Payload

```json
{
  "data": [{
    "event_name": "Purchase",
    "event_time": 1717000000,
    "event_id": "uuid-from-frontend",
    "action_source": "website",
    "event_source_url": "https://safraskin.online/thank-you/SS-xxx",
    "user_data": {
      "ph": ["<sha256_phone>"],
      "fn": ["<sha256_first_name>"],
      "client_ip_address": "1.2.3.4",
      "client_user_agent": "Mozilla/5.0...",
      "fbc": "fb.1.xxx",
      "fbp": "fb.1.xxx"
    },
    "custom_data": {
      "value": 279,
      "currency": "SAR",
      "content_ids": ["SS-FRESHGUARD-01"],
      "content_type": "product",
      "order_id": "SS-20260529-XXXX"
    }
  }]
}
```

POST: `https://graph.facebook.com/v21.0/{PIXEL_ID}/events?access_token={TOKEN}`

---

## TikTok

### Browser — NO hashing

```javascript
ttq.track('CompletePayment', {
  value: 279,
  currency: 'SAR',
  content_id: 'SS-FRESHGUARD-01',
  content_type: 'product',
}, { event_id: eventId });
```

### TikTok Events API — hashing REQUIRED

**Phone normalization for TikTok:**

```
E.164 WITH leading + and country code
Example: +966501234567
Then SHA256 hash the string INCLUDING the +
```

```python
def normalize_phone_tiktok(phone_e164: str) -> str:
    """TikTok: E.164 with + prefix before hashing"""
    digits = re.sub(r'\D', '', phone_e164)
    if not digits.startswith('966'):
        if digits.startswith('0'):
            digits = '966' + digits[1:]
        else:
            digits = '966' + digits
    return '+' + digits

def hash_phone_tiktok(phone_e164: str) -> str:
    return sha256_hash(normalize_phone_tiktok(phone_e164))
```

### TikTok CAPI Payload

```json
{
  "event_source": "web",
  "event_source_id": "PIXEL_ID",
  "data": [{
    "event": "CompletePayment",
    "event_time": "2026-05-29T12:00:00Z",
    "event_id": "uuid",
    "user": {
      "phone": "<sha256_of_+966501234567>",
      "external_id": "<sha256_order_id>"
    },
    "properties": {
      "value": 279,
      "currency": "SAR",
      "content_type": "product",
      "contents": [{ "content_id": "SS-FRESHGUARD-01", "quantity": 1 }]
    },
    "page": { "url": "https://safraskin.online/thank-you/..." }
  }]
}
```

POST: `https://business-api.tiktok.com/open_api/v1.3/event/track/`

Header: `Access-Token: {TIKTOK_ACCESS_TOKEN}`

---

## Snapchat

### Browser — deferred snaptr

```javascript
snaptr('track', 'PURCHASE', {
  'price': 279,
  'currency': 'SAR',
  'transaction_id': orderId,
  'item_ids': ['SS-FRESHGUARD-01'],
  'uuid_c1': eventId  // dedup
});
```

### Snapchat CAPI — hashing REQUIRED

Phone: E.164 digits **without +** OR per Snap docs — use SHA256 of lowercase trimmed email/phone.

**Snap phone hash:** Remove non-digits, include country code, no plus:

```python
def hash_phone_snap(phone_e164: str) -> str:
    normalized = normalize_phone_meta(phone_e164)  # same as Meta — digits only 966...
    return sha256_hash(normalized)
```

---

## Dedup Summary Table

| Platform | Browser key | CAPI key | Phone hash input |
|----------|-------------|----------|------------------|
| Meta | `eventID` in fbq options | `event_id` in payload | `966501234567` (no +) |
| TikTok | `event_id` in ttq options | `event_id` in payload | `+966501234567` (with +) |
| Snap | `uuid_c1` | `client_dedup_id` / event_id | `966501234567` (no +) |

---

## Frontend → Backend on Order

Pass to `POST /api/v1/orders`:

```typescript
{
  event_id: string,
  fbc?: string,      // from cookie _fbc
  fbp?: string,      // from cookie _fbp
  ttclid?: string,   // from URL/cookie
  sc_click_id?: string,
  user_agent: string,
  // IP captured server-side from request headers
}
```

## Testing

- Meta: `META_TEST_EVENT_CODE` in CAPI payload `test_event_code` field
- TikTok: test events in Events Manager
- Verify dedup: same event_id → 1 counted event in dashboard

## Privacy

- Cookie consent banner (KSA — lightweight notice)
- Privacy policy page link in footer
- Do not send PII to browser pixels — only CAPI server-side
