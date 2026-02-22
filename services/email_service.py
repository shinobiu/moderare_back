from datetime import datetime, timedelta
import smtplib
import ssl
import logging
from email.message import EmailMessage
import uuid
from core.config import settings
from models.Pessoa import Pessoa

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM
        
    def gerar_token_confirmacao(self, pessoa: Pessoa) -> str:
      token = uuid.uuid4().hex

      pessoa.codigo_verificacao = token
      pessoa.codigo_expira_em = datetime.utcnow() + timedelta(minutes=30)
      pessoa.email_verificado = False

      self.db.commit()

      return token


    def enviar_confirmacao(self, destino: str, token: str):
        link = f"{settings.APP_URL}/auth/confirmar-email?token={token}"

        assunto = "Confirme seu e-mail"
        corpo_texto = f"""
Olá,

Para confirmar seu e-mail, clique no link abaixo:

{link}

Se você não criou esta conta, ignore este e-mail.
"""

        corpo_html = f"""
<html>
  <body>
    <p>Olá,</p>
    <p>Para confirmar seu e-mail, clique no botão abaixo:</p>
    <p>
      <a href="{link}" style="
        display:inline-block;
        padding:10px 15px;
        background-color:#4CAF50;
        color:#ffffff;
        text-decoration:none;
        border-radius:4px;
      ">
        Confirmar e-mail
      </a>
    </p>
    <p>Se você não criou esta conta, ignore este e-mail.</p>
  </body>
</html>
"""

        msg = EmailMessage()
        msg["From"] = self.from_email
        msg["To"] = destino
        msg["Subject"] = assunto
        msg.set_content(corpo_texto)
        msg.add_alternative(corpo_html, subtype="html")

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls(context=context)
                server.login(self.user, self.password)
                server.send_message(msg)

            logger.info("Email de confirmação enviado para %s", destino)

        except Exception as e:
            logger.error(
                "Falha ao enviar email destino=%s erro=%s",
                destino,
                str(e)
            )
            raise
