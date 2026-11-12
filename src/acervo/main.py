from fastapi import FastAPI

from acervo.api.controllers.livros_controller import criar_livros_router
from acervo.repositories.livro_repository import LivroRepository
from acervo.services.livro_service import LivroService


def criar_app() -> FastAPI:
    repository = LivroRepository()
    service = LivroService(repository)
    app = FastAPI(
        title="Acervo de Livros",
        summary="API para consultar e gerenciar um acervo de livros.",
        description=(
            "Cadastre, pesquise, atualize e remova livros. "
            "Os dados são mantidos em memória e reiniciados ao reiniciar a aplicação."
        ),
        version="1.1.0",
    )
    app.include_router(criar_livros_router(service))

    @app.get("/health", tags=["Sistema"], summary="Verificar saúde da API")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = criar_app()
