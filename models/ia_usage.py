from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime

from core.database import Base


class IAUsage(Base):
    __tablename__ = "ia_usage"

    pessoa_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("public.pessoa.id"),
        primary_key=True,
        nullable=False
    )

    tipo = Column(
        String(50),
        primary_key=True,
        nullable=False
    )

    ultimo_uso = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )