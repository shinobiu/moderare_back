from fastapi import Cookie, Request, HTTPException
from core.security import JWTService

def get_current_user_id(access_token: str | None = Cookie(default=None)) -> str:

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Não autenticado"
        )

    try:
        user_id = JWTService().verify(access_token)
        return user_id

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )