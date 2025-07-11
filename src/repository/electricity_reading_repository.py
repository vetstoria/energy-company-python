from __future__ import annotations
from typing import List

from ..domain.electricity_reading import ElectricityReading
from ..db import database, electricity_readings
from ..repository.smart_meter_repository import smart_meter_repository

DEFAULT_PRICE_PLAN_ID = "price-plan-0"


class ElectricityReadingRepository:
    """
    Async MySQL-backed repository (databases + SQLAlchemy Core).
    """

    async def store(self, smart_meter_id: str, readings: List[ElectricityReading]):
        # Ensure the smart meter exists (insert if needed)
        await smart_meter_repository.store(smart_meter_id, DEFAULT_PRICE_PLAN_ID)

        # ✅ Get the internal numeric smart meter ID
        meter_row = await smart_meter_repository.get_meter_by_identifier(smart_meter_id)
        if meter_row is None:
            raise ValueError(f"Smart meter {smart_meter_id} not found after store.")
        meter_id = meter_row["id"]

        # ✅ Store readings using the numeric smart meter ID
        values = [
            {
                "smart_meter_id": meter_id,
                "time": reading.time,
                "reading": reading.reading,
            }
            for reading in readings
        ]
        await database.execute_many(electricity_readings.insert(), values)
        return readings

    async def find(self, smart_meter_id: str) -> List[ElectricityReading]:
        # ✅ Look up numeric ID first
        meter_row = await smart_meter_repository.get_meter_by_identifier(smart_meter_id)
        if meter_row is None:
            return []
        meter_id = meter_row["id"]

        # Retrieve readings
        query = electricity_readings.select().where(
            electricity_readings.c.smart_meter_id == meter_id
        )
        rows = await database.fetch_all(query)
        return [
            ElectricityReading({"time": row["time"], "reading": row["reading"]})
            for row in rows
        ]


# Singleton instance
electricity_reading_repository = ElectricityReadingRepository()
