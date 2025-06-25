import pytest
from unittest.mock import AsyncMock
from src.domain.electricity_reading import ElectricityReading
from src.domain.price_plan import PricePlan
from src.service.price_plan_service import PricePlanService
from src.service.time_converter import iso_format_to_unix_time
from src.repository.price_plan_repository import price_plan_repository  # ← direct module import


@pytest.mark.asyncio
async def test_calculate_costs_against_all_price_plans(monkeypatch):
    # ── 1. stub out the price-plan repo so we stay independent of DB contents ──
    async def fake_get():
        return [
            PricePlan("X1", "XS1", 10),
            PricePlan("X2", "XS2", 2),
            PricePlan("X6", "XS6", 1),
        ]

    monkeypatch.setattr(price_plan_repository, "get", fake_get)

    # ── 2. fake three readings so we don't hit the DB here either ─────────────
    reading_list = [
        ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T09:00:00"), "reading": 0.65}),
        ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T09:30:00"), "reading": 0.35}),
        ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T10:00:00"), "reading": 0.5}),
    ]

    svc = PricePlanService()
    svc.electricity_reading_service.retrieve_readings_for = AsyncMock(return_value=reading_list)

    spend = await svc.get_list_of_spend_against_each_price_plan_for("any-meter")

    assert spend == [{"X6": 0.5}, {"X2": 1.0}, {"X1": 5.0}]
