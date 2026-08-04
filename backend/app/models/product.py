from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin


class Product(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150))

    description: Mapped[str]

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    image_url: Mapped[str | None]

    inventory: Mapped[int] = mapped_column(
    nullable=False,
    default=0,
)

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products",
    )