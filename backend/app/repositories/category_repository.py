from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, UTC
from app.models.category import Category



class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Category]:
        stmt = select(Category).where(
            Category.deleted_at.is_(None)
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def get_by_id(
        self,
        category_id: int,
    ) -> Category | None:

        stmt = select(Category).where(
            Category.id == category_id,
            Category.deleted_at.is_(None),
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_name(
        self,
        name: str,
    ) -> Category | None:

        stmt = select(Category).where(
            Category.name == name,
            Category.deleted_at.is_(None),
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def create(
        self,
        category: Category,
    ) -> Category:

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category


    def update(
        self,
        category: Category,
        data: dict,
    ) -> Category:

        for field, value in data.items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)

        return category

    def delete(self, category: Category) -> None:

        category.deleted_at = datetime.now(UTC)

        self.db.commit()