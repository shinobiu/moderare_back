from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from core.auth_dependency import get_current_user_id

from schemas.Resaponse import ApiResponse
from services.StreakService import StreakService
from schemas.Streak import StreakResponse


router = APIRouter(
    prefix="/streak",
    tags=["Streak"]
)


@router.get("/me", response_model=ApiResponse[StreakResponse])
def obter_meu_streak(
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result = StreakService(db).obter_status(pessoa_id)

    return {
        "success": True,
        "data": StreakResponse.model_validate(result)
    }


@router.post("/checkin", response_model=ApiResponse[StreakResponse])
def checkin(
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result = StreakService(db).checkin(pessoa_id)

    return {
        "success": True,
        "data": StreakResponse.model_validate(result)
    }
    
@router.post("/reset", response_model=ApiResponse[StreakResponse])
def resetar_streak(pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)):
    service = StreakService(db)
    result = service.reset(pessoa_id)
    return {
        "success": True,
        "data": StreakResponse.model_validate(result)
    }