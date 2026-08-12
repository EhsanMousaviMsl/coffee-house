from sqlalchemy.orm import Session

from app.core.exceptions import (
    OrderCannotBePaidError,
    OrderNotFoundError,
    OrderCannotBeConfirmedError,
    PaymentAlreadyExistsError,
    PaymentAlreadyFailedError,
    PaymentNotFoundError,
    PaymentAlreadySucceededError,
)
from app.models.order import OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository


class PaymentService:

    def __init__(
        self,
        payment_repository: PaymentRepository,
        order_repository: OrderRepository,
        db: Session,
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository
        self.db = db

    def create_payment(
        self,
        order_id: int,
    ) -> Payment:

        try:
            # 1. Find order
            order = self.order_repository.get_by_id(
                order_id
            )

            if order is None:
                raise OrderNotFoundError(order_id)

            # 2. Order must be pending
            if order.status != OrderStatus.PENDING:
                raise OrderCannotBePaidError(
                    order_id,
                    order.status.value,
                )

            # 3. Make sure there isn't already
            # a pending payment attempt
            pending_payment = (
                self.payment_repository.get_pending_by_order_id(
                    order_id
                )
            )

            if pending_payment is not None:
                raise PaymentAlreadyExistsError(
                    order_id
                )

            # 4. Create a NEW payment
            payment = Payment(
                order_id=order.id,
                amount=order.total_price,
                status=PaymentStatus.PENDING,
            )

            self.payment_repository.create(payment)

            # 5. Commit
            self.db.commit()

            # 6. Refresh
            self.db.refresh(payment)

            return payment

        except Exception:
            self.db.rollback()
            raise

    def succeed_payment(
        self,
        payment_id: int,
    ) -> Payment:

        try:
            # 1. Find payment
            payment = self.payment_repository.get_by_id(
                payment_id
            )

            if payment is None:
                raise PaymentNotFoundError(payment_id)

            # 2. Idempotency:
            # If payment was already successful,
            # simply return it.
            if payment.status == PaymentStatus.SUCCEEDED:
                return payment

            # 3. A failed payment cannot be
            # magically turned into a success.
            if payment.status == PaymentStatus.FAILED:
                raise PaymentAlreadyFailedError(
                    payment_id
                )

            # 4. Find the related order
            order = self.order_repository.get_by_id(
                payment.order_id
            )

            if order is None:
                raise OrderNotFoundError(
                    payment.order_id
                )

            # 5. Make sure order is still pending
            if order.status != OrderStatus.PENDING:
                raise OrderCannotBeConfirmedError(
                    order.id,
                    order.status.value,
                )

            # 6. Mark payment as successful
            payment.status = PaymentStatus.SUCCEEDED

            # 7. Confirm the order
            order.status = OrderStatus.CONFIRMED

            # 8. Commit both changes together
            self.db.commit()

            # 9. Refresh payment
            self.db.refresh(payment)

            return payment

        except Exception:
            self.db.rollback()
            raise
    
    def fail_payment(
        self,
        payment_id: int,
    ) -> Payment:

        try:
            # 1. Find payment
            payment = self.payment_repository.get_by_id(
                payment_id
            )

            if payment is None:
                raise PaymentNotFoundError(payment_id)

            # 2. Idempotency
            if payment.status == PaymentStatus.FAILED:
                return payment

            # 3. A successful payment cannot become failed
            if payment.status == PaymentStatus.SUCCEEDED:
                raise PaymentAlreadySucceededError(
                    payment_id
                )

            # 4. Mark payment as failed
            payment.status = PaymentStatus.FAILED

            # 5. Commit
            self.db.commit()

            # 6. Refresh
            self.db.refresh(payment)

            return payment

        except Exception:
            self.db.rollback()
            raise