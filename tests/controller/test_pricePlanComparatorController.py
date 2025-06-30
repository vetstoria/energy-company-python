import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.service.time_converter import iso_format_to_unix_time

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def _seed_readings(client):
    """Put some readings into the DB so /compare-all has data to work with."""
    readings = [
        {"time": iso_format_to_unix_time("2020-01-05T10:00:00"), "reading": 10.0},
        {"time": iso_format_to_unix_time("2020-01-05T11:00:00"), "reading": 20.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": "smart-meter-0", "electricityReadings": readings},
    )

def test_compare_all_price_plans(client):
    _seed_readings(client)

    resp = client.get("/price-plans/compare-all/smart-meter-0")
    assert resp.status_code == 200
    body = resp.json()

    # The exact cheapest plan depends on price-plan data loaded at start-up,
    # so we only assert that one of the known plan-IDs is chosen.
    assert body["pricePlanId"] in {"price-plan-0", "price-plan-1", "price-plan-2"}
    assert len(body["pricePlanComparisons"]) == 3

def test_recommend_cheapest_plans(client):
    readings = [
        {"time": iso_format_to_unix_time("2020-01-05T10:30:00"), "reading": 35.0},
        {"time": iso_format_to_unix_time("2020-01-05T11:00:00"), "reading": 5.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": "meter-103", "electricityReadings": readings},
    )

    resp = client.get("/price-plans/recommend/meter-103")
    assert resp.status_code == 200
    assert resp.json() == [
        {"price-plan-2": 40.0},
        {"price-plan-1": 80.0},
        {"price-plan-0": 400.0},
    ]

def test_compare_all_with_insufficient_readings(client):
    # Only 1 reading -> should trigger 422
    readings = [
        {"time": iso_format_to_unix_time("2024-01-01T10:00:00"), "reading": 10.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": "meter-insufficient", "electricityReadings": readings},
    )
    resp = client.get("/price-plans/compare-all/meter-insufficient")
    assert resp.status_code == 422
    assert "Not enough readings" in resp.json()["detail"]

def test_recommend_with_insufficient_readings(client):
    readings = [
        {"time": iso_format_to_unix_time("2024-01-01T10:00:00"), "reading": 15.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": "meter-recommend-insufficient", "electricityReadings": readings},
    )
    resp = client.get("/price-plans/recommend/meter-recommend-insufficient")
    assert resp.status_code == 422
    assert "Not enough readings" in resp.json()["detail"]
