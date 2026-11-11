from acervo.domain.livro import Livro
from acervo.repositories.livro_repository import LivroRepository


class LivroJaCadastradoError(Exception):
    """Indica que já existe um livro com o mesmo identificador."""


class LivroService:
    def __init__(self, repository: LivroRepository) -> None:
        self._repository = repository

    def cadastrar(self, livro: Livro) -> Livro:
        if self._repository.existe(livro.id):
            raise LivroJaCadastradoError(f"Já existe um livro com id {livro.id}.")
        return self._repository.adicionar(livro)

    def listar(self) -> list[Livro]:
        return self._repository.buscar_todos()
