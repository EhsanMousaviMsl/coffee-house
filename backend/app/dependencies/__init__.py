from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


def get_product_repository(
    db: Session = Depends(get_db),
) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(
    repository: ProductRepository = Depends(get_product_repository),
) -> ProductService:
    return ProductService(repository)