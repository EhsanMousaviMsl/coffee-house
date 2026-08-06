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