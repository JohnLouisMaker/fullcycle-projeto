from acervo.domain.livro import Livro


class LivroRepository:
    """Repository em memória para acesso ao acervo de livros."""

    def __init__(self) -> None:
        self._livros: dict[int, Livro] = {}

    def adicionar(self, livro: Livro) -> Livro:
        self._livros[livro.id] = livro
        return livro

    def buscar_todos(self) -> list[Livro]:
        return list(self._livros.values())

    def existe(self, livro_id: int) -> bool:
        return livro_id in self._livros
