from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_public_user
from app.db import get_session

auth_router = APIRouter()

PublicDB = Annotated[AsyncSession, Depends(get_session)]

@auth_router.get("/account_limit")
async def auth_account_limit(*, public_db: PublicDB):  # *, public_db: PublicDB

    public_user = await crud_public_user.get_public_user_by_email(public_db, "m@m.pl")
    return public_user
    # db_companies_no = crud_auth.get_public_company_count(public_db)
    # limit = 120
    #
    # return {"accounts": db_companies_no, "limit": limit}
