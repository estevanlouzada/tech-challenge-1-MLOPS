from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# Modelo para o Livro (Baseado nos requisitos de extração [2])
class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    availability: str
    category: str
    image: HttpUrl

# Modelo para Estatísticas (Requisito de Insights [3, 4])
class StatsOverview(BaseModel):
    total_books: int
    average_price: float
    rating_distribution: dict

# Modelo para Autenticação (Desafio 1 [4])
class Token(BaseModel):
    access_token: str
    token_type: str