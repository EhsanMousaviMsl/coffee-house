from fastapi import APIRouter, Depends, Request, status

from app.dependencies.payment_webhooks import (
    get_payment_webhook_service,
)
from app.schemas.payment import PaymentResponse
from app.schemas.payment_webhook import PaymentWebhookRequest
from app.services.payment_webhook_service import (
    PaymentWebhookService,
)


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post(
    "/payment",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def payment_webhook(
    data: PaymentWebhookRequest,
    request: Request,
    service: PaymentWebhookService = Depends(
        get_payment_webhook_service
    ),
):
    payload = await request.json()

    return service.process(
        data=data,
        payload=payload,
    )