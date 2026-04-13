from pydantic import BaseModel, EmailStr

class CadastroRequest(BaseModel):
    email: EmailStr
    senha: str
    nome: str
    aceito_termos: bool
    aceito_privacidade: bool
    captcha: str


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str
    captcha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
