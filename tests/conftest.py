import asyncio
import pytest
from dotenv import load_dotenv
from src.db import database

# ❶ load .env BEFORE touching the DB
load_dotenv()


# -------------------------------------------------------------- #
# 1. a single event-loop for the whole test-session              #
# -------------------------------------------------------------- #
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# -------------------------------------------------------------- #
# 2. create the connection-pool once per session                 #
# -------------------------------------------------------------- #
@pytest.fixture(scope="session", autouse=True)
async def _database_pool():
    await database.connect()
    yield
    await database.disconnect()


# -------------------------------------------------------------- #
# 3. wrap every test in a SAVEPOINT & roll everything back       #
# -------------------------------------------------------------- #
@pytest.fixture(autouse=True)
async def _isolate_tests_with_transaction(_database_pool):  # ⬅ dependency guarantees pool exists
    async with database.transaction():
        yield
