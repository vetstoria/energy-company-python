import pytest
import uuid
from src.db import database
from src.domain.electricity_reading import ElectricityReading
from src.service.price_plan_service import PricePlanService
from src.service.time_converter import iso_format_to_unix_time

@pytest.mark.asyncio
async def test_calculate_costs_against_all_price_plans():
    await database.connect()

    meter_id = f"test-meter-{uuid.uuid4()}"
    readings = [
        ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T09:00:00"), "reading": 0.65}),
        ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T09:30:00"), "reading": 0.35}),
        ElectricityReading({"time": iso_format_to_unix_time("2017-11-10T10:00:00"), "reading": 0.5}),
    ]

    svc = PricePlanService()
    await svc.electricity_reading_service.store_reading({
        "smartMeterId": meter_id,
        "electricityReadings": [
            {"time": r.time, "reading": r.reading} for r in readings
        ]
    })

    spend = await svc.get_list_of_spend_against_each_price_plan_for(meter_id)

    assert isinstance(spend, list)
    assert all(isinstance(item, dict) for item in spend)
    assert len(spend) == 3

    await database.disconnect()
