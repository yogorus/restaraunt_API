import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import get_db, Base
from src.main import app

# DB
# DATABASE_URL_TEST = f"sqlite:///"

# TEST_SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@test_db:6000/db"

# engine = create_engine(
#     TEST_SQLALCHEMY_DATABASE_URL,
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# @pytest.fixture(autouse=True, scope="session")
# async def prepare_database():
#     with engine_test.begin() as conn:
#         await conn.metadata.create_all()
#     yield
#     with engine_test.begin() as conn:
#         await conn.metadata.drop_all()


# @pytest.fixture(autouse=True, scope="function")
# def clean_up_database():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield
#     db.rollback()


# @pytest.fixture(autouse=True, scope="session")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture
# def test_client():
#     yield client


# @pytest.fixture(name='client')
# def client
