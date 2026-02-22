import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    CHAR,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Pessoa(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    e_mail: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    cpf: Mapped[str | None] = mapped_column(
        CHAR(11),
        nullable=True,
        unique=True
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    email_verificado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    email_verificado_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    ultimo_login_em: Mapped[datetime | None] = mapped_column(
        DateTime,
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

    codigo_verificacao: Mapped[str | None] = mapped_column(
        CHAR(8),
        nullable=True
    )

    codigo_expira_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    aceito_termos: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    aceito_termos_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    aceito_privacidade: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    aceito_privacidade_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )