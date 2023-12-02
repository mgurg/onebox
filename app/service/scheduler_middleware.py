from __future__ import annotations

from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.eventbrokers.asyncpg import AsyncpgEventBroker
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send

from app.config import get_settings

settings = get_settings()


class SchedulerMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        scheduler: AsyncScheduler,
    ) -> None:
        self.app = app
        self.scheduler = scheduler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            async with self.scheduler:
                # await self.scheduler.add_schedule(tick, IntervalTrigger(seconds=10), id="tick")
                await self.scheduler.start_in_background()
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)


engine = create_async_engine(settings.DB_CONFIG.unicode_string())
data_store = SQLAlchemyDataStore(engine)
event_broker = AsyncpgEventBroker.from_async_sqla_engine(engine)
scheduler = AsyncScheduler(data_store, event_broker)
middleware = [Middleware(SchedulerMiddleware, scheduler=scheduler)]
