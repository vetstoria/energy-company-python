"""
Populates initial data directly into MySQL (async).
Called once during FastAPI startup, *after* the DB connection opens.
"""
from __future__ import annotations

from typing import List

from .domain.price_plan import PricePlan
from .generator.electricity_reading_generator import generate_electricity_readings
from .repository.electricity_reading_repository import electricity_reading_repository
from .repository.price_plan_repository import price_plan_repository
from .repository.smart_meter_repository import smart_meter_repository
from .domain.electricity_reading import ElectricityReading

# Price-plan constants
DR_EVILS_DARK_ENERGY = "Dr Evil's Dark Energy"
THE_GREEN_ECO        = "The Green Eco"
POWER_FOR_EVERYONE   = "Power for Everyone"

MOST_EVIL   = "price-plan-0"
RENEWABLES  = "price-plan-1"
STANDARD    = "price-plan-2"

NUM_METERS  = 10
NUM_READINGS_PER_METER = 5


async def _populate_price_plans() -> None:
    plans: List[PricePlan] = [
        PricePlan(MOST_EVIL,   DR_EVILS_DARK_ENERGY, 10),
        PricePlan(RENEWABLES,  THE_GREEN_ECO,        2),
        PricePlan(STANDARD,    POWER_FOR_EVERYONE,   1),
    ]
    await price_plan_repository.store(plans)


async def _populate_smart_meters() -> None:
    for i in range(NUM_METERS):
        smart_id     = f"smart-meter-{i}"
        plan_name    = [MOST_EVIL, RENEWABLES, STANDARD][i % 3]
        await smart_meter_repository.store(smart_id, plan_name)


async def _populate_random_readings() -> None:
    for i in range(NUM_METERS):
        smart_id = f"smart-meter-{i}"
        await electricity_reading_repository.store(
            smart_id,
            [ElectricityReading(r) for r in generate_electricity_readings(NUM_READINGS_PER_METER)],
        )


async def initialize_data() -> None:
    await _populate_price_plans()
    await _populate_smart_meters()
    await _populate_random_readings()
