import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.INTEGER(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), autoincrement=False, nullable=True)
    email = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True, unique=True)
    phone = sa.Column(sa.VARCHAR(length=16), autoincrement=False, nullable=True, unique=True)
    password = sa.Column(sa.VARCHAR(length=256), autoincrement=False, nullable=True, unique=True)
    first_name = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    last_name = sa.Column(sa.VARCHAR(length=100), autoincrement=False, nullable=True)
    auth_token = sa.Column(sa.VARCHAR(length=128), autoincrement=False, nullable=True, unique=True)
    auth_token_valid_to = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    user_role_id = sa.Column(sa.INTEGER(), sa.ForeignKey("roles.id"), autoincrement=False, nullable=True)
    is_active = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    is_verified = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    is_visible = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=False)
    tos = sa.Column(sa.BOOLEAN(), autoincrement=False, nullable=True)
    tz = sa.Column(sa.VARCHAR(length=64), autoincrement=False, nullable=True, unique=True)
    lang = sa.Column(sa.VARCHAR(length=8), autoincrement=False, nullable=True, unique=True)
    tenant_id = sa.Column(sa.VARCHAR(length=64), autoincrement=False, nullable=True)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
    deleted_at = sa.Column(sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True)
