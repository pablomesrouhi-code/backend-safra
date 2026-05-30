# 04 — Design System

## Brand Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-primary` | `#2D6A5A` | Sage green — trust, halal, natural |
| `--color-primary-dark` | `#1E4D42` | Hover, footer |
| `--color-accent` | `#C4A265` | Soft gold — premium, CTA accents |
| `--color-accent-light` | `#E8D5B0` | Badges, highlights |
| `--color-bg` | `#FAF7F2` | Warm cream page background |
| `--color-bg-card` | `#FFFFFF` | Cards, drawer |
| `--color-text` | `#1A1A1A` | Body text |
| `--color-text-muted` | `#6B6B6B` | Secondary |
| `--color-success` | `#3D8B6E` | Trust badges |
| `--color-scarcity` | `#B85C4A` | Soft terracotta — urgency (not aggressive red) |
| `--color-border` | `#E8E4DD` | Dividers |

## Typography

```tsx
// next/font in layout.tsx
import { IBM_Plex_Sans_Arabic, Inter } from 'next/font/google';

const arabic = IBM_Plex_Sans_Arabic({
  subsets: ['arabic'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-arabic',
});

const english = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-english',
});
```

| Element | Font | Size (mobile / desktop) |
|---------|------|-------------------------|
| H1 | Arabic 700 | 28px / 40px |
| H2 | Arabic 600 | 22px / 32px |
| Body | Arabic 400 | 16px / 18px |
| English sub-brand | Inter 500 | 11px / 12px, letter-spacing 0.08em |
| Price | Arabic 700 | 24px / 28px |

## Header (RTL — logo on RIGHT)

```
┌────────────────────────────────────────────────────────────┐
│  [🛒 Cart 2]    الرئيسية  المجموعة  من نحن  تواصل          │
│                                    ┌──┐  سفرا جلد          │
│                                    │ S │  Safra Skin        │
│                                    └──┘  (circle primary)  │
└────────────────────────────────────────────────────────────┘
```

### Logo Component Spec

- **Circle:** 40px · bg `--color-primary` · white "S" · font-weight 700
- **Arabic:** سفرا جلد — `--font-arabic` 600 · 18px
- **English:** Safra Skin — `--font-english` 500 · 10px · muted · below Arabic
- **Click:** → homepage

## Footer

```
┌────────────────────────────────────────────────────────────┐
│  [S] سفرا جلد · Safra Skin                                  │
│  انتعاشك يسبق انطباعك                                       │
├────────────────────────────────────────────────────────────┤
│  تسوق          │  مساعدة           │  قانوني               │
│  المجموعة      │  تواصل            │  الشروط               │
│  فريش‌گارد     │  الأسئلة          │  الخصوصية             │
│  هيت‌شield     │  COD · اتصال تأكيد │  الاسترداد            │
│  أندر‌گارد     │                   │                       │
├────────────────────────────────────────────────────────────┤
│  ✓ Halal-aligned  ✓ COD  ✓ 14-day guarantee  ✓ KSA shipping│
│  © 2026 Safra Skin · safraskin.online                        │
└────────────────────────────────────────────────────────────┘
```

## Spacing & Radius

| Token | Value |
|-------|-------|
| `--radius-sm` | 8px |
| `--radius-md` | 12px |
| `--radius-lg` | 16px |
| `--radius-full` | 9999px |
| Section padding | py-16 md:py-24 |
| Container max | 1200px |

## Components Library

| Component | Notes |
|-----------|-------|
| `Button` | primary (sage) · accent (gold) · ghost |
| `TrustBar` | horizontal badges |
| `ProductCard` | stars · scarcity · price from |
| `OfferSelector` | 1/2/3 piece radio cards |
| `CartDrawer` | slide from left (RTL) |
| `CheckoutPopup` | modal center mobile full-screen |
| `UpsellModal` | timer ring · 99 SAR |
| `ReviewCard` | city · stars · problem tag |
| `IngredientRow` | icon + name + benefit |
| `AlternatingSection` | image/text flip per section |
| `ScarcityBadge` | "🔥 X طلب اليوم" (dynamic or seeded) |
| `StarRating` | 4.8/5 display |

## Alternating Layout Pattern

```tsx
// Section 1: image LEFT, text RIGHT (in RTL: image appears on visual right)
// Section 2: image RIGHT, text LEFT
// Alternate on product pages and homepage story sections

<section className="grid md:grid-cols-2 gap-8 items-center">
  <div className={index % 2 === 0 ? 'md:order-2' : 'md:order-1'}>
    {/* Text */}
  </div>
  <div className={index % 2 === 0 ? 'md:order-1' : 'md:order-2'}>
    {/* Image placeholder */}
  </div>
</section>
```

## Responsive Breakpoints

| Name | Width |
|------|-------|
| sm | 640px |
| md | 768px |
| lg | 1024px |
| xl | 1280px |

Mobile-first. Sticky mobile ATC on PDP. Cart drawer full-width mobile.

## Motion

- Drawer: `transform translate` 300ms ease
- Modal: fade + scale
- Trust bar: subtle marquee optional
- **No** heavy animations — performance first

## Icons

Use **Lucide React** — consistent stroke width 1.5
