import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_db, Base
from src.main import app

# DB
DATABASE_URL_TEST = f"postgresql://postgres:postgres@localhost:6000/db"
metadata = MetaData()

engine_test = create_engine(DATABASE_URL_TEST, poolclass=NullPool)
TestingSessionLocal = sessionmaker(
    engine_test, expire_on_commit=False, autocommit=False, autoflush=False
)
# metadata.bind = engine_test  # type: ignore


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
