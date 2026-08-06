from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()

        return order

    def create_item(self, item: OrderItem) -> OrderItem:
        self.db.add(item)
        self.db.flush()

        return item

    def get_all(self) -> list[Order]:
        stmt = select(Order).where(
            Order.deleted_at.is_(None)
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def get_by_id(
        self,
        order_id: int,
    ) -> Order | None:

        stmt = select(Order).where(
            Order.id == order_id,
            Order.deleted_at.is_(None),
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()