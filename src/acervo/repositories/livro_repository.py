from acervo.domain.livro import Livro


class LivroRepository:
    def __init__(self) -> None:
        livros_iniciais = [
            Livro(
                id=1,
                titulo="O Hobbit",
                autor="J. R. R. Tolkien",
                categoria="Fantasia",
                ano_publicacao=1937,
                status="disponível",
            ),
            Livro(
                id=2,
                titulo="1984",
                autor="George Orwell",
                categoria="Ficção distópica",
                ano_publicacao=1949,
                status="emprestado",
            ),
            Livro(
                id=3,
                titulo="Dom Casmurro",
                autor="Machado de Assis",
                categoria="Romance",
                ano_publicacao=1899,
                status="disponível",
            ),
        ]
        self._livros: dict[int, Livro] = {livro.id: livro for livro in livros_iniciais}

    def adicionar(self, livro: Livro) -> Livro:
        self._livros[livro.id] = livro
        return livro

    def buscar_todos(self) -> list[Livro]:
        return list(self._livros.values())

    def buscar_por_id(self, livro_id: int) -> Livro | None:
        return self._livros.get(livro_id)

    def atualizar(self, livro: Livro) -> Livro:
        self._livros[livro.id] = livro
        return livro

    def remover(self, livro_id: int) -> bool:
        return self._livros.pop(livro_id, None) is not None

    def existe(self, livro_id: int) -> bool:
        return livro_id in self._livros
