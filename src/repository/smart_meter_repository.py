from ..db import database, smart_meters, price_plans

class SmartMeterRepository:
    async def store(self, smart_meter_id: str, price_plan_name: str):
        # Look up the numeric PK for the given price-plan name (SQLAlchemy 2.0+ syntax)
        row = await database.fetch_one(
            price_plans
                .select()
                .with_only_columns(price_plans.c.plan_id)
                .where(price_plans.c.id == price_plan_name)
        )
        if row is None:
            raise ValueError(f"Unknown price plan '{price_plan_name}'")
        plan_pk = row["plan_id"]

        # Insert (or ignore if already exists) the new meter
        query = smart_meters.insert().prefix_with("IGNORE").values(
            smart_meter_id=smart_meter_id,
            price_plan_id=plan_pk
        )
        await database.execute(query)

    async def get_price_plan(self, smart_meter_id: str) -> str | None:
        q = smart_meters.select().where(smart_meters.c.smart_meter_id == smart_meter_id)
        row = await database.fetch_one(q)
        return row["price_plan_id"] if row else None

# Singleton instance
smart_meter_repository = SmartMeterRepository()
