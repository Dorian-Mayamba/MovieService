from fastapi import APIRouter, Depends
import pandas as pd
import os
import requests
from sqlalchemy.orm import Session
from typing import List
import schemas
from models.models import Genre, Movie
from database import engine, get_db

router = APIRouter(
    prefix='/movies',
    tags=['Movies']
)


@router.get('', response_model=List[schemas.MovieSchema])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if len(movies) > 0:
        ##
        return movies
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=true&language=en-US&page=1" \
          "&sort_by=popularity.desc"

    token = os.getenv('MOVIE_DB_TOKEN')
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    columns = ['id', 'title', 'overview', 'poster_path', 'original_title', 'original_language', 'release_date',
               'genre_ids']
    results = data['results']
    df = pd.DataFrame(results, columns=columns)
    for index, row in df.iterrows():
        new_movie = Movie(title=row['title'], overview=row['overview'],
                          poster_path=row['poster_path'],
                          original_title=row['original_title'],
                          original_language=row['original_language'],
                          release_date=row['release_date'])
        for genre_id in row['genre_ids']:
            genre = db.query(Genre).filter(Genre.id == genre_id).first()
            if genre is not None:
                new_movie.genres.append(genre)
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
    movies = db.query(Movie).all()
    return movies


@router.get("/genres", response_model=List[schemas.GenreSchema])
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(Genre).all()
    if len(genres) > 0:
        return genres
    token = os.getenv('MOVIE_DB_TOKEN')
    url = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    columns = ['id', 'name']
    df = pd.DataFrame(data['genres'], columns=columns)

    df.to_sql(Genre.__tablename__, engine, if_exists='append', index=False)
    genres = db.query(Genre).all()
    return genres
