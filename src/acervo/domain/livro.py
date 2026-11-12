from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Livro:
    id: int
    titulo: str
    autor: str
    categoria: str
    ano_publicacao: int
    status: Literal["disponível", "emprestado"]
