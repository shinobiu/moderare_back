from services.PessoaService import PessoaService

class FakeQuery:
    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return None


class FakeDB:
    def query(self, *args, **kwargs):
        return FakeQuery()

    def add(self, obj):
        pass

    def commit(self):
        pass

    def refresh(self, obj):
        pass


def test_cadastro_sem_termos():
    service = PessoaService(FakeDB())

    try:
        service.cadastrar(
            email="teste@teste.com",
            senha="123456",
            nome="Teste",
            aceito_termos=False,
            aceito_privacidade=False
        )
        assert False
    except ValueError as e:
        assert "obrigatório aceitar" in str(e)


def test_cadastro_email_duplicado():
    class FakeQueryDup(FakeQuery):
        def first(self):
            return object()

    class FakeDBDup(FakeDB):
        def query(self, *args, **kwargs):
            return FakeQueryDup()

    service = PessoaService(FakeDBDup())

    try:
        service.cadastrar(
            email="teste@teste.com",
            senha="Senha123!",
            nome="Teste",
            aceito_termos=True,
            aceito_privacidade=True
        )
        assert False
    except ValueError as e:
        assert "Email já cadastrado" in str(e)


def test_cadastro_sucesso():
    service = PessoaService(FakeDB())

    pessoa = service.cadastrar(
        email="teste@teste.com",
        senha="Senha123!",
        nome="Teste",
        aceito_termos=True,
        aceito_privacidade=True
    )

    assert pessoa.e_mail == "teste@teste.com"
    assert pessoa.ativo is True

