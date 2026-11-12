from typing import Literal

from fastapi import APIRouter, HTTPException, Path, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field

from acervo.domain.livro import Livro
from acervo.services.livro_service import (
    LivroJaCadastradoError,
    LivroNaoEncontradoError,
    LivroService,
)


class LivroRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: int = Field(gt=0)
    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=160)
    categoria: str = Field(min_length=1, max_length=80)
    ano_publicacao: int = Field(ge=1000, le=9999)
    status: Literal["disponível", "emprestado"]


class LivroAtualizacaoRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=160)
    categoria: str = Field(min_length=1, max_length=80)
    ano_publicacao: int = Field(ge=1000, le=9999)
    status: Literal["disponível", "emprestado"]


class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    categoria: str
    ano_publicacao: int
    status: Literal["disponível", "emprestado"]


def criar_livros_router(service: LivroService) -> APIRouter:
    router = APIRouter(prefix="/livros", tags=["Livros"])

    def erro_nao_encontrado(erro: Exception) -> HTTPException:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro))

    @router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
    def cadastrar_livro(dados: LivroRequest) -> Livro:
        livro = Livro(
            id=dados.id,
            titulo=dados.titulo,
            autor=dados.autor,
            categoria=dados.categoria,
            ano_publicacao=dados.ano_publicacao,
            status=dados.status,
        )
        try:
            return service.cadastrar(livro)
        except LivroJaCadastradoError as erro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(erro),
            ) from erro

    @router.get("", response_model=list[LivroResponse], summary="Listar livros")
    def listar_livros(
        busca: str | None = Query(default=None, min_length=1, max_length=120),
        categoria: str | None = Query(default=None, min_length=1, max_length=80),
        status_livro: Literal["disponível", "emprestado"] | None = Query(default=None, alias="status"),
        ano_publicacao: int | None = Query(default=None, ge=1000, le=9999),
        limite: int = Query(default=20, ge=1, le=100),
        deslocamento: int = Query(default=0, ge=0),
    ) -> list[Livro]:
        return service.listar(
            busca=busca,
            categoria=categoria,
            status=status_livro,
            ano_publicacao=ano_publicacao,
            limite=limite,
            deslocamento=deslocamento,
        )

    @router.get("/{livro_id}", response_model=LivroResponse, summary="Buscar livro")
    def buscar_livro(livro_id: int = Path(gt=0)) -> Livro:
        try:
            return service.buscar_por_id(livro_id)
        except LivroNaoEncontradoError as erro:
            raise erro_nao_encontrado(erro) from erro

    @router.put("/{livro_id}", response_model=LivroResponse, summary="Atualizar livro")
    def atualizar_livro(
        dados: LivroAtualizacaoRequest,
        livro_id: int = Path(gt=0),
    ) -> Livro:
        livro = Livro(id=livro_id, **dados.model_dump())
        try:
            return service.atualizar(livro_id, livro)
        except LivroNaoEncontradoError as erro:
            raise erro_nao_encontrado(erro) from erro

    @router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover livro")
    def remover_livro(livro_id: int = Path(gt=0)) -> Response:
        try:
            service.remover(livro_id)
        except LivroNaoEncontradoError as erro:
            raise erro_nao_encontrado(erro) from erro
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
