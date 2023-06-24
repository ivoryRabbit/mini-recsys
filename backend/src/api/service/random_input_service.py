import logging
from typing import Optional

from fastapi import Depends

from api.repository.genre_repository import GenreRepository
from api.repository.movie_repository import MovieRepository
from api.repository.user_repository import UserRepository

logger = logging.getLogger(__name__)


class RandomInputService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        movie_repository: MovieRepository = Depends(),
        genre_repository: GenreRepository = Depends(),
    ):
        self._user_repository = user_repository
        self._movie_repository = movie_repository
        self._genre_repository = genre_repository

    def get_random_user_id(self) -> int:
        return self._user_repository.find_user_by_random().id

    def get_random_movie_id(self) -> int:
        return self._movie_repository.find_movie_by_random().id

    def get_random_genre_name(self) -> str:
        return self._genre_repository.find_genre_by_random().name
