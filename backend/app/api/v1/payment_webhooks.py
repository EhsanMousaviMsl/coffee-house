import json
from fastapi import APIRouter, Depends, Request, status
from app.core.config import get_settings
from app.core.security import verify_webhook_signature
from app.core.exceptions import InvalidWebhookSignatureError

from app.dependencies.payment_webhooks import (
    get_payment_webhook_service,
)
from app.schemas.payment import PaymentResponse
from app.schemas.payment_webhook import PaymentWebhookRequest, PaymentWebhookResponse
from app.services.payment_webhook_service import (
    PaymentWebhookService,
)


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post(
    "/payment",
    response_model=PaymentWebhookResponse,
    status_code=status.HTTP_200_OK,
)
async def payment_webhook(
    data: PaymentWebhookRequest,
    request: Request,
    service: PaymentWebhookService = Depends(
        get_payment_webhook_service
    ),
):
    settings = get_settings()

    raw_body = await request.body()

    signature = request.headers.get(
        "X-Webhook-Signature"
    )

    if signature is None:
        raise InvalidWebhookSignatureError()

    if not verify_webhook_signature(
        payload=raw_body,
        signature=signature,
        secret=settings.payment_webhook_secret,
    ):
        raise InvalidWebhookSignatureError()

    payload = json.loads(raw_body)

    service.process(
        data=data,
        payload=payload,
    )

    return PaymentWebhookResponse(
        received=True,
    )

