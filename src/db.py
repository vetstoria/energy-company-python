"""
Central async-database helper.

The module exposes
    • metadata – SQLAlchemy Core MetaData (table registry)
    • database – `databases.Database` instance (aiomysql URL)
    • electricity_readings / price_plans / smart_meters – SQLAlchemy Table objects
    • create_tables() – idempotent bootstrap called on startup
"""
from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import time
from databases import Database
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError

# --------------------------------------------------------------------------- #
# Connection URL                                                              #
# --------------------------------------------------------------------------- #
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# When TESTING=1 we force a rollback after every request.
database: Database = Database(
    DATABASE_URL, force_rollback=os.getenv("TESTING") == "1"
)

metadata = sa.MetaData()

# --------------------------------------------------------------------------- #
# Table definitions – reflected into MySQL on startup                         #
# --------------------------------------------------------------------------- #
electricity_readings = sa.Table(
    "electricity_readings",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("smart_meter_id", sa.String(64), nullable=False, index=True),
    sa.Column("time", sa.BigInteger, nullable=False),
    sa.Column("reading", sa.Float, nullable=False),
)

price_plans = sa.Table(
    "price_plans",
    metadata,
    sa.Column("plan_id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("id", sa.String(64), nullable=False, unique=True),  # Still unique for lookups
    sa.Column("supplier", sa.String(128), nullable=False),
    sa.Column("unit_rate", sa.Float, nullable=False),
)

smart_meters = sa.Table(
    "smart_meters",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("smart_meter_id", sa.String(64), nullable=False, unique=True),  # Still unique for lookups
    sa.Column("price_plan_id", sa.BigInteger, sa.ForeignKey("price_plans.plan_id"), nullable=False),
)

# --------------------------------------------------------------------------- #
# Create tables with retry loop to wait for MySQL readiness                   #
# --------------------------------------------------------------------------- #
def create_tables() -> None:
    """
    Idempotently create tables if they do not yet exist.
    Retries if DB isn't ready yet (e.g., in Docker).
    """
    from sqlalchemy import create_engine

    sync_url = DATABASE_URL.replace("+aiomysql", "+pymysql")
    engine = create_engine(sync_url, future=True)

    max_retries = 10
    for attempt in range(1, max_retries + 1):
        try:
            metadata.create_all(engine, checkfirst=True)
            print("✅ Tables created successfully.")
            break
        except OperationalError as e:
            print(f" DB not ready (attempt {attempt}/{max_retries}) — retrying in 3s...")
            time.sleep(3)
    else:
        raise RuntimeError("❌ Could not connect to MySQL after 10 retries.")
