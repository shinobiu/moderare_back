import logging
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from typing import Optional

from models.Pessoa import Pessoa
from core.security import PasswordService, JWTService
from core.policies.password_policy import PasswordPolicy
from core.policies.cpf_policy import CPFPolicy

logger = logging.getLogger(__name__)


class PessoaService:

    def __init__(self, db: Session):
        self.db = db
        self.password_service = PasswordService()
        self.jwt_service = JWTService()

    # =========================
    # CADASTRO
    # =========================
    def cadastrar(
        self,
        email: str,
        senha: str,
        nome: str,
        aceito_termos: bool,
        aceito_privacidade: bool,
    ) -> Pessoa:

        email = email.strip().lower()
        logger.info("Iniciando cadastro email=%s", email)

        # 🔒 valida aceite obrigatório
        if not aceito_termos or not aceito_privacidade:
            logger.warning(
                "Cadastro recusado (termos não aceitos) email=%s",
                email
            )
            raise ValueError(
                "É obrigatório aceitar os termos e a política de privacidade."
            )

        # 🔐 valida senha
        try:
            PasswordPolicy.validate(senha)
        except ValueError as e:
            logger.warning(
                "Cadastro recusado (senha inválida) email=%s motivo=%s",
                email,
                str(e)
            )
            raise

        # 📧 valida email duplicado
        if self.db.query(Pessoa).filter(Pessoa.e_mail == email).first():
            logger.warning(
                "Cadastro recusado (email duplicado) email=%s",
                email
            )
            raise ValueError("Email já cadastrado")

        agora = datetime.utcnow()

        pessoa = Pessoa(
            e_mail=email,
            senha_hash=self.password_service.hash(senha),
            nome=nome,
            criado_em=agora,
            atualizado_em=agora,
            ativo=True,
            email_verificado=False,
            aceito_termos=True,
            aceito_termos_em=agora,
            aceito_privacidade=True,
            aceito_privacidade_em=agora
        )

        self.db.add(pessoa)
        self.db.commit()
        self.db.refresh(pessoa)

        logger.info(
            "Cadastro realizado com sucesso pessoa_id=%s email=%s",
            pessoa.id,
            email
        )

        return pessoa

    # =========================
    # LOGIN
    # =========================
    def autenticar(self, email: str, senha: str) -> str:

        email = email.strip().lower()
        logger.info("Tentativa de login email=%s", email)

        pessoa = self.db.query(Pessoa).filter(Pessoa.e_mail == email).first()

        if not pessoa:
            raise ValueError("Credenciais inválidas")

        if not pessoa.ativo:
            raise ValueError("Usuário inativo")

        if not self.password_service.verify(senha, pessoa.senha_hash):
            raise ValueError("Credenciais inválidas")

        pessoa.ultimo_login_em = datetime.utcnow()
        self.db.commit()

        token = self.jwt_service.create(str(pessoa.id))

        logger.info(
            "Login realizado com sucesso pessoa_id=%s email=%s",
            pessoa.id,
            email
        )

        return token

    # =========================
    # ATUALIZAÇÃO
    # =========================
    def atualizar_dados(
        self,
        pessoa_id: UUID,
        nome: Optional[str],
        e_mail: Optional[str],
        senha_atual: Optional[str],
        nova_senha: Optional[str]
    ) -> Pessoa:

        logger.info("Iniciando atualização pessoa_id=%s", pessoa_id)

        pessoa = self.db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

        if not pessoa:
            raise ValueError("Usuário não encontrado")

        # -------- SENHA --------
        if nova_senha is not None:

            if not senha_atual:
                raise ValueError("Senha atual é obrigatória para alterar a senha")

            if not self.password_service.verify(senha_atual, pessoa.senha_hash):
                raise ValueError("Senha atual inválida")

            PasswordPolicy.validate(nova_senha)

            pessoa.senha_hash = self.password_service.hash(nova_senha)

            logger.info("Senha alterada pessoa_id=%s", pessoa_id)

        # -------- EMAIL --------
        if e_mail is not None:

            email_normalizado = e_mail.strip().lower()

            if email_normalizado != pessoa.e_mail:

                if (
                    self.db.query(Pessoa)
                    .filter(Pessoa.e_mail == email_normalizado, Pessoa.id != pessoa.id)
                    .first()
                ):
                    raise ValueError("Email já cadastrado")

                pessoa.e_mail = email_normalizado
                pessoa.email_verificado = False
                pessoa.email_verificado_em = None

                logger.info("Email alterado pessoa_id=%s", pessoa_id)

        # -------- NOME --------
        if nome is not None:
            pessoa.nome = nome.strip()

        pessoa.atualizado_em = datetime.utcnow()

        self.db.commit()
        self.db.refresh(pessoa)

        logger.info("Atualização concluída pessoa_id=%s", pessoa_id)

        return pessoa

    # =========================
    # BUSCAR POR ID
    # =========================
    def obter_por_id(self, pessoa_id: UUID) -> Pessoa:

        pessoa = (
            self.db.query(Pessoa)
            .filter(Pessoa.id == pessoa_id)
            .first()
        )

        if not pessoa:
            raise ValueError("Usuário não encontrado")

        return pessoa