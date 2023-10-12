"""Add user tables

Revision ID: f77d8db8fbd7
Revises: cdef3b7288aa
Create Date: 2023-10-13 15:00:20.380478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f77d8db8fbd7'
down_revision: Union[str, None] = 'cdef3b7288aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), sa.Identity(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(as_uuid=True), autoincrement=False, nullable=False, index=True),
        sa.Column("email", sa.VARCHAR(length=256), autoincrement=False, nullable=False),
        sa.Column("phone", sa.VARCHAR(length=16), autoincrement=False, nullable=True),
        sa.Column("password", sa.VARCHAR(length=256), autoincrement=False, nullable=True),
        sa.Column("tos", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("first_name", sa.VARCHAR(length=100), autoincrement=False, nullable=True),
        sa.Column("last_name", sa.VARCHAR(length=100), autoincrement=False, nullable=True),
        sa.Column("user_role_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("auth_token", sa.VARCHAR(length=128), autoincrement=False, nullable=True, unique=True),
        sa.Column("auth_token_valid_to", sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_verified", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("is_visible", sa.BOOLEAN(), autoincrement=False, nullable=True, default=True),
        sa.Column("service_token", sa.VARCHAR(length=100), autoincrement=False, nullable=True, unique=True),
        sa.Column("service_token_valid_to", sa.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column("tz", sa.VARCHAR(length=64), autoincrement=False, nullable=False),
        sa.Column("lang", sa.VARCHAR(length=8), autoincrement=False, nullable=False),
        sa.Column("tenant_id", sa.VARCHAR(length=64), autoincrement=False, nullable=True),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column("updated_at", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column("deleted_at", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        schema=None,
    )


def downgrade() -> None:
    pass
