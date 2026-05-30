from pydantic import BaseModel


class ProductOut(BaseModel):
    slug: str
    sku: str
    name_ar: str
    name_en: str
    unit_price_sar: int
    cross_sell_slugs: list[str]
