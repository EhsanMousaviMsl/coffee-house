from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PaymentWebhookEventType(str, Enum):
    PAYMENT_SUCCEEDED = "payment.succeeded"
    PAYMENT_FAILED = "payment.failed"


class PaymentWebhookRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1, max_length=255)
    event_type: PaymentWebhookEventType
    payment_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)


class PaymentWebhookResponse(BaseModel):
    received: bool