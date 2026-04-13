from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth_dependency import get_current_user_id

from services.MetaStreakService import MetaStreakService
from schemas.MetaStreak import (
    MetaStreakCreateRequest,
    MetaStreakCreateResponse,
    MetaStreakStatusResponse
)

router = APIRouter(
    prefix="/meta",
    tags=["Meta"]
)


# =========================
# CRIAR META
# =========================
@router.post(
    "/criar",
    response_model=MetaStreakCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_meta(
    data: MetaStreakCreateRequest,
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        meta = MetaStreakService(db).criar_meta(
            pessoa_id=pessoa_id,
            meta_dias=data.meta_dias,
            habito_id=data.habito_id,
            descricao_custom=data.descricao_custom
        )

        return meta

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# META ATIVA
# =========================
@router.get(
    "/ativa"
)
def get_meta_ativa(
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        meta = MetaStreakService(db).obter_meta_ativa(pessoa_id)

        if not meta:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma meta ativa"
            )

        return meta

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.delete(
    "/ativa"
)
def cancela(
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        meta = MetaStreakService(db).cancelar_meta(pessoa_id)

        if not meta:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma meta ativa"
            )

        return meta

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/habitos")
def get_habitos(pessoa_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    service = MetaStreakService(db)
    return service.listar_habitos()