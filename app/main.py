from __future__ import annotations

from datetime import datetime

from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response

from app.api.auth import auth_router
from app.config import get_settings
from app.service.scheduler_middleware import scheduler, middleware
from app.service.tenants import alembic_upgrade_head

settings = get_settings()


def tick():
    print("Hello, the time is", datetime.now())


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


@app.get("/register_tenant")
async def register_tenant():
    await alembic_upgrade_head("tn", "head")
    return {"message": "Hello World"}

@app.get("/")
async def root():
    return {"message": "Hello World"}
