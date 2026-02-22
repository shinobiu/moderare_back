from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from core.config import settings


class Database:
    """
    Classe responsável por:
    - Criar a engine do SQLAlchemy
    - Gerenciar o pool de conexões
    - Fornecer sessões para a aplicação
    """

    _engine = None
    _SessionLocal = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                echo=settings.ENV == "development"
            )
        return cls._engine

    @classmethod
    def get_session_factory(cls):
        if cls._SessionLocal is None:
            cls._SessionLocal = sessionmaker(
                bind=cls.get_engine(),
                autocommit=False,
                autoflush=False
            )
        return cls._SessionLocal

    @classmethod
    def get_session(cls) -> Session:
        return cls.get_session_factory()()


class Base(DeclarativeBase):
    """
    Base para todos os models ORM
    """
    pass


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para FastAPI
    Cria e fecha a sessão corretamente por request
    """
    db = Database.get_session()
    try:
        yield db
    finally:
        db.close()
