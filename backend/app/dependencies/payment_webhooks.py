from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.payment_webhook_event import (
    PaymentWebhookEventRepository,
)
from app.services.payment_webhook_service import (
    PaymentWebhookService,
)
from app.dependencies.orders import get_order_repository
from app.dependencies.payments import get_payment_repository


def get_payment_webhook_event_repository(
    db: Session = Depends(get_db),
) -> PaymentWebhookEventRepository:

    return PaymentWebhookEventRepository(db)


def get_payment_webhook_service(
    db: Session = Depends(get_db),
    payment_repository: PaymentRepository = Depends(
        get_payment_repository
    ),
    order_repository: OrderRepository = Depends(
        get_order_repository
    ),
    webhook_event_repository: PaymentWebhookEventRepository = Depends(
        get_payment_webhook_event_repository
    ),
) -> PaymentWebhookService:

    return PaymentWebhookService(
        payment_repository=payment_repository,
        order_repository=order_repository,
        webhook_event_repository=webhook_event_repository,
        db=db,
    )