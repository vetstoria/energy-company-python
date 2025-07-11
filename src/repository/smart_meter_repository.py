from ..db import database, smart_meters, price_plans


class SmartMeterRepository:
    async def store(self, smart_meter_id: str, price_plan_name: str) -> None:
        # Look up numeric PK of the price plan
        row = await database.fetch_one(
            price_plans
            .select()
            .with_only_columns(price_plans.c.id)          # ⇽ PK bigint
            .where(price_plans.c.plan_id == price_plan_name)
        )
        if row is None:
            raise ValueError(f"Unknown price plan '{price_plan_name}'")
        plan_pk = row["id"]

        # Insert meter (IGNORE duplicates)
        await database.execute(
            smart_meters.insert().prefix_with("IGNORE").values(
                smart_meter_id=smart_meter_id,
                price_plan_id=plan_pk,
            )
        )

    async def get_price_plan(self, smart_meter_id: str) -> int | None:
        row = await database.fetch_one(
            smart_meters.select().where(smart_meters.c.smart_meter_id == smart_meter_id)
        )
        return row["price_plan_id"] if row else None


    async def get_meter_by_identifier(self, smart_meter_id: str) -> dict | None:
        """
        Look up the full smart_meter row by its string identifier.
        Returns None if not found.
        """
        query = smart_meters.select().where(smart_meters.c.smart_meter_id == smart_meter_id)
        return await database.fetch_one(query)

smart_meter_repository = SmartMeterRepository()
