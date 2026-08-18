from fastapi import APIRouter

from app.schemas.product import ProductOut
from app.services.pricing import FEMMELIA_TIER_PRICES, SLUG_TO_NAME_AR, SLUG_TO_SKU, TIER_PRICES

router = APIRouter(prefix="/api/v1", tags=["products"])

PRODUCTS: list[ProductOut] = [
    ProductOut(
        slug="clarelia",
        sku=SLUG_TO_SKU["clarelia"],
        name_ar=SLUG_TO_NAME_AR["clarelia"],
        name_en="Clarélia",
        unit_price_sar=TIER_PRICES[1],
        unit_price_mad=TIER_PRICES[1],
        cross_sell_slugs=["luminora", "capilys", "femmelia"],
    ),
    ProductOut(
        slug="femmelia",
        sku=SLUG_TO_SKU["femmelia"],
        name_ar=SLUG_TO_NAME_AR["femmelia"],
        name_en="Femmélia",
        unit_price_sar=FEMMELIA_TIER_PRICES[1],
        unit_price_mad=FEMMELIA_TIER_PRICES[1],
        cross_sell_slugs=["clarelia", "luminora", "capilys"],
    ),
    ProductOut(
        slug="capilys",
        sku=SLUG_TO_SKU["capilys"],
        name_ar=SLUG_TO_NAME_AR["capilys"],
        name_en="Capilys",
        unit_price_sar=TIER_PRICES[1],
        unit_price_mad=TIER_PRICES[1],
        cross_sell_slugs=["luminora", "clarelia", "femmelia"],
    ),
    ProductOut(
        slug="luminora",
        sku=SLUG_TO_SKU["luminora"],
        name_ar=SLUG_TO_NAME_AR["luminora"],
        name_en="Luminora",
        unit_price_sar=TIER_PRICES[1],
        unit_price_mad=TIER_PRICES[1],
        cross_sell_slugs=["clarelia", "capilys", "femmelia"],
    ),
]


@router.get("/products", response_model=list[ProductOut])
def list_products() -> list[ProductOut]:
    return PRODUCTS
