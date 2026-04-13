from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class TipoMensagem(str, Enum):
    CHECKIN = "CHECKIN"
    META = "META"
    ALERTA = "ALERTA"


class IAUsageResponse(BaseModel):
    pessoa_id: UUID
    tipo: TipoMensagem
    ultimo_uso: datetime

    class Config:
        from_attributes = True