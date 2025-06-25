import os
import asyncio
import pytest
from dotenv import load_dotenv

# Load .env.test specifically for test runs
# TEST_ENV_PATH = ".env.test"
# if os.path.exists(TEST_ENV_PATH):
#     load_dotenv(dotenv_path=TEST_ENV_PATH, override=True)
# else:
#     load_dotenv()  # fallback to regular .env

load_dotenv(dotenv_path=".env.test")

from src.db import database  # <-- Must import AFTER env is loaded

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
async def _isolate_tests_with_transaction(_database_pool):  # ⬅ ensures pool is ready
    async with database.transaction():
        yield
