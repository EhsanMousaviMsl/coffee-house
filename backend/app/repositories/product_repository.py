from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate
from datetime import datetime, UTC


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Product]:
        stmt = select(Product).where(
            Product.deleted_at.is_(None)
        )

        result = self.session.execute(stmt)

        return result.scalars().all()

    def create(self, data: ProductCreate) -> Product:
        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            image_url=data.image_url,
            available=data.available,
            category_id=data.category_id,
            inventory=data.inventory
        )

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def get_by_id(
        self,
        product_id: int
    ) -> Product | None:

        stmt = select(Product).where(
            Product.id == product_id,
            Product.deleted_at.is_(None)
        )

        result = self.session.execute(stmt)

        return result.scalar_one_or_none()
    
    def get_by_id_for_update(
        self,
        product_id: int,
    ) -> Product | None:

        stmt = (
            select(Product)
            .where(
                Product.id == product_id,
                Product.deleted_at.is_(None),
            )
            .with_for_update()
        )

        result = self.session.execute(stmt)

        return result.scalar_one_or_none()

    def update(
        self,
        product: Product,
        data: dict
    ) -> Product:

        for field, value in data.items():
            setattr(product, field, value)

        self.session.commit()
        self.session.refresh(product)

        return product

    def delete(
        self,
        product: Product,
    ):

        product.deleted_at = datetime.now(UTC)

        self.session.commit()
        self.session.refresh(product)

        return product

    def exists_by_category_id(
        self,
        category_id: int,
    ) -> bool:

        stmt = select(Product.id).where(
            Product.category_id == category_id,
            Product.deleted_at.is_(None),
        ).limit(1)

        result = self.session.execute(stmt)

        return result.scalar_one_or_none() is not None
    
    def decrease_inventory(
        self,
        product: Product,
        quantity: int,
    ) -> Product:
        product.inventory -= quantity

        self.session.flush()

        return product
    
    def increase_inventory(
        self,
        product: Product,
        quantity: int,
    ) -> Product:

        product.inventory += quantity

        self.session.flush()

        return product