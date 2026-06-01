from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    db_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    return {
        "status": "ok" if db_ok else "degraded",
        "database": db_ok,
        "sheets_webhook_configured": settings.sheets_enabled,
        "order_number_prefix": settings.ORDER_NUMBER_PREFIX,
    }
