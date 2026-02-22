from fastapi import Request, HTTPException
from core.security import JWTService

def get_current_user_id(request: Request) -> str:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Não autenticado"
        )

    try:
        user_id = JWTService().verify(token)
        return user_id
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )