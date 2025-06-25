from __future__ import annotations

from typing import Any, List

from ..domain.electricity_reading import ElectricityReading
from ..repository.electricity_reading_repository import (
    electricity_reading_repository,
)


class ElectricityReadingService:
    def __init__(self, repository=electricity_reading_repository):
        self.electricity_reading_repository = repository

    async def store_reading(self, json: Any) -> List[ElectricityReading]:
        readings = [
            ElectricityReading(x) for x in json["electricityReadings"]
        ]
        return await self.electricity_reading_repository.store(
            json["smartMeterId"], readings
        )

    async def retrieve_readings_for(
        self, smart_meter_id: str
    ) -> List[ElectricityReading]:
        return await self.electricity_reading_repository.find(smart_meter_id)
