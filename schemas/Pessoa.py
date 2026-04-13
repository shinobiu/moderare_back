from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class PessoaUpdateRequest(BaseModel):
    nome: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    senha_atual: Optional[str] = None
    nova_senha: Optional[str] = None


class PessoaResponse(BaseModel):
    id: UUID
    e_mail: str
    nome: str
    ativo: bool
    email_verificado: bool
    criado_em: datetime
    atualizado_em: datetime
    aceito_termos: bool
    aceito_privacidade: bool

    class Config:
        from_attributes = True