from fastapi import APIRouter, Depends, status

from app.dependencies.payments import get_payment_service
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)
from app.services.payment_service import PaymentService
from app.dependencies.payment_webhooks import (
    get_payment_webhook_service,
)
from app.schemas.payment_webhook import PaymentWebhookEventType
from app.services.payment_webhook_service import PaymentWebhookService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    data: PaymentCreate,
    service: PaymentService = Depends(
        get_payment_service
    ),
):
    return service.create_payment(
        data.order_id
    )

@router.post(
    "/{payment_id}/succeed",
    response_model=PaymentResponse,
)
def succeed_payment(
    payment_id: int,
    service: PaymentService = Depends(
        get_payment_service
    ),
):
    return service.succeed_payment(
        payment_id
    )

@router.post(
    "/{payment_id}/fail",
    response_model=PaymentResponse,
)
def fail_payment(
    payment_id: int,
    service: PaymentService = Depends(
        get_payment_service
    ),
):
    return service.fail_payment(
        payment_id
    )

@router.post(
    "/{payment_id}/simulate-success",
    response_model=PaymentResponse,
)
def simulate_payment_success(
    payment_id: int,
    service: PaymentWebhookService = Depends(
        get_payment_webhook_service
    ),
):
    return service.simulate(
        payment_id=payment_id,
        event_type=PaymentWebhookEventType.PAYMENT_SUCCEEDED,
    )

@router.post(
    "/{payment_id}/simulate-failure",
    response_model=PaymentResponse,
)
def simulate_payment_failure(
    payment_id: int,
    service: PaymentWebhookService = Depends(
        get_payment_webhook_service
    ),
):
    return service.simulate(
        payment_id=payment_id,
        event_type=PaymentWebhookEventType.PAYMENT_FAILED,
    )