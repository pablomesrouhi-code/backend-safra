import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    order_number: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(200))
    customer_phone: Mapped[str] = mapped_column(String(20), index=True)
    customer_phone_display: Mapped[str] = mapped_column(String(20))
    tier_count: Mapped[int] = mapped_column(Integer)
    tier_total_sar: Mapped[int] = mapped_column(Integer)
    upsell_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    upsell_sku: Mapped[str | None] = mapped_column(String(50), nullable=True)
    upsell_price_sar: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grand_total_sar: Mapped[int] = mapped_column(Integer)
    payment_method: Mapped[str] = mapped_column(String(20), default="COD")
    status: Mapped[str] = mapped_column(String(30), default="pending_confirmation")
    sheets_synced: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"), index=True)
    product_slug: Mapped[str] = mapped_column(String(50))
    sku: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_reference_price_sar: Mapped[int] = mapped_column(Integer, default=199)

    order: Mapped["Order"] = relationship(back_populates="items")
