from database import Base
from sqlalchemy import Column, Integer, String, Text, Date, Table, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import date

movie_genres = Table('movie_genres', Base.metadata,
                     Column('movie_id', ForeignKey('movies.id'), primary_key=True),
                     Column('genre_id', ForeignKey('genres.id'), primary_key=True)
                     )


class Movie(Base):
    __tablename__ = 'movies'

    def __init__(self, title, overview, poster_path, original_title, original_language, release_date):
        self.title = title
        self.overview = overview
        self.poster_path = poster_path,
        self.original_title = original_title
        self.original_language = original_language
        self.release_date = release_date

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    overview = Column(Text, nullable=False)
    poster_path = Column(String, nullable=False)
    original_title = Column(String, nullable=False)
    original_language = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    genres = relationship("Genre", secondary=movie_genres, backref="movies")


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
