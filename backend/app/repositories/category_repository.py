from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)

        result = self.session.execute(stmt)

        return result.scalar_one_or_none()
        