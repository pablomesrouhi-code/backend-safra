import random
import string
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.order import Order, OrderItem
from app.schemas.order import CreateOrderRequest
from app.services.geoip import lookup_ip
from app.services.integrations import fire_purchase_events, sync_order_to_sheets
from app.services.phone import normalize_ksa_phone
from app.services.pricing import (
    VALID_SKUS,
    calculate_grand_total,
    calculate_tier,
    slug_for_sku,
)


class OrderValidationError(ValueError):
    def __init__(self, detail: str, code: str = "VALIDATION_ERROR"):
        self.detail = detail
        self.code = code
        super().__init__(detail)


def generate_order_number() -> str:
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    prefix = settings.ORDER_NUMBER_PREFIX
    return f"{prefix}-{date_part}-{suffix}"


def validate_and_price(payload: CreateOrderRequest) -> dict:
    if not payload.items:
        raise OrderValidationError("السلة فارغة", "EMPTY_CART")

    slugs: list[str] = []
    line_items: list[dict] = []

    for item in payload.items:
        sku = item.sku.strip().upper()
        if sku not in VALID_SKUS:
            raise OrderValidationError(f"منتج غير معروف: {sku}", "INVALID_SKU")
        if item.qty < 1:
            raise OrderValidationError("الكمية غير صالحة", "INVALID_QTY")

        slug = slug_for_sku(sku)
        assert slug is not None
        slugs.append(slug)
        line_items.append(
            {
                "sku": sku,
                "product_slug": slug,
                "quantity": item.qty,
                "unit_reference_price_sar": 199,
            }
        )

    upsell_accepted = bool(payload.upsell_sku)
    upsell_price = 0
    upsell_sku_norm: str | None = None

    if upsell_accepted:
        upsell_sku_norm = payload.upsell_sku.strip().upper()
        if upsell_sku_norm not in VALID_SKUS:
            raise OrderValidationError("منتج الإضافة غير صالح", "INVALID_UPSELL")
        expected = settings.UPSELL_PRICE_SAR
        if payload.upsell_price_sar is not None and payload.upsell_price_sar != expected:
            raise OrderValidationError("سعر الإضافة غير صحيح", "PRICE_MISMATCH")
        upsell_price = expected

    total_qty = sum(item.qty for item in payload.items)
    tier_count, tier_total = calculate_tier(slugs, total_qty)
    grand_total = calculate_grand_total(tier_total, upsell_accepted, upsell_price)

    return {
        "line_items": line_items,
        "tier_count": tier_count,
        "tier_total_sar": tier_total,
        "upsell_accepted": upsell_accepted,
        "upsell_sku": upsell_sku_norm,
        "upsell_price_sar": upsell_price if upsell_accepted else None,
        "grand_total_sar": grand_total,
    }


async def create_order(
    db: Session,
    payload: CreateOrderRequest,
    *,
    client_ip: str | None = None,
) -> Order:
    geo = lookup_ip(client_ip)
    if settings.GEOIP_ENFORCE_KSA and client_ip and geo.get("country_code") not in (None, "SA"):
        raise OrderValidationError(
            "الطلبات متاحة داخل المملكة فقط",
            "GEO_NOT_KSA",
        )

    try:
        e164, display = normalize_ksa_phone(payload.customer_phone)
    except ValueError as exc:
        code = getattr(exc, "code", "INVALID_PHONE")
        raise OrderValidationError(str(exc), code) from exc

    priced = validate_and_price(payload)
    order_number = generate_order_number()

    order = Order(
        order_number=order_number,
        customer_name=payload.customer_name.strip(),
        customer_phone=e164,
        customer_phone_display=display,
        tier_count=priced["tier_count"],
        tier_total_sar=priced["tier_total_sar"],
        upsell_accepted=priced["upsell_accepted"],
        upsell_sku=priced["upsell_sku"],
        upsell_price_sar=priced["upsell_price_sar"],
        grand_total_sar=priced["grand_total_sar"],
        payment_method="COD",
        status="pending_confirmation",
    )
    db.add(order)
    db.flush()

    for line in priced["line_items"]:
        db.add(
            OrderItem(
                order_id=order.id,
                product_slug=line["product_slug"],
                sku=line["sku"],
                quantity=line["quantity"],
                unit_reference_price_sar=line["unit_reference_price_sar"],
            )
        )

    db.commit()
    db.refresh(order)

    sheets_payload = {
        "order_id": order.order_number,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "grand_total_sar": order.grand_total_sar,
        "tier_total_sar": order.tier_total_sar,
        "items": priced["line_items"],
        "upsell_sku": order.upsell_sku,
    }
    synced = await sync_order_to_sheets(sheets_payload)
    if synced:
        order.sheets_synced = True
        db.commit()

    await fire_purchase_events(
        {
            "order_id": order.order_number,
            "grand_total_sar": order.grand_total_sar,
            "customer_phone": order.customer_phone,
            "client_ip": client_ip,
            "country_code": geo.get("country_code"),
            "country_name": geo.get("country_name"),
        }
    )

    return order
