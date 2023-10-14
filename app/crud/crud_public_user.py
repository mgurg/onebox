from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shared_models import PublicUser


async def get_public_user_by_email(db: AsyncSession, email: EmailStr) -> PublicUser | None:
    query = select(PublicUser).where(PublicUser.email == email)

    result = await db.execute(query)  # await db.execute(query)

    return result.scalar_one_or_none()
