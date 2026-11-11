import pytest
from fastapi.testclient import TestClient

from acervo.main import criar_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(criar_app())


def test_listar_livros_sem_cadastros_retorna_lista_vazia(client: TestClient) -> None:
    resposta = client.get("/livros")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_cadastrar_livro_e_listar_acervo(client: TestClient) -> None:
    dados = {"id": 1, "titulo": "O Hobbit", "autor": "J. R. R. Tolkien"}

    resposta_cadastro = client.post("/livros", json=dados)
    resposta_listagem = client.get("/livros")

    assert resposta_cadastro.status_code == 201
    assert resposta_cadastro.json() == dados
    assert resposta_listagem.status_code == 200
    assert resposta_listagem.json() == [dados]


def test_cadastrar_id_duplicado_retorna_conflito(client: TestClient) -> None:
    dados = {"id": 1, "titulo": "O Hobbit", "autor": "J. R. R. Tolkien"}
    client.post("/livros", json=dados)

    resposta = client.post("/livros", json=dados)

    assert resposta.status_code == 409
    assert resposta.json() == {"detail": "Já existe um livro com id 1."}


@pytest.mark.parametrize(
    "dados",
    [
        {"id": 0, "titulo": "O Hobbit", "autor": "J. R. R. Tolkien"},
        {"id": 1, "titulo": "  ", "autor": "J. R. R. Tolkien"},
        {"id": 1, "titulo": "O Hobbit", "autor": " "},
    ],
)
def test_dados_invalidos_retornam_erro_de_validacao(client: TestClient, dados: dict[str, object]) -> None:
    resposta = client.post("/livros", json=dados)

    assert resposta.status_code == 422
