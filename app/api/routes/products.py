from fastapi import APIRouter

from app.schemas.product import ProductOut
from app.services.pricing import SLUG_TO_NAME_AR, SLUG_TO_SKU

router = APIRouter(prefix="/api/v1", tags=["products"])

PRODUCTS: list[ProductOut] = [
    ProductOut(
        slug="cyclecalm",
        sku=SLUG_TO_SKU["cyclecalm"],
        name_ar=SLUG_TO_NAME_AR["cyclecalm"],
        name_en="Cycle Calm PMS Gummies",
        unit_price_sar=199,
        cross_sell_slugs=["oralflora", "clearbalance"],
    ),
    ProductOut(
        slug="oralflora",
        sku=SLUG_TO_SKU["oralflora"],
        name_ar=SLUG_TO_NAME_AR["oralflora"],
        name_en="Oral Flora Probiotic Gummies",
        unit_price_sar=199,
        cross_sell_slugs=["cyclecalm", "clearbalance"],
    ),
    ProductOut(
        slug="clearbalance",
        sku=SLUG_TO_SKU["clearbalance"],
        name_ar=SLUG_TO_NAME_AR["clearbalance"],
        name_en="Clear Balance Skin Gummies",
        unit_price_sar=199,
        cross_sell_slugs=["cyclecalm", "oralflora"],
    ),
]


@router.get("/products", response_model=list[ProductOut])
def list_products() -> list[ProductOut]:
    return PRODUCTS
