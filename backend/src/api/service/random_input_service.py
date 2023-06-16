import logging
from typing import Optional

from fastapi import Depends

from api.repository.genre_repository import GenreRepository
from api.repository.item_repository import ItemRepository
from api.repository.user_repository import UserRepository

logger = logging.getLogger(__name__)


class RandomInputService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        item_repository: ItemRepository = Depends(),
        genre_repository: GenreRepository = Depends(),
    ):
        self._user_repository = user_repository
        self._item_repository = item_repository
        self._genre_repository = genre_repository

    def get_random_user_id(self) -> Optional[str]:
        return self._user_repository.get_random_user_id()

    def get_random_item_id(self) -> Optional[str]:
        return self._item_repository.get_random_item_id()

    def get_random_genre(self) -> Optional[str]:
        return self._genre_repository.get_random_genre()
