import pytest
from http import HTTPStatus
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    # startup / shutdown events (and therefore DB connect / disconnect)
    # are only fired when TestClient is used as a *context manager*.
    with TestClient(app) as c:
        yield c


def test_store_reading_new_meter(client):
    payload = {
        "smartMeterId": "meter-11",
        "electricityReadings": [{"time": 1505825656, "reading": 0.6}],
    }
    resp = client.post("/readings/store", json=payload)
    assert resp.status_code == HTTPStatus.CREATED


def test_store_reading_existing_meter(client):
    first = {
        "smartMeterId": "meter-100",
        "electricityReadings": [
            {"time": 1505825838, "reading": 0.6},
            {"time": 1505825848, "reading": 0.65},
        ],
    }
    second = {
        "smartMeterId": "meter-100",
        "electricityReadings": [{"time": 1605825849, "reading": 0.7}],
    }

    client.post("/readings/store", json=first)
    client.post("/readings/store", json=second)

    readings = client.get("/readings/read/meter-100").json()
    assert {"time": 1505825838, "reading": 0.6} in readings
    assert {"time": 1505825848, "reading": 0.65} in readings
    assert {"time": 1605825849, "reading": 0.7} in readings


def test_no_readings_returns_404(client):
    import uuid
    # Use a guaranteed non-existent smart meter ID
    meter_id = f"non-existent-meter-{uuid.uuid4()}"
    resp = client.get(f"/readings/read/{meter_id}")
    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "payload",
    [
        {"electricityReadings": []},     # missing smartMeterId
        {"smartMeterId": "x"},           # missing readings
    ],
)
def test_validation_errors(client, payload):
    # FastAPI uses 422 for validation errors by default
    assert client.post("/readings/store", json=payload).status_code == 422
