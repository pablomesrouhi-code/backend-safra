# 18 — Placeholder Images

Until real photography/UGC is provided, use **inline SVG** files in `frontend/public/placeholders/`.

## Design Spec for Placeholders

| Property | Value |
|----------|-------|
| Background | `#FAF7F2` (cream) |
| Accent shape | `#2D6A5A` (sage) |
| Secondary | `#C4A265` (gold) |
| Text | Product name AR · "صورة قريباً" |
| Size | 800×800 product · 1440×800 hero |
| Format | SVG (lightweight) |

## Required Files

```
frontend/public/placeholders/
├── hero-home.svg
├── freshguard.svg
├── heatshield.svg
├── underguard.svg
├── mechanism-breath.svg
├── mechanism-heat.svg
├── mechanism-underarm.svg
└── collection-banner.svg
```

## SVG Template (Product)

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <rect fill="#FAF7F2" width="800" height="800"/>
  <circle cx="400" cy="320" r="120" fill="#2D6A5A" opacity="0.15"/>
  <rect x="280" y="420" width="240" height="180" rx="16" fill="#2D6A5A" opacity="0.25"/>
  <text x="400" y="680" text-anchor="middle" font-family="Arial" font-size="24" fill="#2D6A5A">فريش‌گارد</text>
  <text x="400" y="720" text-anchor="middle" font-family="Arial" font-size="16" fill="#6B6B6B">صورة المنتج قريباً</text>
</svg>
```

## Usage in Next.js

```tsx
import Image from 'next/image';

<Image
  src="/placeholders/freshguard.svg"
  alt="فريش‌گارد — بروتوكول النفس الواثق من الداخل"
  width={800}
  height={800}
  priority
  className="rounded-2xl"
/>
```

## Replacement Process

When real images arrive:
1. Add to `/public/products/freshguard/` (webp preferred)
2. Update `PRODUCTS` constant image paths
3. Keep same aspect ratios to avoid CLS

## UGC Video Placeholders (Homepage)

Use gray rounded rectangles with play icon — link to `#` until videos ready.
