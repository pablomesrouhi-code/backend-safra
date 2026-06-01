from fastapi import APIRouter

from app.core.config import settings
from app.core.database import is_db_ready, mask_database_url, normalized_database_url, try_init_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    db_ok = is_db_ready() or try_init_db()

    return {
        "status": "ok" if db_ok else "degraded",
        "database": db_ok,
        "database_url_scheme": mask_database_url(normalized_database_url()).split("://")[0],
        "sheets_webhook_configured": settings.sheets_enabled,
        "order_number_prefix": settings.ORDER_NUMBER_PREFIX,
    }
