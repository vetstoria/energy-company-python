import pytest
from unittest.mock import AsyncMock
from src.domain.electricity_reading import ElectricityReading
from src.service.electricity_reading_service import ElectricityReadingService
from src.service.time_converter import iso_format_to_unix_time


@pytest.mark.asyncio
async def test_calls_repository_to_store_readings():
    repo_mock = AsyncMock()
    service = ElectricityReadingService(repo_mock)

    payload = {
        "smartMeterId": "meter-45",
        "electricityReadings": [
            {"time": iso_format_to_unix_time("2015-03-02T08:55:00"), "reading": 0.812},
            {"time": iso_format_to_unix_time("2015-09-02T08:55:00"), "reading": 0.23},
        ],
    }

    await service.store_reading(payload)

    repo_mock.store.assert_awaited_once_with(
        "meter-45",
        [
            ElectricityReading({"time": iso_format_to_unix_time("2015-03-02T08:55:00"), "reading": 0.812}),
            ElectricityReading({"time": iso_format_to_unix_time("2015-09-02T08:55:00"), "reading": 0.23}),
        ],
    )
