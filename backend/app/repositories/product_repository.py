from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Product]:
        stmt = select(Product)

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
        )

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product