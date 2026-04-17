from datetime import date
from uuid import UUID
from pydantic import BaseModel


class StreakResponse(BaseModel):
    id: UUID
    pessoa_id: UUID
    mensagem: str | None
    dias: int
    data_inicio: date
    ultimo_checkin: date | None

    class Config:
        from_attributes = True
        
class CheckinRequest(BaseModel):
    humor: str | None