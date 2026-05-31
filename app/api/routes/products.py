from fastapi import APIRouter

from app.schemas.product import ProductOut

router = APIRouter(prefix="/api/v1", tags=["products"])

PRODUCTS: list[ProductOut] = [
    ProductOut(
        slug="cyclecalm",
        sku="BL-CYCLE-01",
        name_ar="هدوء الدورة",
        name_en="Cycle Calm PMS Gummies",
        unit_price_sar=199,
        cross_sell_slugs=["oralflora", "clearbalance"],
    ),
    ProductOut(
        slug="oralflora",
        sku="BL-ORAL-02",
        name_ar="فلورا الفم",
        name_en="Oral Flora Probiotic Gummies",
        unit_price_sar=199,
        cross_sell_slugs=["cyclecalm", "clearbalance"],
    ),
    ProductOut(
        slug="clearbalance",
        sku="BL-SKIN-03",
        name_ar="توازن البشرة",
        name_en="Clear Balance Skin Gummies",
        unit_price_sar=199,
        cross_sell_slugs=["cyclecalm", "oralflora"],
    ),
]


@router.get("/products", response_model=list[ProductOut])
def list_products() -> list[ProductOut]:
    return PRODUCTS
