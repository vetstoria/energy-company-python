"""
Central async-database helper.

Exposes
    • metadata – SQLAlchemy Core MetaData (table registry)
    • database – `databases.Database`
    • electricity_readings / price_plans / smart_meters – SQLAlchemy Table objects
    • create_tables() – idempotent bootstrap
"""
from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os, time
import sqlalchemy as sa
from databases import Database
from sqlalchemy.exc import OperationalError

# --------------------------------------------------------------------------- #
# Connection URL                                                              #
# --------------------------------------------------------------------------- #
DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME = (
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME"),
)
DATABASE_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

database: Database = Database(
    DATABASE_URL, force_rollback=os.getenv("TESTING") == "1"
)
metadata = sa.MetaData()

# --------------------------------------------------------------------------- #
# Table definitions                                                           #
# --------------------------------------------------------------------------- #
price_plans = sa.Table(
    "price_plans",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),      # ⇽ NEW PK
    sa.Column("plan_id", sa.String(64), nullable=False, unique=True),          # ⇽ String lookup key
    sa.Column("supplier", sa.String(128), nullable=False),
    sa.Column("unit_rate", sa.Float, nullable=False),
)

smart_meters = sa.Table(
    "smart_meters",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("smart_meter_id", sa.String(64), nullable=False, unique=True),
    sa.Column("price_plan_id", sa.BigInteger,
              sa.ForeignKey("price_plans.id"), nullable=False),                # ⇽ FK now targets price_plans.id
)

electricity_readings = sa.Table(
    "electricity_readings",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("smart_meter_id", sa.BigInteger,
              sa.ForeignKey("smart_meters.id"), nullable=False, index=True),   # ⇽ BIGINT FK
    sa.Column("time", sa.BigInteger, nullable=False),
    sa.Column("reading", sa.Float, nullable=False),
)

# --------------------------------------------------------------------------- #
# DDL bootstrap                                                               #
# --------------------------------------------------------------------------- #
def create_tables() -> None:
    """Idempotently create tables, retrying until MySQL is ready."""
    from sqlalchemy import create_engine
    sync_url = DATABASE_URL.replace("+aiomysql", "+pymysql")
    engine = create_engine(sync_url, future=True)

    for attempt in range(1, 11):
        try:
            metadata.create_all(engine, checkfirst=True)
            print("✅ Tables created successfully.")
            break
        except OperationalError:
            print(f" DB not ready (attempt {attempt}/10) — retrying in 3 s…")
            time.sleep(3)
    else:
        raise RuntimeError("❌ Could not connect to MySQL after 10 retries.")
