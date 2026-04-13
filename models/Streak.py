import uuid
from datetime import date, datetime

from sqlalchemy import Integer, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base

class Streak(Base):
    __tablename__ = "streak"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    pessoa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.pessoa.id"),
        nullable=False,
        unique=True
    )

    dias: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    data_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    ultimo_checkin: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )