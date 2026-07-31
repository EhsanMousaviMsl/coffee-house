from app.db.mixins import TimestampMixin, SoftDeleteMixin
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True)

    image_url: Mapped[str | None]


    products = relationship(
        "Product",
        back_populates="category",
    )