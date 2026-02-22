from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv()

        self.APP_NAME = os.getenv("APP_NAME", "Vicio API")
        self.ENV = os.getenv("ENV", "development")
        
        self.APP_URL = os.getenv("APP_URL")

        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.SMTP_HOST = os.getenv("SMTP_HOST")
        self.SMTP_PORT= os.getenv("SMTP_PORT")
        self.SMTP_USER= os.getenv("SMTP_USER")
        self.SMTP_PASSWORD= os.getenv("SMTP_PASSWORD")
        self.SMTP_FROM = os.getenv("SMTP_FROM")

        if not all([
            self.DB_HOST,
            self.DB_NAME,
            self.DB_USER,
            self.DB_PASSWORD
        ]):
            raise RuntimeError("Configuração do banco incompleta no .env")

        self.DATABASE_URL = (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

        self.SECRET_KEY = os.getenv("SECRET_KEY")
        if not self.SECRET_KEY:
            raise RuntimeError("SECRET_KEY não definida")

        self.ALGORITHM = "HS256"

        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
        )

        self.CORS_ORIGINS = os.getenv("CORS_ORIGINS", "")
        self.CORS_ORIGINS = (
            [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
            if self.CORS_ORIGINS
            else []
        )

settings = Settings()
