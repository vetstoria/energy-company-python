import pytest
from src.db import database

@pytest.fixture
async def db_transaction():
    await database.connect()
    async with database.transaction():
        yield
    await database.disconnect()
