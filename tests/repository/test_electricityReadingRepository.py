import dataclasses
import pytest
from src.db import database
from src.domain.electricity_reading import ElectricityReading
from src.repository.electricity_reading_repository import ElectricityReadingRepository

@pytest.mark.asyncio
async def test_store_and_fetch_readings():
    if not database.is_connected:
        await database.connect()

    repo = ElectricityReadingRepository()

    # Clear existing readings
    await database.execute("DELETE FROM electricity_readings WHERE smart_meter_id = 'smart-meter-0'")

    await repo.store(
        "smart-meter-0",
        [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ],
    )

    readings = await repo.find("smart-meter-0")
    assert dataclasses.asdict(readings[0]) == {"time": 1507375234, "reading": 0.5}
    assert dataclasses.asdict(readings[1]) == {"time": 1510053634, "reading": 0.75}


@pytest.mark.asyncio
async def test_append_readings_to_existing_meter():
    if not database.is_connected:
        await database.connect()

    repo = ElectricityReadingRepository()

    # Clear existing readings
    await database.execute("DELETE FROM electricity_readings WHERE smart_meter_id = 'smart-meter-0'")

    await repo.store(
        "smart-meter-0",
        [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ],
    )
    await repo.store(
        "smart-meter-0",
        [ElectricityReading({"time": 1510572000, "reading": 0.32})],
    )

    readings = await repo.find("smart-meter-0")
    assert len(readings) == 3
