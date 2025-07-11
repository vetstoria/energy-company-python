import dataclasses
import pytest
import uuid
from src.db import database
from src.domain.electricity_reading import ElectricityReading
from src.repository.electricity_reading_repository import ElectricityReadingRepository

@pytest.mark.asyncio
async def test_store_and_fetch_readings():
    await database.connect()

    repo = ElectricityReadingRepository()
    meter_id_str = f"meter-{uuid.uuid4()}"

    await repo.store(
        meter_id_str,
        [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ],
    )

    readings = await repo.find(meter_id_str)
    assert dataclasses.asdict(readings[0]) == {"time": 1507375234, "reading": 0.5}
    assert dataclasses.asdict(readings[1]) == {"time": 1510053634, "reading": 0.75}

    await database.disconnect()

@pytest.mark.asyncio
async def test_append_readings_to_existing_meter():
    await database.connect()

    repo = ElectricityReadingRepository()
    meter_id_str = f"meter-{uuid.uuid4()}"

    await repo.store(
        meter_id_str,
        [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ],
    )

    await repo.store(
        meter_id_str,
        [ElectricityReading({"time": 1510572000, "reading": 0.32})],
    )

    readings = await repo.find(meter_id_str)
    assert len(readings) == 3

    await database.disconnect()
