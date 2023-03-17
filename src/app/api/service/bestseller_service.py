import logging
from typing import List

from fastapi import Depends

from app.api.model.dto import Movie
from app.api.repository.bestseller_repository import BestsellerRepository
from app.api.repository.item_repository import ItemRepository

logger = logging.getLogger(__name__)


class BestsellerService:
    def __init__(
        self,
        bestseller_repository: BestsellerRepository = Depends(),
        item_repository: ItemRepository = Depends(),
    ):
        self._bestseller_repository = bestseller_repository
        self._item_repository = item_repository

    def get_popular_movies(self, genre: str, top_k: int = 10) -> List[Movie]:
        item_ids, populars = self._bestseller_repository.get_bestseller_by_popular(genre, top_k)
        movies = self._item_repository.get_movie_metas(item_ids)

        for movie, popular in zip(movies, populars):
            movie.popular = popular

        return movies

    def get_high_rated_movies(self, genre: str, top_k: int = 10) -> List[Movie]:
        item_ids, ratings = self._bestseller_repository.get_bestseller_by_rating(genre, top_k)
        movies = self._item_repository.get_movie_metas(item_ids)

        for movie, rating in zip(movies, ratings):
            movie.rating = rating

        return movies
