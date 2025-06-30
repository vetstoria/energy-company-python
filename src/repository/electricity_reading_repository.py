# src/repository/electricity_reading_repository.py

from __future__ import annotations

from typing import List

from ..domain.electricity_reading import ElectricityReading
from ..db import database, electricity_readings
from ..repository.smart_meter_repository import smart_meter_repository

# Default price plan ID to assign when a new smart meter is seen
DEFAULT_PRICE_PLAN_ID = "price-plan-0"


class ElectricityReadingRepository:
    """
    Async MySQL-backed repository (databases + SQLAlchemy Core).
    """

    async def store(self, smart_meter_id: str, readings: List[ElectricityReading]):
        # 1) Ensure the smart_meter is registered (INSERT IGNORE in repo)
        await smart_meter_repository.store(smart_meter_id, DEFAULT_PRICE_PLAN_ID)

        # 2) Store the actual readings
        values = [
            {
                "smart_meter_id": smart_meter_id,
                "time": reading.time,
                "reading": reading.reading,
            }
            for reading in readings
        ]
        query = electricity_readings.insert()
        await database.execute_many(query, values)
        return readings  # keep existing behaviour

    async def find(self, smart_meter_id: str) -> List[ElectricityReading]:
        query = electricity_readings.select().where(
            electricity_readings.c.smart_meter_id == smart_meter_id
        )
        rows = await database.fetch_all(query)
        return [
            ElectricityReading({"time": row["time"], "reading": row["reading"]})
            for row in rows
        ]


# Singleton instance
electricity_reading_repository = ElectricityReadingRepository()
