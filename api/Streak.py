from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from core.auth_dependency import get_current_user_id

from schemas.Resaponse import ApiResponse
from services.StreakService import StreakService
from schemas.Streak import CheckinRequest


router = APIRouter(
    prefix="/streak",
    tags=["Streak"]
)


@router.get("/me")
def obter_meu_streak(
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result = StreakService(db).obter_status(pessoa_id)

    return {
        "success": True,
        "data": result
    }


@router.post("/checkin")
def checkin(
    payload: CheckinRequest,
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result = StreakService(db).checkin(pessoa_id, payload.humor)

    return {
        "success": True,
        "data": result
    }
    
@router.post("/reset")
def resetar_streak(
    payload: CheckinRequest,
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)):
    service = StreakService(db)
    result = service.reset(pessoa_id, payload.humor)
    return {
        "success": True,
        "data": result
    }