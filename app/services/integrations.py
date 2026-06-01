"""Optional Google Sheets and CAPI integrations — no-op when env is empty."""

import json
import logging
import re

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


def normalize_sheets_webhook_url(url: str) -> str:
    """Use /exec deployment URL, not /dev."""
    u = url.strip()
    if "/macros/s/" in u and u.rstrip("/").endswith("/dev"):
        u = re.sub(r"/dev/?$", "/exec", u.rstrip("/"))
    return u


def _resolve_redirect_url(response: httpx.Response, location: str) -> str:
    if location.startswith("http://") or location.startswith("https://"):
        return location
    return str(response.url.join(location))


def _parse_sheets_http_response(resp: httpx.Response, orderid: str) -> tuple[bool, str | None]:
    text = (resp.text or "").strip()
    if resp.status_code >= 400:
        return False, f"HTTP {resp.status_code}: {text[:200]}"

    if not text:
        return False, "Empty response from Google Apps Script"

    if text.startswith("<"):
        return False, "Got HTML instead of JSON — redeploy Web app (Anyone) and use /exec URL"

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        return False, f"Invalid JSON: {text[:200]}"

    if not result.get("success"):
        err = result.get("error") or result
        return False, str(err)[:300]

    logger.info("Google Sheets OK orderid=%s", orderid)
    return True, None


async def sync_order_to_sheets(payload: dict) -> tuple[bool, str | None]:
    """
    POST order row to Google Apps Script web app.
    Returns (synced, error_message).
    """
    if not settings.sheets_enabled:
        msg = "GOOGLE_SHEETS_WEBHOOK_URL is empty"
        logger.warning("%s — order %s", msg, payload.get("orderid"))
        return False, msg

    url = normalize_sheets_webhook_url(settings.GOOGLE_SHEETS_WEBHOOK_URL)
    body_str = json.dumps(payload, ensure_ascii=False)
    orderid = payload.get("orderid", "?")
    last_error: str | None = None

    async with httpx.AsyncClient(timeout=30.0) as client:
        attempts: list[tuple[str, dict]] = [
            (
                "form+redirect",
                {"data": {"payload": body_str}, "follow_redirects": True},
            ),
            (
                "json+redirect",
                {
                    "content": body_str,
                    "headers": {"Content-Type": "application/json"},
                    "follow_redirects": True,
                },
            ),
        ]

        for name, kwargs in attempts:
            try:
                resp = await client.post(url, **kwargs)
                ok, err = _parse_sheets_http_response(resp, orderid)
                if ok:
                    return True, None
                last_error = f"{name}: {err}"
                logger.warning("Sheets attempt failed (%s) orderid=%s: %s", name, orderid, err)
            except Exception as exc:
                last_error = f"{name}: {exc}"
                logger.warning("Sheets attempt exception (%s) orderid=%s: %s", name, orderid, exc)

        # Manual redirect replay (302 body loss workaround)
        try:
            resp = await client.post(
                url, data={"payload": body_str}, follow_redirects=False
            )
            if resp.status_code in (301, 302, 303, 307, 308):
                location = resp.headers.get("location")
                if location:
                    target = _resolve_redirect_url(resp, location)
                    resp = await client.post(
                        target, data={"payload": body_str}, follow_redirects=False
                    )
            ok, err = _parse_sheets_http_response(resp, orderid)
            if ok:
                return True, None
            last_error = f"manual-redirect: {err}"
        except Exception as exc:
            last_error = f"manual-redirect: {exc}"

    logger.error("Google Sheets sync failed orderid=%s: %s", orderid, last_error)
    return False, last_error


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
