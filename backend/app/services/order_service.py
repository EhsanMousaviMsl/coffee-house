from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.exceptions import (
    InsufficientInventoryError,
    OrderNotFoundError,
    ProductNotFoundError,
    ProductUnavailableError,
    OrderAlreadyCancelledError,
    OrderCannotBeCancelledError,
    OrderCannotBeConfirmedError,
)
from app.models.order import Order, OrderStatus
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
                product = self.product_repository.get_by_id_for_update(
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


    def get_all_orders(self) -> list[Order]:
        return self.order_repository.get_all()
    
    def get_order_by_id(
        self,
        order_id: int,
    ) -> Order:

        order = self.order_repository.get_by_id(
            order_id
        )

        if order is None:
            raise OrderNotFoundError(order_id)

        return order
    
    def cancel_order(
        self,
        order_id: int,
    ) -> Order:

        try:
            # 1. Find order
            order = self.order_repository.get_by_id(
                order_id
            )

            if order is None:
                raise OrderNotFoundError(order_id)

            # 2. Check status
            if order.status == OrderStatus.CANCELLED:
                raise OrderAlreadyCancelledError(order_id)

            if not order.can_be_cancelled():
                raise OrderCannotBeCancelledError(
                    order_id,
                    order.status.value,
                )           

            # 3. Restore inventory
            for item in order.items:

                product = self.product_repository.get_by_id_for_update(
                    item.product_id
                )

                if product is None:
                    raise ProductNotFoundError(
                        item.product_id
                    )

                self.product_repository.increase_inventory(
                    product,
                    item.quantity,
                )

            # 4. Change order status
            order.status = OrderStatus.CANCELLED

            self.order_repository.update(order)

            # 5. Commit everything
            self.db.commit()

            # 6. Refresh
            self.db.refresh(order)

            return order

        except Exception:
            self.db.rollback()
            raise


    def confirm_order(
        self,
        order_id: int,
    ) -> Order:

        try:
            # 1. Find order
            order = self.order_repository.get_by_id(
                order_id
            )

            if order is None:
                raise OrderNotFoundError(order_id)

            # 2. Order must be pending
            if not order.can_be_confirmed():
                raise OrderCannotBeConfirmedError(
                    order_id,
                    order.status.value,
            )

            # 3. Change status
            order.status = OrderStatus.CONFIRMED

            self.order_repository.update(order)

            # 4. Commit
            self.db.commit()

            # 5. Refresh
            self.db.refresh(order)

            return order

        except Exception:
            self.db.rollback()
            raise