from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_public_user, crud_user
from app.db import get_session

auth_router = APIRouter()

PublicDB = Annotated[AsyncSession, Depends(get_session)]


@auth_router.get("/public_user")
async def auth_account_limit(*, public_db: PublicDB):  # *, public_db: PublicDB

    public_user = await crud_public_user.get_public_user_by_email(public_db, "m@m.pl")
    return public_user


@auth_router.get("/user")
async def auth_account_limit(*, public_db: PublicDB):  # *, public_db: PublicDB

    user = await crud_user.get_user_by_email(public_db, "mn@mn.pl")
    return user
