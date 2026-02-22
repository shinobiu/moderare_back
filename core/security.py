from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.config import settings

class PasswordService:
    def __init__(self):
        self._context = CryptContext(
            schemes=["argon2"],
            deprecated="auto"
        )

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return self._context.verify(plain, hashed)


class JWTService:
    def create(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": subject,
            "exp": expire
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise ValueError("Token inválido")
