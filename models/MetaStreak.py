import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

class MetaStreak(Base): 
    __tablename__ = "meta_streak"
    __table_args__ = {"schema": "public"}

    habito = relationship("Habito")
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    pessoa_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.pessoa.id"),
        nullable=False
    )

    # 🔥 NOVO: hábito (padrão)
    habito_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.habito.id"),
        nullable=True
    )

    # 🔥 NOVO: descrição custom (fallback)
    descricao_custom: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    meta_dias: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    streak_inicial: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    concluida: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )