from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import (
    OrderCannotBeConfirmedError,
    OrderNotFoundError,
    PaymentAmountMismatchError,
    PaymentNotFoundError,
    PaymentWebhookInvalidEventError,
)
from app.models.order import OrderStatus
from app.models.payment import PaymentStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.payment_webhook_event import (
    PaymentWebhookEventRepository,
)
from app.schemas.payment_webhook import (
    PaymentWebhookEventType,
    PaymentWebhookRequest,
)


class PaymentWebhookService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        order_repository: OrderRepository,
        webhook_event_repository: PaymentWebhookEventRepository,
        db: Session,
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository
        self.webhook_event_repository = webhook_event_repository
        self.db = db

    def process(
        self,
        data: PaymentWebhookRequest,
        payload: dict,
    ):
        try:
            # 1. Fast idempotency check
            existing_event = (
                self.webhook_event_repository.get_by_event_id(
                    data.event_id
                )
            )

            if existing_event is not None:
                payment = self.payment_repository.get_by_id(
                    existing_event.payment_id
                )

                if payment is None:
                    raise PaymentNotFoundError(
                        existing_event.payment_id
                    )

                return payment
            # 1. Find payment
            payment = self.payment_repository.get_by_id(
                data.payment_id
            )

            if payment is None:
                raise PaymentNotFoundError(
                    data.payment_id
                )

            # 2. Validate amount
            if payment.amount != data.amount:
                raise PaymentAmountMismatchError(
                    payment.id,
                    str(payment.amount),
                    str(data.amount),
                )

            # 3. Find related order
            order = self.order_repository.get_by_id(
                payment.order_id
            )

            if order is None:
                raise OrderNotFoundError(
                    payment.order_id
                )

            # 4. Apply event
            if (
                data.event_type
                == PaymentWebhookEventType.PAYMENT_SUCCEEDED
            ):
                self._handle_success(
                    payment,
                    order,
                )

            elif (
                data.event_type
                == PaymentWebhookEventType.PAYMENT_FAILED
            ):
                self._handle_failure(
                    payment,
                )

            # 5. Record webhook event
            webhook_event = (
                self.webhook_event_repository
                .create_if_not_exists(
                    event_id=data.event_id,
                    event_type=data.event_type.value,
                    payment_id=payment.id,
                    payload=payload,
                    processed_at=datetime.now(timezone.utc),
                    created_at=datetime.now(timezone.utc),
                )
            )

            # 6. Duplicate webhook
            if webhook_event is None:
                self.db.rollback()
                return payment

            # 7. Commit everything
            self.db.commit()

            # 8. Refresh payment
            self.db.refresh(payment)

            return payment

        except Exception:
            self.db.rollback()
            raise

    def _handle_success(
        self,
        payment,
        order,
    ) -> None:
        if payment.status == PaymentStatus.SUCCEEDED:
            return

        if payment.status == PaymentStatus.FAILED:
            raise PaymentWebhookInvalidEventError(
                PaymentWebhookEventType.PAYMENT_SUCCEEDED.value,
                payment.id,
            )

        if order.status != OrderStatus.PENDING:
            raise OrderCannotBeConfirmedError(
                order.id,
                order.status.value,
            )

        payment.status = PaymentStatus.SUCCEEDED
        order.status = OrderStatus.CONFIRMED

    def _handle_failure(
        self,
        payment,
    ) -> None:
        if payment.status == PaymentStatus.FAILED:
            return

        if payment.status == PaymentStatus.SUCCEEDED:
            raise PaymentWebhookInvalidEventError(
                PaymentWebhookEventType.PAYMENT_FAILED.value,
                payment.id,
            )

        payment.status = PaymentStatus.FAILED