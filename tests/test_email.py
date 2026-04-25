import pytest
from datetime import datetime, timedelta
from services.email_confirm_service import EmailConfirmService


# =========================
# FAKES
# =========================

class FakePessoa:
    def __init__(self, token, expira_em):
        self.codigo_verificacao = token
        self.codigo_expira_em = expira_em
        self.email_verificado = False
        self.id = 1


class FakeQuery:
    def __init__(self, pessoa):
        self.pessoa = pessoa

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.pessoa


class FakeDB:
    def __init__(self, pessoa):
        self.pessoa = pessoa

    def query(self, *args, **kwargs):
        return FakeQuery(self.pessoa)

    def commit(self):
        pass


# =========================
# TESTES
# =========================

def test_token_invalido():
    db = FakeDB(None)  # simula não encontrado
    service = EmailConfirmService(db)

    with pytest.raises(ValueError) as e:
        service.confirmar_email("token-fake")

    assert "Token inválido" in str(e.value)


def test_token_expirado():
    pessoa = FakePessoa(
        token="abc",
        expira_em=datetime.utcnow() - timedelta(hours=1)  # já expirado
    )

    db = FakeDB(pessoa)
    service = EmailConfirmService(db)

    with pytest.raises(ValueError) as e:
        service.confirmar_email("abc")

    assert "Token expirado" in str(e.value)


def test_confirmacao_sucesso():
    pessoa = FakePessoa(
        token="abc",
        expira_em=datetime.utcnow() + timedelta(hours=1)  # válido
    )

    db = FakeDB(pessoa)
    service = EmailConfirmService(db)

    service.confirmar_email("abc")

    assert pessoa.email_verificado is True
    assert pessoa.codigo_verificacao is None
    assert pessoa.codigo_expira_em is None
