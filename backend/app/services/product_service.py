from app.core.exceptions import CategoryNotFoundError
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:

    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def get_all_products(self):
        return self.product_repository.get_all()

    def create_product(self, data: ProductCreate):

        category = self.category_repository.get_by_id(
            data.category_id
        )

        if category is None:
            raise CategoryNotFoundError(data.category_id)

        return self.product_repository.create(data)