from fastapi import APIRouter

from app.schemas.product import ProductOut

router = APIRouter(prefix="/api/v1", tags=["products"])

PRODUCTS: list[ProductOut] = [
    ProductOut(
        slug="freshguard",
        sku="SS-FRESHGUARD-01",
        name_ar="نفس واثق",
        name_en="FreshGuard Oral Protocol",
        unit_price_sar=199,
        cross_sell_slugs=["heatshield", "underguard"],
    ),
    ProductOut(
        slug="heatshield",
        sku="SS-HEATSHIELD-02",
        name_ar="درع الحر",
        name_en="HeatShield Body Powder",
        unit_price_sar=199,
        cross_sell_slugs=["freshguard", "underguard"],
    ),
    ProductOut(
        slug="underguard",
        sku="SS-UNDERGUARD-03",
        name_ar="ثقة الإبط",
        name_en="UnderGuard Deodorant Duo",
        unit_price_sar=199,
        cross_sell_slugs=["freshguard", "heatshield"],
    ),
]


@router.get("/products", response_model=list[ProductOut])
def list_products() -> list[ProductOut]:
    return PRODUCTS
