from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.order_service import OrderService


def get_order_repository(
    db: Session = Depends(get_db),
) -> OrderRepository:
    return OrderRepository(db)


def get_product_repository(
    db: Session = Depends(get_db),
) -> ProductRepository:
    return ProductRepository(db)


def get_order_service(
    db: Session = Depends(get_db),
    order_repository: OrderRepository = Depends(
        get_order_repository
    ),
    product_repository: ProductRepository = Depends(
        get_product_repository
    ),
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        product_repository=product_repository,
        db=db,
    )