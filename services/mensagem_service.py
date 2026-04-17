import random
from fastapi import HTTPException
from sqlalchemy.orm import Session

from services.ai_service import AIService
from services.ia_usage_service import IAUsageService
from schemas.ia_usage import TipoMensagem
from models.mensagem_ia import MensagemIA
from models.mensagem_usuario import MensagemUsuario


class MensagemService:

    def __init__(self, db: Session):
        self.db = db
        self.ai = AIService()
        self.ia_usage = IAUsageService(db)


    def buscar_mensagem(self, dias: int, perdeu: bool, tipo: TipoMensagem, humor):

        mensagens = self.db.query(MensagemIA).filter(
            MensagemIA.tipo == tipo.value,
            MensagemIA.ativo == True,
            MensagemIA.perdeu_streak == perdeu,
            MensagemIA.contexto_min_dias <= dias,
            MensagemIA.contexto_max_dias >= dias
        ).all()

        if mensagens:
            msg = random.choice(mensagens)

            msg.score_uso += 1
            self.db.commit()

            return msg.mensagem

        return None

    def salvar_mensagem(self, texto: str, dias: int, perdeu: bool, tipo: TipoMensagem):

        nova = MensagemIA(
            tipo=tipo.value,
            mensagem=texto,
            perdeu_streak=perdeu,
            contexto_min_dias=max(dias - 2, 0),
            contexto_max_dias=dias + 2
        )

        self.db.add(nova)
        self.db.commit()
        
    def salvar_mensagem_usuario(self, texto: str, pessoa_id, tipo: TipoMensagem):
        mensagem = self.db.query(MensagemUsuario).filter(MensagemUsuario.pessoa_id == pessoa_id).filter(MensagemUsuario.tipo == tipo.value).first()
        if not mensagem:
            nova = MensagemUsuario(
                tipo=tipo.value,
                conteudo = texto,
                pessoa_id = pessoa_id
            )
            self.db.add(nova)
            self.db.commit()
            self.db.refresh(nova)
            return nova
        mensagem.conteudo = texto
        self.db.commit()
            

    def get_mensagem_checkin(self, pessoa_id, dias: int, perdeu: bool, humor):

        tipo = TipoMensagem.CHECKIN

        mensagem = self.buscar_mensagem(dias, perdeu, tipo, humor)

        if self.ia_usage.pode_usar_ia(pessoa_id, tipo):
            mensagem = self.ai.gerar_mensagem_checkin(dias, perdeu, humor)

            self.salvar_mensagem(mensagem, dias, perdeu, tipo)
            self.salvar_mensagem_usuario(mensagem, pessoa_id, tipo)
            self.ia_usage.registrar_uso_ia(pessoa_id, tipo)

            return mensagem
        else:
            return None

    def get_mensagem_relapse(self, pessoa_id, dias: int, perdeu: bool, humor):

        tipo = TipoMensagem.ALERTA

        mensagem = self.buscar_mensagem(dias, perdeu, tipo, humor)

        if self.ia_usage.pode_usar_ia(pessoa_id, tipo):
            mensagem = self.ai.gerar_mensagem_relapse(dias, perdeu, humor)

            self.salvar_mensagem(mensagem, dias, perdeu, tipo)
            self.salvar_mensagem_usuario(mensagem, pessoa_id, tipo)
            self.ia_usage.registrar_uso_ia(pessoa_id, tipo)

            return mensagem
        else:
            return None

    def get_mensagem_usuario(self, pessoa_id, tipo):
        mensagem = self.db.query(MensagemUsuario).filter(MensagemUsuario.pessoa_id == pessoa_id).filter(MensagemUsuario.tipo == tipo).first()
        return mensagem    
        