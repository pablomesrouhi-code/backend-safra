TIER_PRICES: dict[int, int] = {1: 219, 2: 279, 3: 319}
CLARELIA_LUMINORA_TIER_PRICES: dict[int, int] = {1: 279, 2: 349, 3: 419}
FEMMELIA_TIER_PRICES: dict[int, int] = {1: 299, 2: 379, 3: 449}
UPSELL_PRICE_MAD = 150

SKU_TO_SLUG: dict[str, str] = {
    "SK482917CL": "clarelia",
    "SK739405FM": "femmelia",
    "SK156820CP": "capilys",
    "SK904371LM": "luminora",
    "SK618204P4": "pack-4",
    "SK275839P3": "pack-3",
    "SK-CLAR-01": "clarelia",
    "SK-FEMM-02": "femmelia",
    "SK-CAPI-03": "capilys",
    "SK-LUMI-04": "luminora",
    "SK-PACK-04": "pack-4",
    "SK-PACK-03": "pack-3",
}

SLUG_TO_SKU: dict[str, str] = {
    "clarelia": "SK482917CL",
    "femmelia": "SK739405FM",
    "capilys": "SK156820CP",
    "luminora": "SK904371LM",
    "pack-4": "SK618204P4",
    "pack-3": "SK275839P3",
}

SLUG_TO_NAME_AR: dict[str, str] = {
    "clarelia": "كريم تفتيح الوجه",
    "femmelia": "زيادة المناطق الأنثوية · 60 كبسولة",
    "capilys": "زيت تساقط الشعر · 60 مل",
    "luminora": "كولاجين بحري · 30 كبسولة",
    "pack-4": "الروتين الكامل",
    "pack-3": "روتين الوجه والشعر",
}

PACK_PRICES: dict[str, int] = {
    "SK618204P4": 699,
    "SK275839P3": 549,
    "SK-PACK-04": 699,
    "SK-PACK-03": 549,
}

VALID_SKUS = frozenset(SKU_TO_SLUG.keys())
PRODUCT_SKUS = frozenset(
    {
        "SK482917CL",
        "SK739405FM",
        "SK156820CP",
        "SK904371LM",
        "SK-CLAR-01",
        "SK-FEMM-02",
        "SK-CAPI-03",
        "SK-LUMI-04",
    }
)


def slug_for_sku(sku: str) -> str | None:
    return SKU_TO_SLUG.get(sku.upper() if sku else "")


def offer_price(qty: int, slug: str | None = None) -> int:
    if slug == "femmelia":
        prices = FEMMELIA_TIER_PRICES
    elif slug in {"clarelia", "luminora"}:
        prices = CLARELIA_LUMINORA_TIER_PRICES
    else:
        prices = TIER_PRICES
    if qty <= 0:
        return 0
    if qty == 1:
        return prices[1]
    if qty == 2:
        return prices[2]
    return prices[3]


def line_price(sku: str, qty: int) -> int:
    pack = PACK_PRICES.get(sku.upper() if sku else "")
    if pack is not None:
        return pack
    return offer_price(qty, slug_for_sku(sku))


def calculate_tier(unique_slugs: list[str], total_qty: int = 0) -> tuple[int, int]:
    unique = set(unique_slugs)
    if len(unique) == 1 and total_qty > 0:
        count = min(max(total_qty, 1), 3)
        return count, TIER_PRICES[count]
    count = min(len(unique), 3) or 1
    return count, TIER_PRICES[count]


def calculate_grand_total(tier_total: int, upsell_accepted: bool, upsell_price: int) -> int:
    return tier_total + (upsell_price if upsell_accepted else 0)
