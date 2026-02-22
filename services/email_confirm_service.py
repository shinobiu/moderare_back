import secrets
import string
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.Pessoa import Pessoa
import logging


logger = logging.getLogger(__name__)


class EmailConfirmService:
    TOKEN_EXPIRACAO_MINUTOS = 30
    
    
    def __init__(self, db: Session):
        self.db = db

    def gerar_token_confirmacao(self, pessoa: Pessoa) -> str:
        alfabeto = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alfabeto) for _ in range(8))

        pessoa.codigo_verificacao = token
        pessoa.codigo_expira_em = datetime.utcnow() + timedelta(
            minutes=self.TOKEN_EXPIRACAO_MINUTOS
        )
        pessoa.email_verificado = False

        self.db.commit()

        logger.info(
            "Token de confirmação gerado pessoa_id=%s expira_em=%s",
            pessoa.id,
            pessoa.codigo_expira_em
        )

        return token

    def confirmar_email(self, token: str):
        pessoa = (
            self.db.query(Pessoa)
            .filter(Pessoa.codigo_verificacao == token)
            .first()
        )

        if not pessoa:
            logger.warning("Confirmação de email falhou (token inválido)")
            raise ValueError("Token inválido")

        if not pessoa.codigo_expira_em or pessoa.codigo_expira_em < datetime.utcnow():
            logger.warning(
                "Confirmação de email falhou (token expirado) pessoa_id=%s",
                pessoa.id
            )
            raise ValueError("Token expirado")

        pessoa.email_verificado = True
        pessoa.codigo_verificacao = None
        pessoa.codigo_expira_em = None

        self.db.commit()

        logger.info("Email confirmado com sucesso pessoa_id=%s", pessoa.id)
