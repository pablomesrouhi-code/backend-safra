from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.request_ip import client_ip_from_request
from app.schemas.order import CreateOrderRequest, CreateOrderResponse
from app.services.orders import create_order

router = APIRouter(prefix="/api/v1", tags=["orders"])


@router.post("/orders", response_model=CreateOrderResponse)
async def post_order(
    payload: CreateOrderRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> CreateOrderResponse:
    client_ip = client_ip_from_request(request)
    order = await create_order(db, payload, client_ip=client_ip)
    upsell_total = order.upsell_price_sar or 0
    return CreateOrderResponse(
        order_id=order.order_number,
        grand_total_sar=order.grand_total_sar,
        tier_total_sar=order.tier_total_sar,
        upsell_total_sar=upsell_total,
        status=order.status,
        thank_you_path=f"/thank-you/{order.order_number}",
    )
