"""Config for pytest"""
import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[AbstractEventLoop, None, None]:
    # pylint: disable=unused-argument
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Test client"""
    # pylint: disable=redefined-outer-name
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client
