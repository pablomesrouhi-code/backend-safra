"""Optional Google Sheets and CAPI integrations — no-op when env is empty."""

import json
import logging
import re
from urllib.parse import quote

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


def normalize_sheets_webhook_url(url: str) -> str:
    """Use /exec deployment URL, not /dev."""
    u = url.strip()
    if "/macros/s/" in u and u.rstrip("/").endswith("/dev"):
        u = re.sub(r"/dev/?$", "/exec", u.rstrip("/"))
    return u


def validate_sheets_webhook_url(url: str) -> str | None:
    """Return error message if URL format is wrong."""
    u = url.strip()
    if not u:
        return "GOOGLE_SHEETS_WEBHOOK_URL is empty"
    if "docs.google.com/spreadsheets" in u or "spreadsheets/d/" in u:
        return (
            "Wrong URL: you pasted the Sheet link. "
            "Use Apps Script Deploy → Web app URL ending in /exec"
        )
    if "script.google.com/macros" not in u:
        return (
            "Wrong URL: must be https://script.google.com/macros/s/.../exec "
            "(from Apps Script → Deploy → Web app)"
        )
    if "/exec" not in u and "/dev" not in u:
        return "Wrong URL: must end with /exec (Web app deployment URL)"
    return None


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
    Send order to Google Apps Script.
    GET ?payload= first (avoids HTTP 405 on POST redirect).
    """
    if not settings.sheets_enabled:
        msg = "GOOGLE_SHEETS_WEBHOOK_URL is empty"
        logger.warning("%s — order %s", msg, payload.get("orderid"))
        return False, msg

    raw_url = settings.GOOGLE_SHEETS_WEBHOOK_URL
    url_error = validate_sheets_webhook_url(raw_url)
    if url_error:
        logger.error("%s — order %s", url_error, payload.get("orderid"))
        return False, url_error

    url = normalize_sheets_webhook_url(raw_url)
    body_str = json.dumps(payload, ensure_ascii=False)
    orderid = payload.get("orderid", "?")
    last_error: str | None = None

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1) GET with payload query (most reliable for Apps Script)
        try:
            get_url = f"{url}?payload={quote(body_str)}"
            resp = await client.get(get_url, follow_redirects=True)
            ok, err = _parse_sheets_http_response(resp, orderid)
            if ok:
                return True, None
            last_error = f"GET: {err}"
            logger.warning("Sheets GET failed orderid=%s: %s", orderid, err)
        except Exception as exc:
            last_error = f"GET: {exc}"
            logger.warning("Sheets GET exception orderid=%s: %s", orderid, exc)

        # 2) POST form
        try:
            resp = await client.post(
                url,
                data={"payload": body_str},
                follow_redirects=True,
            )
            ok, err = _parse_sheets_http_response(resp, orderid)
            if ok:
                return True, None
            last_error = f"POST: {err}"
        except Exception as exc:
            last_error = f"POST: {exc}"

    if last_error and "is not defined" in last_error:
        last_error = (
            f"{last_error} — Replace ALL Apps Script code and Deploy > New deployment"
        )
    if last_error and "404" in last_error:
        last_error = (
            "Webhook URL returns 404 (wrong or old deployment). "
            "Apps Script → Deploy → New deployment → copy new /exec URL → "
            "update GOOGLE_SHEETS_WEBHOOK_URL in Easypanel → Redeploy backend"
        )

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
