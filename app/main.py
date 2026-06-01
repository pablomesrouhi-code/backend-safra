import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, orders, products
from app.core.config import settings
from app.core.database import mask_database_url, normalized_database_url, try_init_db
from app.services.geoip import init_geoip
from app.services.orders import OrderValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _database_warmup_loop() -> None:
    """Connect to Postgres in background so API starts fast (no 502 while DB boots)."""
    for attempt in range(1, 31):
        if try_init_db():
            logger.info("Database connected on attempt %s", attempt)
            return
        await asyncio.sleep(2)
    logger.error(
        "DATABASE STILL DOWN after 60s. Fix DATABASE_URL in Easypanel:\n"
        "  postgres://postgres:PASSWORD@safraskin_database:5432/safraskin?sslmode=disable"
    )


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Safra Skin API starting")
    logger.info("DATABASE_URL (masked): %s", mask_database_url(normalized_database_url()))
    asyncio.create_task(_database_warmup_loop())
    try:
        init_geoip()
    except Exception:
        logger.exception("GeoIP init failed; API will run without MaxMind")
    yield


app = FastAPI(
    title="Safra Skin API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.exception_handler(OrderValidationError)
async def order_validation_handler(_request: Request, exc: OrderValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail, "code": exc.code},
    )


@app.exception_handler(RuntimeError)
async def runtime_error_handler(_request: Request, exc: RuntimeError) -> JSONResponse:
    if "Database not ready" in str(exc):
        return JSONResponse(
            status_code=503,
            content={
                "detail": "قاعدة البيانات غير متصلة. تحقق من DATABASE_URL في Easypanel.",
                "code": "DATABASE_NOT_READY",
            },
        )
    raise exc
