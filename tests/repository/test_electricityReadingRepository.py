import dataclasses
import pytest

from src.db import database
from src.domain.electricity_reading import ElectricityReading
from src.repository.electricity_reading_repository import ElectricityReadingRepository
from src.repository.smart_meter_repository import smart_meter_repository


@pytest.mark.asyncio
async def test_store_and_fetch_readings():
    if not database.is_connected:
        await database.connect()

    repo = ElectricityReadingRepository()
    meter_id_str = "smart-meter-0"

    # Store readings (smart meter is auto-created)
    await repo.store(
        meter_id_str,
        [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ],
    )

    # ✅ Now fetch numeric meter ID to clear readings
    meter_row = await smart_meter_repository.get_meter_by_identifier(meter_id_str)
    assert meter_row is not None
    meter_db_id = meter_row["id"]
    await database.execute(
        "DELETE FROM electricity_readings WHERE smart_meter_id = :id",
        {"id": meter_db_id},
    )

    # Re-store and verify
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


@pytest.mark.asyncio
async def test_append_readings_to_existing_meter():
    if not database.is_connected:
        await database.connect()

    repo = ElectricityReadingRepository()
    meter_id_str = "smart-meter-0"

    await repo.store(
        meter_id_str,
        [
            ElectricityReading({"time": 1507375234, "reading": 0.5}),
            ElectricityReading({"time": 1510053634, "reading": 0.75}),
        ],
    )

    # ✅ Get numeric ID
    meter_row = await smart_meter_repository.get_meter_by_identifier(meter_id_str)
    assert meter_row is not None
    meter_db_id = meter_row["id"]
    await database.execute(
        "DELETE FROM electricity_readings WHERE smart_meter_id = :id",
        {"id": meter_db_id},
    )

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
