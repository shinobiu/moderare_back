from sqlalchemy import Column, String, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

from core.database import Base


class MensagemIA(Base):
    __tablename__ = "mensagens_ia"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tipo = Column(String(50), nullable=False)
    mensagem = Column(Text, nullable=False)

    contexto_min_dias = Column(Integer)
    contexto_max_dias = Column(Integer)

    perdeu_streak = Column(Boolean)

    ativo = Column(Boolean, default=True)
    score_uso = Column(Integer, default=0)