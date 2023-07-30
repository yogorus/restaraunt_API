import sys
from typing import AsyncGenerator
from dotenv.main import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from .config import DB_HOST, DB_NAME, DB_PORT, POSTGRES_USER, POSTGRES_PASSWORD

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@ylab_db:5432/db"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)

# SessionLocal = sessionmaker(
#     engine, autocommit=False, autoflush=False, class_=AsyncSession
# )
SessionLocal = AsyncSession(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_db():
#     async with SessionLocal() as session:
#         yield session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal as db:  # type: ignore
        yield db


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
