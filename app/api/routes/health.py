from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "sheets_webhook_configured": settings.sheets_enabled,
        "order_number_prefix": settings.ORDER_NUMBER_PREFIX,
    }
