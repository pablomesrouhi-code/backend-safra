TIER_PRICES: dict[int, int] = {1: 199, 2: 279, 3: 349}

SKU_TO_SLUG: dict[str, str] = {
    "SS-FRESHGUARD-01": "freshguard",
    "SS-HEATSHIELD-02": "heatshield",
    "SS-UNDERGUARD-03": "underguard",
}

SLUG_TO_SKU: dict[str, str] = {v: k for k, v in SKU_TO_SLUG.items()}

VALID_SKUS = frozenset(SKU_TO_SLUG.keys())


def slug_for_sku(sku: str) -> str | None:
    return SKU_TO_SLUG.get(sku.upper() if sku else "")


def calculate_tier(unique_slugs: list[str]) -> tuple[int, int]:
    """Return (tier_count, tier_total_sar) from unique product slugs."""
    count = min(len(set(unique_slugs)), 3) or 1
    return count, TIER_PRICES.get(count, TIER_PRICES[1])


def calculate_grand_total(tier_total_sar: int, upsell_accepted: bool, upsell_price: int) -> int:
    return tier_total_sar + (upsell_price if upsell_accepted else 0)
