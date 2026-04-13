from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.MetaStreak import cancela

from models.Streak import Streak
from schemas.Streak import StreakResponse
from models.MetaStreak import MetaStreak


class StreakService:

    def __init__(self, db: Session):
        self.db = db

    # =========================
    # GET OU CREATE
    # =========================
    def get_or_create(self, pessoa_id: UUID) -> Streak:

        streak = (
            self.db.query(Streak)
            .filter(Streak.pessoa_id == pessoa_id)
            .first()
        )

        hoje = datetime.utcnow().date()
        ontem = hoje - timedelta(days=1)
        
        perdeu_streak = ( streak.ultimo_checkin is not None and streak.ultimo_checkin < ontem)
        
        if not streak:
            streak = Streak(
                pessoa_id=pessoa_id,
                dias=0,
                data_inicio=hoje
            )
            self.db.add(streak)
            self.db.commit()
            self.db.refresh(streak)
        elif perdeu_streak:
            streak.dias = 0
            streak.data_inicio = hoje
            streak.ultimo_checkin = None

            self.db.commit()
            self.db.refresh(streak)


        return streak

    # =========================
    # CHECKIN
    # =========================
    def checkin(self, pessoa_id: UUID):

        hoje = datetime.utcnow().date()

        streak = self.get_or_create(pessoa_id)

        if streak.ultimo_checkin == hoje:
            raise HTTPException(
        status_code=400,
        detail="Check-in já realizado hoje"
    )

        if streak.ultimo_checkin is None:
            streak.dias = 1
            streak.data_inicio = hoje

        elif streak.ultimo_checkin == hoje - timedelta(days=1):
            streak.dias += 1
        else:
            streak.dias = 1
            streak.data_inicio = hoje

        streak.ultimo_checkin = hoje

        self.db.commit()
        self.db.refresh(streak)

        return StreakResponse.model_validate(streak)
    # =========================
    # STATUS
    # =========================
    def obter_status(self, pessoa_id: UUID) -> Streak:
        return self.get_or_create(pessoa_id)
    
    def reset(self, pessoa_id: UUID):
        streak = self.get_or_create(pessoa_id)

        hoje = datetime.utcnow().date()

        streak.dias = 0
        streak.data_inicio = hoje
        streak.ultimo_checkin = None

        self.db.commit()
        self.db.refresh(streak)
        
        meta = self.db.query(MetaStreak).filter(
            MetaStreak.pessoa_id == pessoa_id,
            MetaStreak.ativo == True
        ).order_by(MetaStreak.criado_em.desc()).first()
        if not meta:
            pass
        else:
            meta.streak_inicial = 0
            self.db.commit()
            self.db.refresh(meta)
        
                
        
        
        streak = self.db.query(Streak).filter(
            Streak.pessoa_id == pessoa_id
        ).first()

        if not streak:
            raise ValueError("Streak não encontrado")
        


        return StreakResponse.model_validate(streak)