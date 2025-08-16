import sqlalchemy as sa
import sqlalchemy.orm as so
from uuid import UUID
from datetime import datetime
from sqlalchemy.dialects import postgresql

from app.database_settings import Base


class APIKeyUsage(Base):
    """Tracks API key usage for each company."""

    __tablename__ = "ApiKeyUsages"

    id: so.Mapped[UUID] = so.mapped_column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=sa.text("gen_random_uuid()"),
    )

    company_name: so.Mapped[str] = so.mapped_column(
        sa.String(length=255),
        nullable=False,
    )

    api_key: so.Mapped[str] = so.mapped_column(
        sa.String(length=255),
        nullable=False,
        unique=True,
    )

    usage_count: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        nullable=False,
        server_default="0",
    )

    last_request_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
    )
