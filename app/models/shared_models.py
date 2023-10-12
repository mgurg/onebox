from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

metadata = sa.MetaData(schema="shared")
Base = declarative_base(metadata=metadata)


class Tenant(Base):
    __tablename__ = "tenants"
    id = sa.Column(sa.Integer(), sa.Identity(), primary_key=True, autoincrement=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True), default=uuid4(), unique=True)
    name = sa.Column("name", sa.String(128), nullable=True)
    schema = sa.Column(sa.String(128), nullable=True)
    schema_header_id = sa.Column("schema_header_id", sa.String(128), nullable=True)

    __table_args__ = {"schema": "public"}