from sqlalchemy.orm import Session
from datetime import datetime, timezone
from uuid import UUID

from models.ia_usage import IAUsage
from schemas.ia_usage import TipoMensagem


class IAUsageService:

    def __init__(self, db: Session):
        self.db = db

    # =========================
    # VERIFICAR SE PODE USAR IA
    # =========================
    def pode_usar_ia(self, pessoa_id: UUID, tipo: TipoMensagem) -> bool:
        uso = self.db.query(IAUsage).filter_by(
            pessoa_id=pessoa_id,
            tipo=tipo.value
        ).first()

        hoje = datetime.now(timezone.utc).date()

        if not uso:
            return True

        return uso.ultimo_uso.date() < hoje

    # =========================
    # REGISTRAR USO
    # =========================
    def registrar_uso_ia(self, pessoa_id: UUID, tipo: TipoMensagem):
        uso = self.db.query(IAUsage).filter_by(
            pessoa_id=pessoa_id,
            tipo=tipo.value
        ).first()

        if not uso:
            uso = IAUsage(
                pessoa_id=pessoa_id,
                tipo=tipo.value
            )

        uso.ultimo_uso = datetime.utcnow()

        self.db.add(uso)
        self.db.commit()