"""Optional Google Sheets and CAPI integrations — no-op when env is empty."""

import json
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def _post_with_redirect(
    client: httpx.AsyncClient,
    url: str,
    *,
    data: dict | None = None,
    content: str | None = None,
    headers: dict | None = None,
) -> httpx.Response:
    """Google Apps Script /exec 302s to googleusercontent.com — replay POST to Location."""
    resp = await client.post(url, data=data, content=content, headers=headers, follow_redirects=False)
    if resp.status_code in (301, 302, 303, 307, 308):
        location = resp.headers.get("location")
        if location:
            resp = await client.post(
                location, data=data, content=content, headers=headers, follow_redirects=False
            )
    return resp


async def sync_order_to_sheets(payload: dict) -> bool:
    if not settings.sheets_enabled:
        logger.warning(
            "GOOGLE_SHEETS_WEBHOOK_URL is empty — order %s saved in DB but NOT sent to Sheet",
            payload.get("orderid"),
        )
        return False

    url = settings.GOOGLE_SHEETS_WEBHOOK_URL.strip()
    body_str = json.dumps(payload, ensure_ascii=False)

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            # Form field survives Google redirect better than raw JSON POST
            resp = await _post_with_redirect(client, url, data={"payload": body_str})

            if resp.status_code >= 400:
                logger.error(
                    "Google Sheets HTTP %s orderid=%s body=%s",
                    resp.status_code,
                    payload.get("orderid"),
                    (resp.text or "")[:500],
                )
                return False

            text = (resp.text or "").strip()
            try:
                result = json.loads(text) if text else {}
            except json.JSONDecodeError:
                logger.error(
                    "Google Sheets non-JSON orderid=%s body=%s",
                    payload.get("orderid"),
                    text[:500],
                )
                return False

            if not result.get("success"):
                logger.error(
                    "Google Sheets error orderid=%s response=%s",
                    payload.get("orderid"),
                    result,
                )
                return False

        logger.info("Google Sheets OK orderid=%s", payload.get("orderid"))
        return True
    except Exception:
        logger.exception("Google Sheets sync failed orderid=%s", payload.get("orderid"))
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
