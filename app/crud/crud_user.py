from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User


async def get_user_by_email(db: AsyncSession, email: EmailStr) -> User | None:
    query = select(User).where(User.email == email)

    result = await db.execute(query)  # await db.execute(query)

    return result.scalar_one_or_none()
