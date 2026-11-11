from fastapi import FastAPI

from acervo.api.controllers.livros_controller import criar_livros_router
from acervo.repositories.livro_repository import LivroRepository
from acervo.services.livro_service import LivroService


def criar_app() -> FastAPI:
    repository = LivroRepository()
    service = LivroService(repository)
    app = FastAPI(title="Acervo de Livros", version="1.0.0")
    app.include_router(criar_livros_router(service))
    return app


app = criar_app()
