"""Build Google Sheets webhook row payload (Safra Skin ops format)."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.order import Order

KSA_TZ = ZoneInfo("Asia/Riyadh")


def format_phone_for_sheets(e164: str) -> str:
    """96650475233 — no plus sign."""
    return (e164 or "").lstrip("+")


def build_sheets_payload(
    order: Order,
    line_items: list[dict],
    *,
    upsell_accepted: bool,
    upsell_sku: str | None,
    slug_for_sku,
    slug_to_name_ar: dict[str, str],
) -> dict:
    """One row matching Sheet columns: date → status (status left empty)."""
    sheet_lines = list(line_items)

    if upsell_accepted and upsell_sku:
        upsell_slug = slug_for_sku(upsell_sku)
        if upsell_slug:
            sheet_lines.append(
                {
                    "sku": upsell_sku.upper(),
                    "product_slug": upsell_slug,
                    "quantity": 1,
                }
            )

    product_names: list[str] = []
    skus: list[str] = []
    quantities: list[str] = []

    for line in sheet_lines:
        slug = line["product_slug"]
        product_names.append(slug_to_name_ar.get(slug, slug))
        skus.append(line["sku"])
        quantities.append(str(line["quantity"]))

    now_ksa = datetime.now(KSA_TZ)

    return {
        "date": now_ksa.strftime("%d/%m/%Y"),
        "orderid": order.order_number,
        "country": "KSA",
        "name": order.customer_name,
        "phone": format_phone_for_sheets(order.customer_phone),
        "product": "/".join(product_names),
        "sku": "/".join(skus),
        "quantity": "/".join(quantities),
        "total_price": order.grand_total_sar,
        "currency": "SAR",
        "status": "",
    }
