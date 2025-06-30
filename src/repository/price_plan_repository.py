from __future__ import annotations

from typing import List

from ..domain.price_plan import PricePlan
from ..db import database, price_plans
import sqlalchemy as sa

class PricePlanRepository:
    """
    Async MySQL-backed repository for `price_plans`.
    """

    async def store(self, plans: List[PricePlan]) -> None:
        """
        Insert price plans. If ID already exists, do nothing.
        """
        for p in plans:
            # Check if the plan with this id already exists
            select_stmt = price_plans.select().with_only_columns(price_plans.c.id).where(price_plans.c.id == p.name)
            row = await database.fetch_one(select_stmt)
            if row is None:
                # Only insert if not present
                insert_stmt = price_plans.insert().values(
                    id=p.name,
                    supplier=p.supplier,
                    unit_rate=p.unit_rate
                )
                await database.execute(insert_stmt)

    async def get(self) -> List[PricePlan]:
        rows = await database.fetch_all(price_plans.select())
        return [PricePlan(r["id"], r["supplier"], r["unit_rate"]) for r in rows]

price_plan_repository = PricePlanRepository()
