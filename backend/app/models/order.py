from enum import Enum
from decimal import Decimal

from sqlalchemy import Enum as SQLEnum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
    )

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
    )

    payments = relationship(
        "Payment",
        back_populates="order",
    )

    def can_be_cancelled(self) -> bool:
        return self.status == OrderStatus.PENDING
    
    def can_be_confirmed(self) -> bool:
        return self.status == OrderStatus.PENDING