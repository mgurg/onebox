from fastapi_pagination import Params
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.models import User


def get_users(sort_column: str | None = None, sort_order: str | None = None, search: str | None = None):
    query = select(User).where(User.deleted_at.is_(None)).where(User.is_visible.is_(True)).order_by(User.id.desc())

    return query

    # all_filters = []
    # if search is not None:
    #     all_filters.append(func.concat(User.first_name, " ", User.last_name).ilike(f"%{search}%"))
    #
    #     query = query.filter(*all_filters)

    # result = await db.execute(query.options(selectinload(User.role_FK)))  # await db.execute(query)

    # return result.scalars().all()
    # return query.options(selectinload(User.role_FK))
    # result = db.execute(query)  # await db.execute(query)
    #
    # return result.scalars().all()


async def get_usrs(db: AsyncSession, params: Params):
    ...


# https://github.com/ruslands/auth-service/blob/8b06c87c69b693262f7b0bd05eceee66fd6f864c/core/base/crud.py#L90
