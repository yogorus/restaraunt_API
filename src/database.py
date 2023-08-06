"""Database config"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import DB_HOST, DB_NAME, DB_PORT, POSTGRES_PASSWORD, POSTGRES_USER

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)

SessionLocal = AsyncSession(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base"""

    # pylint: disable=too-few-public-methods


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get db"""
    async with SessionLocal as session:
        yield session
