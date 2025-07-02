from __future__ import annotations

from typing import List
import sqlalchemy as sa

from ..domain.price_plan import PricePlan
from ..db import database, price_plans


class PricePlanRepository:
    """Async MySQL-backed repository for `price_plans`."""

    async def store(self, plans: List[PricePlan]) -> None:
        """Insert price plans.  If plan_id already exists, do nothing."""
        for p in plans:
            exists = await database.fetch_one(
                price_plans
                .select()
                .with_only_columns(price_plans.c.plan_id)
                .where(price_plans.c.plan_id == p.name)
            )
            if exists is None:
                await database.execute(
                    price_plans.insert().values(
                        plan_id=p.name,
                        supplier=p.supplier,
                        unit_rate=p.unit_rate,
                    )
                )

    async def get(self) -> List[PricePlan]:
        rows = await database.fetch_all(price_plans.select())
        return [PricePlan(r["plan_id"], r["supplier"], r["unit_rate"]) for r in rows]


price_plan_repository = PricePlanRepository()
