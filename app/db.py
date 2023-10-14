from contextlib import asynccontextmanager

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, async_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

metadata = sa.MetaData(schema="tn")
Base = declarative_base(metadata=metadata)


# async def get_session() -> AsyncSession:
#     async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#     async with async_session() as session:
#         yield session


async def get_session():
    async with with_db("xxx") as db:
        yield db
    # --------------------


# for async support
@asynccontextmanager
async def with_db(tenant_schema: str | None):
    if tenant_schema:
        schema_translate_map = {"tenant": tenant_schema}
    else:
        schema_translate_map = None

    connectable = engine.execution_options(schema_translate_map=schema_translate_map)
    try:
        async with async_session(autocommit=False, autoflush=False, bind=connectable) as session:
            yield session
    except Exception as e:
        logger.error(e)
        await session.rollback()
        print("ERRRR: " + tenant_schema)
    finally:
        await session.close()

# https://github.com/sqlalchemy/sqlalchemy/discussions/10024
