TIER_PRICES: dict[int, int] = {1: 199, 2: 279, 3: 349}

SKU_TO_SLUG: dict[str, str] = {
    "SK847291CY": "cyclecalm",
    "SK295103OR": "oralflora",
    "SK716408CB": "clearbalance",
    # legacy SKUs (old carts / imports)
    "BL-CYCLE-01": "cyclecalm",
    "BL-ORAL-02": "oralflora",
    "BL-SKIN-03": "clearbalance",
    "SS-FRESHGUARD-01": "oralflora",
    "SS-HEATSHIELD-02": "cyclecalm",
    "SS-UNDERGUARD-03": "clearbalance",
    "SS-CONFIDENCE-01": "oralflora",
}

SLUG_TO_SKU: dict[str, str] = {
    "cyclecalm": "SK847291CY",
    "oralflora": "SK295103OR",
    "clearbalance": "SK716408CB",
}

SLUG_TO_NAME_AR: dict[str, str] = {
    "cyclecalm": "هدوء الدورة",
    "oralflora": "فلورا الفم",
    "clearbalance": "توازن البشرة",
}

VALID_SKUS = frozenset(SKU_TO_SLUG.keys())


def slug_for_sku(sku: str) -> str | None:
    return SKU_TO_SLUG.get(sku.upper() if sku else "")


def calculate_tier(unique_slugs: list[str], total_qty: int = 0) -> tuple[int, int]:
    """Tier by unique SKUs (1/2/3 products) or by total_qty when single-SKU qty bundles."""
    unique = set(unique_slugs)
    if len(unique) == 1 and total_qty > 0:
        count = min(max(total_qty, 1), 3)
        return count, TIER_PRICES[count]
    count = min(len(unique), 3) or 1
    return count, TIER_PRICES[count]


def calculate_grand_total(tier_total_sar: int, upsell_accepted: bool, upsell_price: int) -> int:
    return tier_total_sar + (upsell_price if upsell_accepted else 0)
