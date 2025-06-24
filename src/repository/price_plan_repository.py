from __future__ import annotations

from typing import List

from ..domain.price_plan import PricePlan
from ..db import database, price_plans


class PricePlanRepository:
    """
    Async MySQL-backed repository for `price_plans`.
    """

    async def store(self, plans: List[PricePlan]) -> None:
        """
        Insert price plans. Duplicate IDs are ignored (`INSERT … ON DUPLICATE KEY`).
        """
        values = [
            {"id": p.name, "supplier": p.supplier, "unit_rate": p.unit_rate}
            for p in plans
        ]
        query = price_plans.insert().prefix_with("IGNORE")
        await database.execute_many(query, values)

    async def get(self) -> List[PricePlan]:
        rows = await database.fetch_all(price_plans.select())
        return [PricePlan(r["id"], r["supplier"], r["unit_rate"]) for r in rows]


price_plan_repository = PricePlanRepository()
