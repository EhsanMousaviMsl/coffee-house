from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import (
    InsufficientInventoryError,
    ProductNotFoundError,
    ProductUnavailableError,
)
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate


class OrderService:

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        db: Session,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.db = db

    def create_order(
        self,
        data: OrderCreate,
    ) -> Order:

        total_price = Decimal("0")

        quantities: dict[int, int] = {}

        for item in data.items:
            quantities[item.product_id] = (
                quantities.get(item.product_id, 0)
                + item.quantity
            )

        order = Order(
            total_price=Decimal("0"),
        )

        try:
            self.order_repository.create(order)

            for product_id, quantity in quantities.items():

                # 1. Find product
                product = self.product_repository.get_by_id(
                    product_id
                )

                if product is None:
                    raise ProductNotFoundError(
                        product_id
                    )

                # 2. Check availability
                if not product.available:
                    raise ProductUnavailableError(
                        product.id
                    )

                # 3. Check inventory
                if product.inventory < quantity:
                    raise InsufficientInventoryError(
                        product.id,
                        quantity,
                        product.inventory,
                    )

                # 4. Calculate item price
                item_total = product.price * quantity
                total_price += item_total

                # 5. Create OrderItem
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                )

                self.order_repository.create_item(
                    order_item
                )

                # 6. Reduce inventory
                self.product_repository.decrease_inventory(
                    product,
                    quantity,
                )

            # 7. Set final order total
            order.total_price = total_price

            # 8. Commit
            self.db.commit()

            # 9. Refresh
            self.db.refresh(order)

            return order

        except Exception:
            self.db.rollback()
            raise