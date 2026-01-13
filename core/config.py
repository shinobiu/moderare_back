import os

class Settings:
    ENV = os.getenv("ENV", "development")

    CORS_ORIGINS = (
        os.getenv("CORS_ORIGINS", "")
        .split(",")
        if os.getenv("CORS_ORIGINS")
        else []
    )

settings = Settings()
