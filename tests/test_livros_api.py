import pytest
from fastapi.testclient import TestClient

from acervo.main import criar_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(criar_app())


def test_listar_livros_retorna_dados_iniciais(client: TestClient) -> None:
    resposta = client.get("/livros")

    assert resposta.status_code == 200
    assert resposta.json() == [
        {
            "id": 1,
            "titulo": "O Hobbit",
            "autor": "J. R. R. Tolkien",
            "categoria": "Fantasia",
            "ano_publicacao": 1937,
            "status": "disponível",
        },
        {
            "id": 2,
            "titulo": "1984",
            "autor": "George Orwell",
            "categoria": "Ficção distópica",
            "ano_publicacao": 1949,
            "status": "emprestado",
        },
        {
            "id": 3,
            "titulo": "Dom Casmurro",
            "autor": "Machado de Assis",
            "categoria": "Romance",
            "ano_publicacao": 1899,
            "status": "disponível",
        },
    ]


def test_cadastrar_livro_e_listar_acervo(client: TestClient) -> None:
    dados = {
        "id": 4,
        "titulo": "A Sociedade do Anel",
        "autor": "J. R. R. Tolkien",
        "categoria": "Fantasia",
        "ano_publicacao": 1954,
        "status": "disponível",
    }

    resposta_cadastro = client.post("/livros", json=dados)
    resposta_listagem = client.get("/livros")

    assert resposta_cadastro.status_code == 201
    assert resposta_cadastro.json() == dados
    assert resposta_listagem.status_code == 200
    assert resposta_listagem.json()[-1] == dados
    assert len(resposta_listagem.json()) == 4


def test_cadastrar_id_duplicado_retorna_conflito(client: TestClient) -> None:
    dados = {
        "id": 1,
        "titulo": "O Hobbit",
        "autor": "J. R. R. Tolkien",
        "categoria": "Fantasia",
        "ano_publicacao": 1937,
        "status": "disponível",
    }
    client.post("/livros", json=dados)

    resposta = client.post("/livros", json=dados)

    assert resposta.status_code == 409
    assert resposta.json() == {"detail": "Já existe um livro com id 1."}


def test_buscar_livro_por_id_e_retornar_404_quando_nao_existe(client: TestClient) -> None:
    resposta = client.get("/livros/1")
    nao_encontrado = client.get("/livros/999")

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "O Hobbit"
    assert nao_encontrado.status_code == 404
    assert nao_encontrado.json() == {"detail": "Livro com id 999 não encontrado."}


def test_filtrar_e_paginar_livros(client: TestClient) -> None:
    resposta_filtrada = client.get("/livros", params={"status": "disponível"})
    resposta_busca = client.get("/livros", params={"busca": "tolkien"})
    resposta_paginada = client.get("/livros", params={"limite": 1, "deslocamento": 1})

    assert [livro["id"] for livro in resposta_filtrada.json()] == [1, 3]
    assert [livro["id"] for livro in resposta_busca.json()] == [1]
    assert [livro["id"] for livro in resposta_paginada.json()] == [2]


def test_atualizar_livro(client: TestClient) -> None:
    dados = {
        "titulo": "O Hobbit: edição revisada",
        "autor": "J. R. R. Tolkien",
        "categoria": "Fantasia",
        "ano_publicacao": 1937,
        "status": "emprestado",
    }

    resposta = client.put("/livros/1", json=dados)

    assert resposta.status_code == 200
    assert resposta.json() == {"id": 1, **dados}
    assert client.get("/livros/1").json() == {"id": 1, **dados}


def test_atualizar_livro_inexistente_retorna_404(client: TestClient) -> None:
    resposta = client.put(
        "/livros/999",
        json={
            "titulo": "Livro novo",
            "autor": "Autor",
            "categoria": "Drama",
            "ano_publicacao": 2020,
            "status": "disponível",
        },
    )

    assert resposta.status_code == 404


def test_remover_livro(client: TestClient) -> None:
    resposta = client.delete("/livros/2")

    assert resposta.status_code == 204
    assert resposta.content == b""
    assert client.get("/livros/2").status_code == 404


def test_health_check(client: TestClient) -> None:
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


@pytest.mark.parametrize(
    "dados",
    [
        {"id": 0, "titulo": "O Hobbit", "autor": "J. R. R. Tolkien"},
        {"id": 1, "titulo": "  ", "autor": "J. R. R. Tolkien"},
        {"id": 1, "titulo": "O Hobbit", "autor": " "},
        {
            "id": 4,
            "titulo": "Livro válido",
            "autor": "Autor válido",
            "categoria": "Categoria",
            "ano_publicacao": 0,
            "status": "disponível",
        },
        {
            "id": 4,
            "titulo": "Livro válido",
            "autor": "Autor válido",
            "categoria": "Categoria",
            "ano_publicacao": 2020,
            "status": "indisponível",
        },
    ],
)
def test_dados_invalidos_retornam_erro_de_validacao(client: TestClient, dados: dict[str, object]) -> None:
    resposta = client.post("/livros", json=dados)

    assert resposta.status_code == 422
