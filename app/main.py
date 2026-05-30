import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, orders, products
from app.core.config import settings
from app.core.database import init_db
from app.services.geoip import init_geoip
from app.services.orders import OrderValidationError

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
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
