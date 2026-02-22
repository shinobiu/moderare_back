from fastapi import APIRouter, Depends, HTTPException, Response
from models.Pessoa import Pessoa
from services.email_confirm_service import EmailConfirmService
from services.email_service import EmailService
from sqlalchemy.orm import Session
from database.session import get_db
from services.PessoaService import PessoaService
from schemas.Auth import CadastroRequest, LoginRequest, TokenResponse
from core.auth_dependency import get_current_user_id

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register(
    payload: CadastroRequest,
    db: Session = Depends(get_db)
):
    try:
        PessoaService(db).cadastrar(
            email=payload.email,
            senha=payload.senha,
            nome=payload.nome,
            aceito_termos=payload.aceito_termos,
            aceito_privacidade=payload.aceito_privacidade
        )

        return {"msg": "Usuário criado com sucesso"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        token = PessoaService(db).autenticar(
            payload.email,
            payload.senha
        )

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,        # True em produção (HTTPS)
            samesite="lax",     # se front e back estiverem no mesmo domínio
            max_age=60 * 60 * 24
        )

        return {"message": "Login realizado com sucesso"}

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/confirmar-email")
def confirm_email(token: str, db: Session = Depends(get_db)):
    service = EmailConfirmService(db)
    service.confirmar_email(token)

    return {
        "message": "E-mail confirmado com sucesso"
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        value="",
        max_age=0,
        expires=0,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {"message": "Logout realizado com sucesso"}

@router.post("/envia-email")
def send_confirm_email(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    pessoa = db.query(Pessoa).filter(Pessoa.id == user_id).first()

    if not pessoa:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if pessoa.email_verificado:
        return {
            "message": "E-mail já confirmado."
        }

    confirm_service = EmailConfirmService(db)
    email_service = EmailService()

    token = confirm_service.gerar_token_confirmacao(pessoa)
    email_service.enviar_confirmacao(pessoa.e_mail, token)

    return {
        "message": "E-mail de confirmação enviado com sucesso."
    }