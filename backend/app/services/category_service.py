from app.core.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    CategoryHasProductsError,
)
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(
        self,
        category_repository: CategoryRepository,
        product_repository: ProductRepository,
    ):
        self.category_repository = category_repository
        self.product_repository = product_repository

    def create_category(
        self,
        data: CategoryCreate,
    ) -> Category:

        existing_category = self.repository.get_by_name(
            data.name
        )

        if existing_category is not None:
            raise CategoryAlreadyExistsError(
                data.name
            )

        category = Category(
            name=data.name,
            image_url=data.image_url,
        )

        return self.repository.create(category)

    def get_all_categories(self) -> list[Category]:

        return self.repository.get_all()

    def get_category_by_id(
        self,
        category_id: int,
    ) -> Category:

        category = self.repository.get_by_id(
            category_id
        )

        if category is None:
            raise CategoryNotFoundError(category_id)

        return category

    def update_category(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Category:

        category = self.repository.get_by_id(
            category_id
        )

        if category is None:
            raise CategoryNotFoundError(category_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:

            existing_category = self.repository.get_by_name(
                update_data["name"]
            )

            if (
                existing_category is not None
                and existing_category.id != category.id
            ):
                raise CategoryAlreadyExistsError(
                    update_data["name"]
                )

        return self.repository.update(
            category,
            update_data,
        )

    def delete_category(
        self,
        category_id: int,
    ) -> None:

        category = self.category_repository.get_by_id(
            category_id
        )

        if category is None:
            raise CategoryNotFoundError(category_id)

        if self.product_repository.exists_by_category_id(
            category_id
        ):
            raise CategoryHasProductsError(category_id)

        self.category_repository.delete(category)