from fastapi import APIRouter

from app.api.v1.products import router as product_router
from app.api.v1.categories import router as category_router
from app.api.v1.orders import router as order_router
from app.api.v1.payments import router as payment_router
from app.api.v1.payment_webhooks import (
    router as payment_webhook_router,
)


api_router = APIRouter()


api_router.include_router(product_router)
api_router.include_router(category_router)
api_router.include_router(order_router)
api_router.include_router(payment_router)
api_router.include_router(
    payment_webhook_router
)