from sqlalchemy import Column, String, Boolean, Text, DateTime, UniqueConstraint, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

from core.database import Base


class MensagemUsuario(Base):
    __tablename__ = "mensagem_usuario"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    pessoa_id = Column(PG_UUID(as_uuid=True), ForeignKey("public.pessoa.id"), nullable=False)

    tipo = Column(String(30), nullable=False) 

    conteudo = Column(Text, nullable=False)

    atualizada_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("pessoa_id", "tipo", name="uq_pessoa_tipo"),
    )