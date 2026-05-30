# 11 — Product Pages Specification

Each PDP is a **landing page** optimized for Snapchat/TikTok traffic.

## Shared PDP Structure (Top → Bottom)

| # | Section | CRO Purpose |
|---|---------|-------------|
| 1 | **Product Hero** | Stars · scarcity · H1 · offer selector · CTA |
| 2 | **Trust bar** | Halal · COD · guarantee |
| 3 | **Problem hook** | Emotion — "تعرفين هذا الشعور؟" |
| 4 | **Mechanism** | Inside-out / science diagram |
| 5 | **Ingredients** | Accordion — INCI + benefit each |
| 6 | **How to use** | 3 steps · 60-day protocol |
| 7 | **Social proof** | Reviews filtered to this product |
| 8 | **Comparison** | Safra Skin vs generic alternative |
| 9 | **FAQ** | 5-6 objections |
| 10 | **Guarantee** | 14-day · phone confirmation |
| 11 | **Final offer block** | Repeat selector + CTA |
| 12 | **Sticky mobile ATC** | Offer + CTA always visible |

## Section 1 — Product Hero Wireframe

```
┌─────────────────────────────────────────────────────────┐
│  ⭐ 4.9 (847)  ·  🔥 34 طلب اليوم                        │
│                                                         │
│  [Product Image — placeholder]                          │
│                                                         │
│  فريش‌گارد                                              │
│  بروتوكول النفس الواثق من الداخل                        │
│  FreshGuard™ Inside-Out Breath System                   │
│                                                         │
│  "مش تغطية. إعادة توازن من الداخل."                     │
│                                                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                     │
│  │ 1 قطعة  │ │ 2 قطعة  │ │ 3 قطع   │                     │
│  │ 199 ر.س │ │ 279 ر.س │ │ 349 ر.س │                     │
│  │         │ │ وفّري   │ │ أفضل    │                     │
│  └─────────┘ └─────────┘ └─────────┘                     │
│                                                         │
│  [  أضيف للسلة واطلب الآن — COD  ]                      │
│  ✓ دفع عند الاستلام · ✓ شحن 2-4 أيام                    │
└─────────────────────────────────────────────────────────┘
```

## CTA Behavior (All PDPs)

```typescript
function handleAddToCart(selectedOffer: 1 | 2 | 3) {
  addItem(currentSlug, selectedOffer); // qty = offer count
  openCartDrawer();
  trackAddToCart({ slug, qty: selectedOffer, eventId });
}
```

---

## Product 1: فريش‌گارد (freshguard)

| Field | Value |
|-------|-------|
| **Slug** | `freshguard` |
| **SKU** | `SS-FRESHGUARD-01` |
| **H1** | فريش‌گارد — بروتوكول النفس الواثق من الداخل |
| **Hero sub** | بروبيوتيك فموي + شاي مسواك · 60 يوم |

### Unique Sections

**Problem copy:**  
*"33% من السعوديات يعانين من نفس كريhe — 76% يقلقن من التواصل. أنتِ مش لوحدك."*

**Mechanism:**  
L. reuteri + zinc gluconate → oral microbiome balance · miswak tea ritual

**Ingredients:**
| Ingredient | Benefit (AR) |
|------------|--------------|
| L. reuteri | يدعم توازن الفم |
| Zinc gluconate | يساعد على نفس منعش |
| Miswak extract | تراث · تنظيف طبيعي |
| Peppermint | انتعاش فوري |

**FAQ:**
- هل halal؟ → نعم، تركيبة متوافقة
- كم المدة؟ → 60 يوم بروتوكول
- بديل غسول فم؟ → من الداخل، ليس تغطية

---

## Product 2: هيت‌شield (heatshield)

| Field | Value |
|-------|-------|
| **Slug** | `heatshield` |
| **SKU** | `SS-HEATSHIELD-02` |
| **H1** | هيت‌شield — بودرة درع الحر للجسم |
| **Hero sub** | Talc-free · Oud-light · 120g + applicator |

### Unique Sections

**Problem:** حر 50°م · بقع · رطوبة · قمصان صيف

**Mechanism:** Rice starch + zinc oxide absorb · tea tree freshness

**Ingredients:**
| Ingredient | Benefit |
|------------|---------|
| Rice starch | امتصاص الرطوبة |
| Zinc oxide | حماية وتجفيف |
| Tea tree | انتعاش · نظافة |
| Peppermint | إحساس بارد |
| Oud light | عطر خليجي راقٍ |

---

## Product 3: أندر‌گارد (underguard)

| Field | Value |
|-------|-------|
| **Slug** | `underguard` |
| **SKU** | `SS-UNDERGUARD-03` |
| **H1** | أندر‌گارد — نظام ثقة الإبط الطبيعي |
| **Hero sub** | Balm + Powder Duo · Aluminum-free · 45°C stable |

### Unique Sections

**Problem:** المصعد · الدوام · الصلاة · رفع الذ arm

**Mechanism:** Natural balm (magnesium + arrowroot) + powder mini

**Ingredients:**
| Ingredient | Benefit |
|------------|---------|
| Magnesium hydroxide | حماية طبيعية |
| Arrowroot powder | امتصاص |
| Probiotic | توازن البشرة |
| Oud citrus | عطر unisex فاخر |

---

## Alternating Section Layout

| Section # | Desktop layout |
|-----------|----------------|
| Problem | Image LEFT · Text RIGHT (RTL visual) |
| Mechanism | Text LEFT · Image RIGHT |
| Ingredients | Image LEFT · Text RIGHT |
| How to use | Text LEFT · Image RIGHT |

Use `index % 2` order flip — see [04-design-system.md](./04-design-system.md).

## Pixel Events on PDP

- `ViewContent` on mount with `content_ids: [sku]`
- `AddToCart` on CTA click

## Cross-sells (shown in drawer after add)

Show the **other 2 products** @ 199 SAR each.
