from app.repositories.product_repository import ProductRepository
from app.models.product import Product


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self) -> list[Product]:
        return self.repository.get_all()