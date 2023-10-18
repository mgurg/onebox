from __future__ import annotations

from datetime import datetime

from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.eventbrokers.asyncpg import AsyncpgEventBroker
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.types import ASGIApp, Receive, Scope, Send

from app.api.auth import auth_router
from app.config import get_settings

settings = get_settings()


def tick():
    print("Hello, the time is", datetime.now())


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


def create_application() -> FastAPI:
    """
    Create base FastAPI app with CORS middlewares and routes loaded
    Returns:
        FastAPI: [description]
    """
    application = FastAPI(middleware=middleware)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["*"],
        max_age=86400,
    )

    # application.add_api_route("/", root)
    application.include_router(auth_router, prefix="/auth", tags=["AUTH"])

    return application


app = create_application()


@app.get("/add_task")
async def root(request: Request) -> Response:
    await scheduler.add_job(tick)
    return PlainTextResponse("Single Job")


@app.get("/start_interval_task")
async def root(request: Request) -> Response:
    await scheduler.add_schedule(tick, IntervalTrigger(seconds=10), id="tick")
    return PlainTextResponse("Tick in 10s")


@app.get("/")
async def root():
    return {"message": "Hello World"}
