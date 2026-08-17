from pydantic import BaseModel, Field


class OrderItemInput(BaseModel):
    sku: str
    qty: int = Field(ge=1)


class CreateOrderRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=200)
    customer_phone: str
    items: list[OrderItemInput] = Field(min_length=1)
    upsell_sku: str | None = None
    upsell_price_mad: int | None = None
    upsell_price_sar: int | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    session_id: str | None = None


class CreateOrderResponse(BaseModel):
    order_id: str
    grand_total_sar: int
    grand_total_mad: int
    tier_total_sar: int
    upsell_total_sar: int
    upsell_total_mad: int
    status: str
    thank_you_path: str
    sheets_synced: bool = False
    sheets_sync_error: str | None = None
