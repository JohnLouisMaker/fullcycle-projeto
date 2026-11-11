from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from acervo.domain.livro import Livro
from acervo.services.livro_service import LivroJaCadastradoError, LivroService


class LivroRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: int = Field(gt=0)
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)


class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: str


def criar_livros_router(service: LivroService) -> APIRouter:
    router = APIRouter(prefix="/livros", tags=["Livros"])

    @router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
    def cadastrar_livro(dados: LivroRequest) -> Livro:
        livro = Livro(id=dados.id, titulo=dados.titulo, autor=dados.autor)
        try:
            return service.cadastrar(livro)
        except LivroJaCadastradoError as erro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(erro),
            ) from erro

    @router.get("", response_model=list[LivroResponse])
    def listar_livros() -> list[Livro]:
        return service.listar()

    return router
