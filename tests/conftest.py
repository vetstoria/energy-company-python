import os

import pytest
from fastapi.testclient import TestClient

# Ensure rollback mode for every connection
os.environ["TESTING"] = "1"

from src.main import app  # noqa: E402  pylint: disable=import-error

@pytest.fixture()
def client():
    """
    Provides a TestClient wrapped in a context-manager so FastAPI startup /
    shutdown events (and therefore DB connect / disconnect with rollback)
    execute for each test.
    """
    with TestClient(app) as c:
        yield c