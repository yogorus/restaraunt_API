"""Config for pytest"""
import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.main import app

# DB
# DATABASE_URL_TEST = f"sqlite:///"

# TEST_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@ylab_db:5432/db"

# engine_test = create_engine(
#     TEST_SQLALCHEMY_DATABASE_URL,
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# # Base.metadata.create_all(bind=engine_test)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


# client = TestClient(app)
# @pytest.fixture(autouse=True, scope="session")
# async def prepare_database():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine_test.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://localhost:8000/api/v1') as client:
        yield client


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
