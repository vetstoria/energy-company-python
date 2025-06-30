from __future__ import annotations

from functools import reduce
from typing import List
from fastapi import HTTPException

from ..repository.price_plan_repository import price_plan_repository
from .electricity_reading_service import ElectricityReadingService
from .time_converter import time_elapsed_in_hours


def _calculate_time_elapsed(readings):
    min_time = min(map(lambda r: r.time, readings))
    max_time = max(map(lambda r: r.time, readings))
    return time_elapsed_in_hours(min_time, max_time)


class PricePlanService:
    def __init__(
        self, reading_service: ElectricityReadingService | None = None
    ):
        # allow DI for testability
        self.electricity_reading_service = (
            reading_service or ElectricityReadingService()
        )

    async def get_list_of_spend_against_each_price_plan_for(
        self, smart_meter_id: str, limit: int | None = None
    ) -> List[dict]:
        readings = await self.electricity_reading_service.retrieve_readings_for(
            smart_meter_id
        )
        if len(readings) < 2:
            raise HTTPException(
                status_code=422,
                detail="Not enough readings to calculate usage. At least 2 readings are required."
            )

        average = self._calculate_average_reading(readings)
        time_elapsed = _calculate_time_elapsed(readings)
        if time_elapsed == 0:
            raise HTTPException(
                status_code=422,
                detail="Invalid readings: timestamps must not all be equal."
            )

        consumed_energy = average / time_elapsed

        price_plans = await price_plan_repository.get()

        def _cost_from_plan(price_plan):
            return {price_plan.name: consumed_energy * price_plan.unit_rate}

        list_of_spend = list(
            map(_cost_from_plan, self._cheapest_plans_first(price_plans))
        )
        return list_of_spend[:limit]

    # --------------------------------------------------------------------- #
    # helpers                                                               #
    # --------------------------------------------------------------------- #
    def _cheapest_plans_first(self, price_plans):
        return sorted(price_plans, key=lambda plan: plan.unit_rate)

    def _calculate_average_reading(self, readings):
        total = reduce(lambda acc, r: acc + r.reading, readings, 0)
        return total / len(readings)