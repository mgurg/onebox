from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_users
from app.db import get_session
from app.schemas.responses.responses import UserIndexResponse

user_router = APIRouter()
UserDB = Annotated[AsyncSession, Depends(get_session)]


@user_router.get("/", response_model=Page[UserIndexResponse])
async def user_get_all(
    *,
    db: UserDB,
    params: Annotated[Params, Depends()],
    # search: Annotated[str | None, Query(max_length=50)] = None,
    search: str | None = None,
    field: str = "name",
    order: str = "asc",
):
    if field not in ["first_name", "last_name", "created_at"]:
        field = "last_name"

    db_users_query = crud_users.get_users()

    # db_users_query = select(User)

    # result = db.execute(db_users_query)  # await db.execute(query)
    # db_users = result.scalars().all()

    return await paginate(db, db_users_query)


@user_router.get("/{user_uuid}")
async def user_get_one(user_uuid: UUID):
    return "OK"


@user_router.post("/")
async def user_add_all():
    return "OK"


@user_router.patch("/{user_uuid}")
async def user_edit_one(user_uuid: UUID):
    return "OK"


@user_router.delete("/{user_uuid}")
async def user_delete_one(user_uuid: UUID):
    return "OK"
