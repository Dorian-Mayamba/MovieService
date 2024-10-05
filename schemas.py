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


class ReviewBase(BaseModel):
    id: int
    movie_id: int
    user_id: int
    username: str
    content: str
    rating: float
    created_at: date
    updated_at: date


class LikeBase(BaseModel):
    id: int
    movie_id: int
    user_id: int


class WatchBase(BaseModel):
    id: int
    movie_id: int
    user_id: int


class GenreBase(BaseModel):
    id: int
    name: str


class GenreSchema(GenreBase):
    movies: List[MovieBase]


class MovieSchema(MovieBase):
    genres: List[GenreBase]
    reviews: List[ReviewBase]
    likes: List[LikeBase]
    watches: List[WatchBase]
