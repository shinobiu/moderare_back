from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field


# =========================
# REQUEST (criar meta)
# =========================
class MetaStreakCreateRequest(BaseModel):
    meta_dias: int = Field(..., gt=0)

    habito_id: Optional[UUID] = None
    descricao_custom: Optional[str] = None

    # validação básica (Pydantic v2)
    def model_post_init(self, __context):
        if not self.habito_id and not self.descricao_custom:
            raise ValueError("Informe um hábito ou descrição")

        if self.habito_id and self.descricao_custom:
            raise ValueError("Escolha apenas um: habito_id ou descricao_custom")

        if self.descricao_custom:
            self.descricao_custom = self.descricao_custom.strip()


# =========================
# RESPONSE (criação)
# =========================
class MetaStreakCreateResponse(BaseModel):
    id: UUID
    meta_dias: int
    streak_inicial: int

    habito_id: Optional[UUID] = None
    descricao_custom: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# RESPONSE (status da meta)
# =========================
class MetaStreakStatusResponse(BaseModel):
    meta_dias: int
    progresso: int
    streak_atual: int
    concluida: bool
    porcentagem: float

    # identificação da meta
    habito_nome: Optional[str] = None
    descricao_custom: Optional[str] = None

    # opcional: pronto pro front
    titulo: Optional[str] = None

    class Config:
        from_attributes = True
