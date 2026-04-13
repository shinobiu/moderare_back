from uuid import UUID
from sqlalchemy.orm import Session

from models.MetaStreak import MetaStreak
from models.Streak import Streak
from models.Habito import Habito


class MetaStreakService:

    def __init__(self, db: Session):
        self.db = db
        
    def listar_habitos(self):
        habitos = self.db.query(Habito).filter(
            Habito.ativo == True
        ).order_by(Habito.nome.asc()).all()

        return [
            {
                "id": h.id,
                "nome": h.nome,
                "categoria": h.categoria
            }
            for h in habitos
        ]

    # =========================
    # CRIAR META
    # =========================
    def criar_meta(
        self,
        pessoa_id: UUID,
        meta_dias: int,
        habito_id: UUID | None = None,
        descricao_custom: str | None = None
    ) -> MetaStreak:

        # validações básicas
        if meta_dias <= 0:
            raise ValueError("Meta deve ser maior que zero")

        if not habito_id and not descricao_custom:
            raise ValueError("Informe um hábito ou descrição")

        if habito_id and descricao_custom:
            raise ValueError("Escolha apenas um: hábito ou descrição")

        # valida hábito
        if habito_id:
            habito = self.db.query(Habito).filter(
                Habito.id == habito_id,
                Habito.ativo == True
            ).first()

            if not habito:
                raise ValueError("Hábito inválido")

        # normaliza descrição
        if descricao_custom:
            descricao_custom = descricao_custom.strip().capitalize()

        # valida meta ativa (por hábito ou custom)
        query = self.db.query(MetaStreak).filter(
            MetaStreak.pessoa_id == pessoa_id,
            MetaStreak.ativo == True
        )

        if habito_id:
            query = query.filter(MetaStreak.habito_id == habito_id)

        if descricao_custom:
            query = query.filter(MetaStreak.descricao_custom == descricao_custom)

        meta_ativa = query.first()

        if meta_ativa:
            raise ValueError("Já existe uma meta ativa para esse hábito")

        # busca streak
        streak = self.db.query(Streak).filter(
            Streak.pessoa_id == pessoa_id
        ).first()

        if not streak:
            raise ValueError("Usuário ainda não possui streak")

        # cria meta
        meta = MetaStreak(
            pessoa_id=pessoa_id,
            meta_dias=meta_dias,
            streak_inicial=streak.dias,
            habito_id=habito_id,
            descricao_custom=descricao_custom
        )

        self.db.add(meta)
        self.db.commit()
        self.db.refresh(meta)

        return meta

    # =========================
    # META ATIVA (STATUS)
    # =========================
    def obter_meta_ativa(self, pessoa_id: UUID):

        meta = self.db.query(MetaStreak).filter(
            MetaStreak.pessoa_id == pessoa_id,
            MetaStreak.ativo == True
        ).order_by(MetaStreak.criado_em.desc()).first()

        if not meta:
            return None

        streak = self.db.query(Streak).filter(
            Streak.pessoa_id == pessoa_id
        ).first()

        if not streak:
            raise ValueError("Streak não encontrado")

        progresso = max(streak.dias - meta.streak_inicial, 0)

        porcentagem = (
            min((progresso / meta.meta_dias) * 100, 100)
            if meta.meta_dias > 0 else 0
        )

        concluida = progresso >= meta.meta_dias

        return {
            "meta_dias": meta.meta_dias,
            "progresso": progresso,
            "streak_atual": streak.dias,
            "concluida": concluida,
            "porcentagem": porcentagem,

            # identificação
            "habito_nome": meta.habito.nome if meta.habito else None,
            "descricao_custom": meta.descricao_custom,

            # pronto pro front
            "titulo": meta.habito.nome if meta.habito else meta.descricao_custom
        }

    def cancelar_meta(self, pessoa_id: UUID):
        meta = self.db.query(MetaStreak).filter(
            MetaStreak.pessoa_id == pessoa_id,
            MetaStreak.ativo == True
        ).order_by(MetaStreak.criado_em.desc()).first()
        if not meta:
            return None
        
        streak = self.db.query(Streak).filter(
            Streak.pessoa_id == pessoa_id
        ).first()

        if not streak:
            raise ValueError("Streak não encontrado")
        
        meta.ativo = False
        self.db.commit()
        self.db.refresh(meta)

        return meta
        