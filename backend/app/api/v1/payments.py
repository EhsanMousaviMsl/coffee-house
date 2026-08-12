from fastapi import APIRouter, Depends, status

from app.dependencies.payments import get_payment_service
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)
from app.services.payment_service import PaymentService


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