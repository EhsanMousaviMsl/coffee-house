from sqlalchemy.orm import Session

from app.models.product import Product

from sqlalchemy import select


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Product]:
        stmt = select(Product)

        result = self.session.execute(stmt)

        return result.scalars().all()