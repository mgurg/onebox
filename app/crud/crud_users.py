from sqlalchemy import Select, func, select, text
from sqlalchemy.orm import selectinload

from app.models.models import User


async def get_users(sort_column: str, sort_order: str, search: str | None = None) -> Select[tuple[User]]:
    query = (
        select(User)
        .where(User.deleted_at.is_(None))
        .where(User.is_visible.is_(True))
        .order_by(text(f"{sort_column} {sort_order}"))
    )

    all_filters = []
    if search is not None:
        all_filters.append(func.concat(User.first_name, " ", User.last_name).ilike(f"%{search}%"))

        query = query.filter(*all_filters)

    # result = await db.execute(query.options(selectinload(User.role_FK)))  # await db.execute(query)

    # return result.scalars().all()
    return query.options(selectinload(User.role_FK))
    # result = db.execute(query)  # await db.execute(query)
    #
    # return result.scalars().all()
