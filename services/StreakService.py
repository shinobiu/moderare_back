from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.MetaStreak import cancela

from models.Streak import Streak
from schemas.Streak import StreakResponse, CheckinRequest
from models.MetaStreak import MetaStreak
from services.mensagem_service import MensagemService


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
    def checkin(self, pessoa_id: UUID, humor):

        hoje = datetime.utcnow().date()

        streak = self.get_or_create(pessoa_id)

        if streak.ultimo_checkin == hoje:
            raise HTTPException(
                status_code=400,
                detail="Check-in já realizado hoje"
            )
            
        perdeu = False
            
        if streak.ultimo_checkin is None:
            streak.dias = 1
            streak.data_inicio = hoje

        elif streak.ultimo_checkin == hoje - timedelta(days=1):
            streak.dias += 1
            if streak.recorde <= streak.dias:
                streak.recorde = streak.dias

        else:
            streak.dias = 1
            streak.data_inicio = hoje
            perdeu = True

        streak.ultimo_checkin = hoje

        mensagem = MensagemService(self.db).get_mensagem_checkin(
            pessoa_id=pessoa_id,
            dias=streak.dias,
            perdeu=perdeu,
            humor=humor
            )

        self.db.commit()
        self.db.refresh(streak)

        return {
            "dias_streak": streak.dias,
            "mensagem": mensagem,
            "perdeu_streak": perdeu
        }
    

    def obter_status(self, pessoa_id: UUID):
        
        streak = self.get_or_create(pessoa_id)
        hoje = datetime.utcnow().date()
        ontem = hoje - timedelta(days=1)
        perdeu_streak = ( streak.dias == 0 and streak.ultimo_checkin == hoje)

        if perdeu_streak:
            mensagem = MensagemService(self.db).get_mensagem_usuario(
            pessoa_id, 'ALERTA'
        )
        else:
            mensagem = MensagemService(self.db).get_mensagem_usuario(
            pessoa_id, 'CHECKIN'
        )

        return {
            "mensagem": mensagem.conteudo if mensagem else None,
            "dias": streak.dias,
            "id": streak.id,
            "data_inicio": streak.data_inicio,
            "ultimo_checkin": streak.ultimo_checkin,
            "recorde": streak.recorde
            }
    
    def reset(self, pessoa_id: UUID, humor):
        streak = self.get_or_create(pessoa_id)

        hoje = datetime.utcnow().date()

        mensagem = MensagemService(self.db).get_mensagem_relapse(
            pessoa_id=pessoa_id,
            dias=streak.dias,
            perdeu=True,
            humor=humor
            )

        streak.dias = 0
        streak.data_inicio = hoje
        streak.ultimo_checkin = hoje
        streak.total_falhas = streak.total_falhas + 1

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
        
        return {
            "dias_streak": streak.dias,
            "mensagem": mensagem,
            "perdeu_streak": True
        }