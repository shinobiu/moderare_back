from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.Pessoa import PessoaUpdateRequest, PessoaResponse
from services.PessoaService import PessoaService
from database.session import get_db
from core.auth_dependency import get_current_user_id

router = APIRouter(
    prefix="/pessoa",
    tags=["Pessoa"]
)


@router.patch("/me")
def atualizar_meus_dados(
    payload: PessoaUpdateRequest,
    pessoa_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        PessoaService(db).atualizar_dados(
            pessoa_id=pessoa_id,
            **payload.dict()
        )
        return {"msg": "Dados atualizados com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=PessoaResponse)
def read_me(
    pessoa_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        pessoa = PessoaService(db).obter_por_id(pessoa_id)
        return pessoa
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))