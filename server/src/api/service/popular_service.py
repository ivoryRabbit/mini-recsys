import logging
from typing import List

from fastapi import Depends

from api.model.movie_dto import MovieDTO
from api.repository.popular_repository import PopularRepository
from api.repository.movie_repository import MovieRepository

logger = logging.getLogger(__name__)


class PopularService:
    def __init__(
        self,
        popular_repository: PopularRepository = Depends(),
        movie_repository: MovieRepository = Depends(),
    ):
        self._popular_repository = popular_repository
        self._movie_repository = movie_repository

    def get_most_viewed_movies(self, genre: str, top_k: int = 10) -> List[MovieDTO]:
        movie_ids, views = self._popular_repository.find_popular_by_view(genre, top_k)
        movies = self._movie_repository.find_movies_by_ids(movie_ids)

        for movie, view in zip(movies, views):
            movie.view = view

        return movies

    def get_high_rated_movies(self, genre: str, top_k: int = 10) -> List[MovieDTO]:
        movie_ids, ratings = self._popular_repository.find_popular_by_rating(genre, top_k)
        movies = self._movie_repository.find_movies_by_ids(movie_ids)

        for movie, rating in zip(movies, ratings):
            movie.rating = rating

        return movies
