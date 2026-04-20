import os

from fastapi import FastAPI
from core.cors import CORSConfig
from api.Auth import router as auth_router
from core.log_config import LoggingConfig
from middlewares.log_middleware import RequestLoggingMiddleware
from api.Pessoa import router as pessoa_router
from api.Streak import router as streak_router
from api.MetaStreak import router as meta_router


LoggingConfig.setup()

ENV = os.getenv("ENVIRONMENT", "dev")

app = FastAPI(
    title="Moderare API", 
    docs_url=None if ENV == "prod" else "/docs",
    redoc_url=None if ENV == "prod" else "/redoc",
    openapi_url=None if ENV == "prod" else "/openapi.json",
    )

@app.get("/health")
def health():
    return {"status": "ok"}

app.middleware("http")(RequestLoggingMiddleware())

CORSConfig.setup(app)

app.include_router(auth_router)
app.include_router(pessoa_router)
app.include_router(streak_router)
app.include_router(meta_router)
