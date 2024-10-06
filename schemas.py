from datetime import date
from typing import List
from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int
    title: str
    overview: str
    poster_path: str
    original_title: str
    original_language: str
    release_date: date


class GenreBase(BaseModel):
    id: int
    name: str


class GenreSchema(GenreBase):
    movies: List[MovieBase]


class MovieSchema(MovieBase):
    genres: List[GenreBase]

