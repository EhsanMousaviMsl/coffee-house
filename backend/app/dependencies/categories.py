from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.services.category_service import CategoryService


def get_category_repository(
    db: Session = Depends(get_db),
) -> CategoryRepository:
    return CategoryRepository(db)


def get_product_repository(
    db: Session = Depends(get_db),
) -> ProductRepository:
    return ProductRepository(db)


def get_category_service(
    category_repository: CategoryRepository = Depends(
        get_category_repository
    ),
    product_repository: ProductRepository = Depends(
        get_product_repository
    ),
) -> CategoryService:

    return CategoryService(
        category_repository,
        product_repository,
    )