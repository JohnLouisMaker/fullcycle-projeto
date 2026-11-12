from dataclasses import replace
from typing import Literal

from acervo.domain.livro import Livro
from acervo.repositories.livro_repository import LivroRepository


class LivroJaCadastradoError(Exception):
    """Indica que já existe um livro com o mesmo identificador."""


class LivroNaoEncontradoError(Exception):
    """Indica que o identificador solicitado não existe no acervo."""


class LivroService:
    def __init__(self, repository: LivroRepository) -> None:
        self._repository = repository

    def cadastrar(self, livro: Livro) -> Livro:
        if self._repository.existe(livro.id):
            raise LivroJaCadastradoError(f"Já existe um livro com id {livro.id}.")
        return self._repository.adicionar(livro)

    def listar(
        self,
        *,
        busca: str | None = None,
        categoria: str | None = None,
        status: Literal["disponível", "emprestado"] | None = None,
        ano_publicacao: int | None = None,
        limite: int = 20,
        deslocamento: int = 0,
    ) -> list[Livro]:
        livros = self._repository.buscar_todos()

        if busca:
            termo = busca.casefold()
            livros = [
                livro
                for livro in livros
                if termo in livro.titulo.casefold()
                or termo in livro.autor.casefold()
                or termo in livro.categoria.casefold()
            ]
        if categoria:
            categoria_normalizada = categoria.casefold()
            livros = [livro for livro in livros if livro.categoria.casefold() == categoria_normalizada]
        if status:
            livros = [livro for livro in livros if livro.status == status]
        if ano_publicacao:
            livros = [livro for livro in livros if livro.ano_publicacao == ano_publicacao]

        livros.sort(key=lambda livro: livro.id)
        return livros[deslocamento : deslocamento + limite]

    def buscar_por_id(self, livro_id: int) -> Livro:
        livro = self._repository.buscar_por_id(livro_id)
        if livro is None:
            raise LivroNaoEncontradoError(f"Livro com id {livro_id} não encontrado.")
        return livro

    def atualizar(self, livro_id: int, dados: Livro) -> Livro:
        self.buscar_por_id(livro_id)
        livro_atualizado = replace(dados, id=livro_id)
        return self._repository.atualizar(livro_atualizado)

    def remover(self, livro_id: int) -> None:
        self.buscar_por_id(livro_id)
        self._repository.remover(livro_id)
