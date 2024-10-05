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
    reviews = relationship("Review", back_populates='movie')
    likes = relationship("Like", back_populates='movie')
    watches = relationship("Watch", back_populates='movie')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  ## comes from userAuthService kafka event
    created_at = Column(TIMESTAMP, default=date.today())
    movie = relationship("Movie", back_populates='likes')


class Watch(Base):
    __tablename__ = 'watches'

    id = Column(Integer, primary_key=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  ## comes from userAuthService kafka event
    created_at = Column(TIMESTAMP, default=date.today())
    movie = relationship("Movie", back_populates='watches')


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    user_id = Column(Integer, nullable=False)  ## comes from userAuthService kafka event
    username = Column(String, nullable=False)  ## Comes from the userAuthService kafka event
    content = Column(Text)
    rating = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=date.today())
    updated_at = Column(TIMESTAMP, default=date.today())
    movie = relationship("Movie", back_populates='reviews')
