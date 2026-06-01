import httpx
from fastapi import APIRouter

from app.core.config import settings
from app.core.database import is_db_ready, mask_database_url, normalized_database_url, try_init_db
from app.services.integrations import normalize_sheets_webhook_url, validate_sheets_webhook_url

router = APIRouter(tags=["health"])


def _check_sheets_webhook() -> dict:
    if not settings.sheets_enabled:
        return {"configured": False, "reachable": False, "hint": "Set GOOGLE_SHEETS_WEBHOOK_URL"}

    fmt_err = validate_sheets_webhook_url(settings.GOOGLE_SHEETS_WEBHOOK_URL)
    if fmt_err:
        return {"configured": True, "reachable": False, "hint": fmt_err}

    url = normalize_sheets_webhook_url(settings.GOOGLE_SHEETS_WEBHOOK_URL)
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(url, follow_redirects=True)
        text = (resp.text or "").strip()[:300]
        if resp.status_code == 404 or text.startswith("<!DOCTYPE"):
            return {
                "configured": True,
                "reachable": False,
                "http_status": resp.status_code,
                "hint": "404 — wrong URL. Apps Script → Deploy → New deployment → copy /exec URL",
            }
        if '"status":"ok"' in text.replace(" ", "") or '"status": "ok"' in text:
            return {"configured": True, "reachable": True, "http_status": resp.status_code}
        return {
            "configured": True,
            "reachable": False,
            "http_status": resp.status_code,
            "hint": f"Unexpected response: {text[:120]}",
        }
    except Exception as exc:
        return {"configured": True, "reachable": False, "hint": str(exc)}


@router.get("/health")
def health() -> dict:
    db_ok = is_db_ready() or try_init_db()
    sheets = _check_sheets_webhook()

    return {
        "status": "ok" if db_ok else "degraded",
        "database": db_ok,
        "database_url_scheme": mask_database_url(normalized_database_url()).split("://")[0],
        "sheets_webhook_configured": settings.sheets_enabled,
        "sheets_webhook_reachable": sheets.get("reachable"),
        "sheets_webhook_hint": sheets.get("hint"),
        "order_number_prefix": settings.ORDER_NUMBER_PREFIX,
    }
