import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.service.time_converter import iso_format_to_unix_time
import uuid

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def _generate_meter_id():
    return f"test-meter-{uuid.uuid4()}"

def test_compare_all_price_plans(client):
    meter_id = _generate_meter_id()
    readings = [
        {"time": iso_format_to_unix_time("2020-01-05T10:00:00"), "reading": 10.0},
        {"time": iso_format_to_unix_time("2020-01-05T11:00:00"), "reading": 20.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": meter_id, "electricityReadings": readings},
    )

    resp = client.get(f"/price-plans/compare-all/{meter_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["pricePlanId"] in {"price-plan-0", "price-plan-1", "price-plan-2"}
    assert len(body["pricePlanComparisons"]) == 3

def test_recommend_cheapest_plans(client):
    meter_id = _generate_meter_id()
    readings = [
        {"time": iso_format_to_unix_time("2020-01-05T10:30:00"), "reading": 35.0},
        {"time": iso_format_to_unix_time("2020-01-05T11:00:00"), "reading": 5.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": meter_id, "electricityReadings": readings},
    )

    resp = client.get(f"/price-plans/recommend/{meter_id}")
    assert resp.status_code == 200
    assert resp.json() == [
        {"price-plan-2": 40.0},
        {"price-plan-1": 80.0},
        {"price-plan-0": 400.0},
    ]

def test_compare_all_with_insufficient_readings(client):
    meter_id = _generate_meter_id()
    readings = [
        {"time": iso_format_to_unix_time("2024-01-01T10:00:00"), "reading": 10.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": meter_id, "electricityReadings": readings},
    )
    resp = client.get(f"/price-plans/compare-all/{meter_id}")
    assert resp.status_code == 422
    assert any(msg in resp.json()["detail"] for msg in [
        "Not enough readings", "Invalid readings"
    ])

def test_recommend_with_insufficient_readings(client):
    meter_id = _generate_meter_id()
    readings = [
        {"time": iso_format_to_unix_time("2024-01-01T10:00:00"), "reading": 15.0},
    ]
    client.post(
        "/readings/store",
        json={"smartMeterId": meter_id, "electricityReadings": readings},
    )
    resp = client.get(f"/price-plans/recommend/{meter_id}")
    assert resp.status_code == 422
    assert any(msg in resp.json()["detail"] for msg in [
        "Not enough readings", "Invalid readings"
    ])
