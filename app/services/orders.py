import logging
import random
import string

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.order import Order, OrderItem
from app.schemas.order import CreateOrderRequest
from app.services.geoip import lookup_ip
from app.services.integrations import fire_purchase_events, sync_order_to_sheets
from app.services.phone import normalize_ma_phone
from app.services.pricing import (
    SLUG_TO_NAME_AR,
    VALID_SKUS,
    calculate_grand_total,
    offer_price,
    slug_for_sku,
)
from app.services.sheets import build_sheets_payload

logger = logging.getLogger(__name__)


class OrderValidationError(ValueError):
    def __init__(self, detail: str, code: str = "VALIDATION_ERROR"):
        self.detail = detail
        self.code = code
        super().__init__(detail)


def generate_order_number() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{settings.ORDER_NUMBER_PREFIX}{suffix}"


def validate_and_price(payload: CreateOrderRequest) -> dict:
    if not payload.items:
        raise OrderValidationError("السلة فارغة", "EMPTY_CART")

    slugs: list[str] = []
    line_items: list[dict] = []
    merchandise = 0

    for item in payload.items:
        sku = item.sku.strip().upper()
        if sku not in VALID_SKUS:
            raise OrderValidationError(f"منتج غير معروف: {sku}", "INVALID_SKU")
        if item.qty < 1:
            raise OrderValidationError("الكمية غير صالحة", "INVALID_QTY")

        slug = slug_for_sku(sku)
        assert slug is not None
        slugs.append(slug)
        line_total = offer_price(item.qty)
        merchandise += line_total
        line_items.append(
            {
                "sku": sku,
                "product_slug": slug,
                "quantity": item.qty,
                "unit_reference_price_sar": line_total,
            }
        )

    upsell_accepted = bool(payload.upsell_sku)
    upsell_price = 0
    upsell_sku_norm: str | None = None

    if upsell_accepted:
        upsell_sku_norm = payload.upsell_sku.strip().upper()
        if upsell_sku_norm not in VALID_SKUS:
            raise OrderValidationError("منتج الإضافة غير صالح", "INVALID_UPSELL")
        expected = settings.UPSELL_PRICE_MAD
        incoming = (
            payload.upsell_price_mad
            if payload.upsell_price_mad is not None
            else payload.upsell_price_sar
        )
        if incoming is not None and incoming != expected:
            raise OrderValidationError("سعر الإضافة غير صحيح", "PRICE_MISMATCH")
        upsell_price = expected

    grand_total = calculate_grand_total(merchandise, upsell_accepted, upsell_price)
    tier_count = min(max(sum(item.qty for item in payload.items), 1), 3)

    return {
        "line_items": line_items,
        "tier_count": tier_count,
        "tier_total_sar": merchandise,
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

    try:
        e164, display = normalize_ma_phone(payload.customer_phone)
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

    sheets_payload = build_sheets_payload(
        order,
        priced["line_items"],
        upsell_accepted=priced["upsell_accepted"],
        upsell_sku=order.upsell_sku,
        slug_for_sku=slug_for_sku,
        slug_to_name_ar=SLUG_TO_NAME_AR,
    )
    sheets_sync_error: str | None = None
    if settings.sheets_enabled:
        synced, sheets_sync_error = await sync_order_to_sheets(sheets_payload)
        if synced:
            order.sheets_synced = True
            db.commit()
    else:
        logger.info("Sheets webhook not set — order %s saved in database only", order.order_number)

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

    order.sheets_sync_error = sheets_sync_error  # type: ignore[attr-defined]
    return order
