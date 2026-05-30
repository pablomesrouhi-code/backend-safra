"""Optional Google Sheets and CAPI integrations — no-op when env is empty."""

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def sync_order_to_sheets(payload: dict) -> bool:
    if not settings.sheets_enabled:
        logger.debug("Google Sheets webhook not configured; skipping sync")
        return False

    body = {**payload}
    if settings.GOOGLE_SHEETS_SECRET:
        body["secret"] = settings.GOOGLE_SHEETS_SECRET

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(settings.GOOGLE_SHEETS_WEBHOOK_URL, json=body)
            resp.raise_for_status()
        return True
    except Exception:
        logger.exception("Google Sheets sync failed")
        return False


async def fire_purchase_events(order_payload: dict) -> None:
    geo_hint = ""
    if order_payload.get("country_code"):
        geo_hint = f" country={order_payload['country_code']}"
    if settings.meta_capi_enabled:
        logger.info(
            "Meta CAPI stub: Purchase %s ip=%s%s",
            order_payload.get("order_id"),
            order_payload.get("client_ip"),
            geo_hint,
        )
    if settings.tiktok_capi_enabled:
        logger.info("TikTok CAPI stub: would send Purchase for %s", order_payload.get("order_id"))
    if settings.snap_capi_enabled:
        logger.info("Snap CAPI stub: would send Purchase for %s", order_payload.get("order_id"))

    if not (
        settings.meta_capi_enabled
        or settings.tiktok_capi_enabled
        or settings.snap_capi_enabled
    ):
        logger.debug("No CAPI credentials configured; skipping purchase events")
