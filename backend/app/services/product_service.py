from app.core.exceptions import CategoryNotFoundError
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.core.exceptions import (
    CategoryNotFoundError,
    ProductNotFoundError,
)
from app.schemas.product import ProductUpdate


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

    def get_product_by_id(
    self,
    product_id: int
):

        product = self.product_repository.get_by_id(
            product_id
        )

        if product is None:
            raise ProductNotFoundError(product_id)

        return product

    def update_product(
        self,
        product_id: int,
        data: ProductUpdate
    ):

        product = self.product_repository.get_by_id(
            product_id
        )

        if product is None:
            raise ProductNotFoundError(product_id)


        update_data = data.model_dump(
            exclude_unset=True
        )


        if "category_id" in update_data:

            category = self.category_repository.get_by_id(
                update_data["category_id"]
            )

            if category is None:
                raise CategoryNotFoundError(
                    update_data["category_id"]
                )


        return self.product_repository.update(
            product,
            update_data
        )

    def delete_product(
        self,
        product_id: int,
    ):

        product = self.product_repository.get_by_id(
            product_id
        )

        if product is None:
            raise ProductNotFoundError(product_id)


        return self.product_repository.delete(
            product
        )