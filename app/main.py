import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, orders, products
from app.core.config import settings
from app.core.database import init_db, mask_database_url, normalized_database_url
from app.services.geoip import init_geoip
from app.services.orders import OrderValidationError

logging.basicConfig(level=logging.INFO)


def _init_db_with_retry(max_attempts: int = 20, delay_sec: float = 3.0) -> None:
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            init_db()
            logging.info("Database ready (attempt %s)", attempt)
            return
        except Exception as exc:
            last_err = exc
            logging.warning(
                "Database not ready (attempt %s/%s): %s",
                attempt,
                max_attempts,
                exc,
            )
            if attempt < max_attempts:
                time.sleep(delay_sec)
    raise RuntimeError(f"Database init failed after {max_attempts} attempts") from last_err


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logging.info("DATABASE_URL (masked): %s", mask_database_url(normalized_database_url()))
    _init_db_with_retry()
    try:
        init_geoip()
    except Exception:
        logging.exception("GeoIP init failed; API will run without MaxMind")
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
