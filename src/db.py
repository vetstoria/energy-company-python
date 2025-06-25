"""
Central async-database helper.

The module exposes
    • metadata – SQLAlchemy Core MetaData (table registry)
    • database – `databases.Database` instance (aiomysql URL)
    • electricity_readings / price_plans – SQLAlchemy Table objects
    • create_tables() – idempotent bootstrap called on startup
"""
from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
from databases import Database
import sqlalchemy as sa

# --------------------------------------------------------------------------- #
# Connection URL                                                              #
# --------------------------------------------------------------------------- #
DB_USER = os.getenv("DB_USER", "energymeter")
DB_PASS = os.getenv("DB_PASSWORD", "energypass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "energy_db")

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
    sa.Column("id", sa.String(64), primary_key=True),
    sa.Column("supplier", sa.String(128), nullable=False),
    sa.Column("unit_rate", sa.Float, nullable=False),
)


def create_tables() -> None:
    """
    Idempotently create tables if they do not yet exist.
    Executed with a *synchronous* SQLAlchemy engine because MySQL
    `CREATE TABLE …` is DDL and only needs to run once.
    """
    from sqlalchemy import create_engine

    # NEW: forces pymysql to avoid MySQLdb crash
    sync_url = DATABASE_URL.replace("+aiomysql", "+pymysql")

    engine = create_engine(
        sync_url,
        future=True,
    )
    metadata.create_all(engine, checkfirst=True)
