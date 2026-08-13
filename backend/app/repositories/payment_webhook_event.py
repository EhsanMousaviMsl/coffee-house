from datetime import datetime
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.payment_webhook_event import PaymentWebhookEvent


class PaymentWebhookEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_event_id(
        self,
        event_id: str,
    ) -> PaymentWebhookEvent | None:
        stmt = (
            select(PaymentWebhookEvent)
            .where(
                PaymentWebhookEvent.event_id == event_id,
            )
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def create_if_not_exists(
        self,
        *,
        event_id: str,
        event_type: str,
        payment_id: int,
        payload: dict,
        processed_at: datetime,
        created_at: datetime,
    ) -> PaymentWebhookEvent | None:

        stmt = (
            insert(PaymentWebhookEvent)
            .values(
                event_id=event_id,
                event_type=event_type,
                payment_id=payment_id,
                payload=payload,
                processed_at=processed_at,
                created_at=created_at,
            )
            .on_conflict_do_nothing(
                index_elements=["event_id"],
            )
            .returning(PaymentWebhookEvent)
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()