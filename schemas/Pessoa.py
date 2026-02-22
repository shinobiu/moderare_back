from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class PessoaUpdateRequest(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    senha_atual: Optional[str] = None
    nova_senha: Optional[str] = None


class PessoaResponse(BaseModel):
    id: UUID
    e_mail: str
    nome: str
    cpf: Optional[str]
    ativo: bool
    email_verificado: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True