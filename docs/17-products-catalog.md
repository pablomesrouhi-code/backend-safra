# 17 — Products Catalog (Source of Truth)

## Pricing Engine

```typescript
export const PRODUCTS = [
  {
    slug: 'freshguard',
    sku: 'SS-FRESHGUARD-01',
    nameAr: 'فريش‌گارد — بروتوكول النفس الواثق من الداخل',
    nameEn: 'FreshGuard™ Inside-Out Breath Confidence System',
    shortDescriptionAr: 'بروبيوتيك فموي + شاي مسواك · 60 يوم',
    unitPriceSar: 199,
    crossSellSlugs: ['heatshield', 'underguard'],
    upsellAffinity: 'underguard',
  },
  {
    slug: 'heatshield',
    sku: 'SS-HEATSHIELD-02',
    nameAr: 'هيت‌شield — بودرة درع الحر للجسم',
    nameEn: 'HeatShield™ Desert Body Cooling Powder',
    shortDescriptionAr: 'Talc-free · Oud-light · 120g',
    unitPriceSar: 199,
    crossSellSlugs: ['freshguard', 'underguard'],
    upsellAffinity: 'underguard',
  },
  {
    slug: 'underguard',
    sku: 'SS-UNDERGUARD-03',
    nameAr: 'أندر‌گارد — نظام ثقة الإبط الطبيعي',
    nameEn: 'UnderGuard™ Natural Confidence Balm + Powder Duo',
    shortDescriptionAr: 'Aluminum-free · 45°C stable',
    unitPriceSar: 199,
    crossSellSlugs: ['freshguard', 'heatshield'],
    upsellAffinity: 'freshguard',
  },
] as const;

export const TIER_PRICES: Record<1 | 2 | 3, number> = {
  1: 199,
  2: 279,
  3: 349,
};

export const CROSSSELL_PRICE_SAR = 199;
```

## Cross-sell Matrix

| In Cart | Cross-sell @ 199 |
|---------|------------------|
| freshguard | heatshield, underguard |
| heatshield | freshguard, underguard |
| underguard | freshguard, heatshield |

Cross-sells appear on: **PDP bottom · Cart page · Thank You page**

## Offer Selector Labels (PDP)

| Qty | Price | Badge | Savings vs 199×n |
|-----|-------|-------|------------------|
| 1 | 199 | — | — |
| 2 | 279 | وفّري | 119 SAR |
| 3 | 349 | الأفضل قيمة | 248 SAR |

## Image Placeholders

| Product | Path |
|---------|------|
| freshguard | `/placeholders/freshguard.svg` |
| heatshield | `/placeholders/heatshield.svg` |
| underguard | `/placeholders/underguard.svg` |
| hero home | `/placeholders/hero-home.svg` |

See [18-placeholder-images.md](./18-placeholder-images.md).
