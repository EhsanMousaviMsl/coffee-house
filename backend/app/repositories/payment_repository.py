from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment, PaymentStatus


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        payment: Payment,
    ) -> Payment:

        self.db.add(payment)
        self.db.flush()

        return payment

    def get_by_id(
        self,
        payment_id: int,
    ) -> Payment | None:

        stmt = select(Payment).where(
            Payment.id == payment_id,
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def update(
        self,
        payment: Payment,
    ) -> Payment:

        self.db.flush()

        return payment
    
    def get_pending_by_order_id(
        self,
        order_id: int,
    ) -> Payment | None:

        stmt = select(Payment).where(
            Payment.order_id == order_id,
            Payment.status == PaymentStatus.PENDING,
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()