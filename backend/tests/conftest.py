import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.core.config import settings

from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = (
    "postgresql+psycopg://"
    f"{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}"
    "/coffee_house_test"
)


@pytest.fixture
def db():
    engine = create_engine(TEST_DATABASE_URL)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    payment_webhook_events,
                    payments,
                    order_items,
                    orders,
                    products,
                    categories
                RESTART IDENTITY CASCADE
                """
            )
        )

    with Session(engine) as session:
        yield session

    engine.dispose()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()