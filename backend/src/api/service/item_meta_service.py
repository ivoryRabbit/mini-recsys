import logging
from typing import Optional, List

from fastapi import Depends

from api.model.genre_dto import GenreDTO
from api.model.movie_dto import MovieDTO
from api.repository.genre_repository import GenreRepository
from api.repository.movie_repository import MovieRepository

logger = logging.getLogger(__name__)


class ItemMetaService:
    def __init__(
        self,
        movie_repository: MovieRepository = Depends(),
        genre_repository: GenreRepository = Depends(),
    ):
        self._movie_repository = movie_repository
        self._genre_repository = genre_repository

    def get_item_meta(self, item_id: int) -> Optional[MovieDTO]:
        return self._movie_repository.find_movie_by_id(item_id)

    def get_item_metas(self, item_ids: List[int]) -> List[MovieDTO]:
        return self._movie_repository.find_movies_by_ids(item_ids)

    def get_all_genres(self) -> List[GenreDTO]:
        return self._genre_repository.find_all_genre()
