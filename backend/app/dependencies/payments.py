from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.payment_service import PaymentService
from app.dependencies.orders import get_order_repository


def get_payment_repository(
    db: Session = Depends(get_db),
) -> PaymentRepository:

    return PaymentRepository(db)


# def get_order_repository(
#     db: Session = Depends(get_db),
# ) -> OrderRepository:

#     return OrderRepository(db)


def get_payment_service(
    db: Session = Depends(get_db),
    payment_repository: PaymentRepository = Depends(
        get_payment_repository
    ),
    order_repository: OrderRepository = Depends(
        get_order_repository
    ),
) -> PaymentService:

    return PaymentService(
        payment_repository=payment_repository,
        order_repository=order_repository,
        db=db,
    )