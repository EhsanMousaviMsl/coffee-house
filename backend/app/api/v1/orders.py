from fastapi import APIRouter, Depends, status

from app.dependencies.orders import get_order_service
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.get(
    "/",
    response_model=list[OrderResponse],
)
def get_orders(
    service: OrderService = Depends(
        get_order_service
    ),
):
    return service.get_all_orders()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    service: OrderService = Depends(
        get_order_service
    ),
):
    return service.get_order_by_id(order_id)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    return service.create_order(data)

