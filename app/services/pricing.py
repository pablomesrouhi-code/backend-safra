TIER_PRICES: dict[int, int] = {1: 219, 2: 279, 3: 319}
UPSELL_PRICE_MAD = 120

SKU_TO_SLUG: dict[str, str] = {
    "SK-CLAR-01": "clarelia",
    "SK-FEMM-02": "femmelia",
    "SK-CAPI-03": "capilys",
    "SK-LUMI-04": "luminora",
    "SK-PACK-04": "pack-4",
    "SK-PACK-03": "pack-3",
}

SLUG_TO_SKU: dict[str, str] = {
    "clarelia": "SK-CLAR-01",
    "femmelia": "SK-FEMM-02",
    "capilys": "SK-CAPI-03",
    "luminora": "SK-LUMI-04",
    "pack-4": "SK-PACK-04",
    "pack-3": "SK-PACK-03",
}

SLUG_TO_NAME_AR: dict[str, str] = {
    "clarelia": "كريم الكلف والتصبغات",
    "femmelia": "كريم عناية للقوام الأنثوي",
    "capilys": "سيروم الفروة ضد التساقط",
    "luminora": "عناية الإشراق من الداخل",
    "pack-4": "الروتين الكامل",
    "pack-3": "روتين الوجه والشعر",
}

PACK_PRICES: dict[str, int] = {
    "SK-PACK-04": 699,
    "SK-PACK-03": 549,
}

VALID_SKUS = frozenset(SKU_TO_SLUG.keys())
PRODUCT_SKUS = frozenset({"SK-CLAR-01", "SK-FEMM-02", "SK-CAPI-03", "SK-LUMI-04"})


def slug_for_sku(sku: str) -> str | None:
    return SKU_TO_SLUG.get(sku.upper() if sku else "")


def offer_price(qty: int) -> int:
    if qty <= 0:
        return 0
    if qty == 1:
        return TIER_PRICES[1]
    if qty == 2:
        return TIER_PRICES[2]
    return TIER_PRICES[3]


def line_price(sku: str, qty: int) -> int:
    pack = PACK_PRICES.get(sku.upper() if sku else "")
    if pack is not None:
        return pack
    return offer_price(qty)


def calculate_tier(unique_slugs: list[str], total_qty: int = 0) -> tuple[int, int]:
    unique = set(unique_slugs)
    if len(unique) == 1 and total_qty > 0:
        count = min(max(total_qty, 1), 3)
        return count, TIER_PRICES[count]
    count = min(len(unique), 3) or 1
    return count, TIER_PRICES[count]


def calculate_grand_total(tier_total: int, upsell_accepted: bool, upsell_price: int) -> int:
    return tier_total + (upsell_price if upsell_accepted else 0)
