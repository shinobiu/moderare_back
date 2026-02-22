from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings


class DatabaseSession:
    def __init__(self):
        self.engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True
        )

        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Session:
        db = self._session_factory()
        try:
            yield db
        finally:
            db.close()


# instância única
database = DatabaseSession()

# dependência para o FastAPI
def get_db() -> Session:
    yield from database.get_session()
