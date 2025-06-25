"""
Populates initial data directly into MySQL (async).
Called once during FastAPI startup, *after* the DB connection opens.
"""
from __future__ import annotations

from typing import List

from .domain.price_plan import PricePlan
from .generator.electricity_reading_generator import generate_electricity_readings
from .repository.electricity_reading_repository import (
    electricity_reading_repository,
)
from .repository.price_plan_repository import price_plan_repository
from .domain.electricity_reading import ElectricityReading

DR_EVILS_DARK_ENERGY_ENERGY_SUPPLIER = "Dr Evil's Dark Energy"
THE_GREEN_ECO_ENERGY_SUPPLIER = "The Green Eco"
POWER_FOR_EVERYONE_ENERGY_SUPPLIER = "Power for Everyone"

MOST_EVIL_PRICE_PLAN_ID = "price-plan-0"
RENEWBLES_PRICE_PLAN_ID = "price-plan-1"
STANDARD_PRICE_PLAN_ID = "price-plan-2"

NUM_METERS = 10
NUM_READINGS_AGAINST_METER = 5


async def _populate_random_electricity_readings():
    for index in range(NUM_METERS):
        smart_meter_id = f"smart-meter-{index}"

        await electricity_reading_repository.store(
            smart_meter_id,
            [
                ElectricityReading(r)
                for r in generate_electricity_readings(NUM_READINGS_AGAINST_METER)
            ],
        )


async def _populate_price_plans():
    price_plans: List[PricePlan] = [
        PricePlan(
            MOST_EVIL_PRICE_PLAN_ID,
            DR_EVILS_DARK_ENERGY_ENERGY_SUPPLIER,
            10,
        ),
        PricePlan(
            RENEWBLES_PRICE_PLAN_ID, THE_GREEN_ECO_ENERGY_SUPPLIER, 2
        ),
        PricePlan(STANDARD_PRICE_PLAN_ID, POWER_FOR_EVERYONE_ENERGY_SUPPLIER, 1),
    ]
    await price_plan_repository.store(price_plans)


async def initialize_data():
    await _populate_random_electricity_readings()
    await _populate_price_plans()
