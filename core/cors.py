from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from core.config import settings

class CORSConfig:
    @staticmethod
    def setup(app: FastAPI):
        if not settings.CORS_ORIGINS:
            return

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
