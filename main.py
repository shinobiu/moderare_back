from fastapi import FastAPI
from core.cors import CORSConfig
from api.Auth import router as auth_router
from core.logging import LoggingConfig
from middlewares.logging import RequestLoggingMiddleware
from api.Pessoa import router as pessoa_router

LoggingConfig.setup()


app = FastAPI(title="Vicio API")
app.middleware("http")(RequestLoggingMiddleware())

CORSConfig.setup(app)

app.include_router(auth_router)
app.include_router(pessoa_router)
