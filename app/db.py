import time
from contextlib import contextmanager
from functools import lru_cache
from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends, Request
from loguru import logger
from sqlalchemy import create_engine, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()

DEFAULT_DB_USER = settings.DEFAULT_DATABASE_USER
DEFAULT_DB_PASS = settings.DEFAULT_DATABASE_PASSWORD
DEFAULT_DB_HOST = settings.DEFAULT_DATABASE_HOSTNAME
DEFAULT_DB_PORT = settings.DEFAULT_DATABASE_PORT
DEFAULT_DB = settings.DEFAULT_DATABASE_DB
# SQLALCHEMY_DB_URL = settings.DEFAULT_SQLALCHEMY_DATABASE_URI


SQLALCHEMY_DB_URL = f"postgresql+psycopg://{DEFAULT_DB_USER}:{DEFAULT_DB_PASS}@{DEFAULT_DB_HOST}:5432/{DEFAULT_DB}"
echo = False

print("======")
print(SQLALCHEMY_DB_URL)
print("======")

engine = create_async_engine(SQLALCHEMY_DB_URL, echo=echo, pool_pre_ping=True, pool_recycle=280)

metadata = sa.MetaData(schema="tenant")
Base = declarative_base(metadata=metadata)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
