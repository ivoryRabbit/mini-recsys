import logging
from typing import List, Optional

from fastapi import Depends

from app.api.component.database import get_connection
from app.api.model.dto import Movie
from app.api.repository.item_repository import ItemRepository

logger = logging.getLogger(__name__)


class ItemService:
    def __init__(self, connection=Depends(get_connection)):
        self._repository = ItemRepository(connection)

    def get_item_meta(self, item_id: str) -> Optional[Movie]:
        return self._repository.get_movie_meta(item_id)

    def get_item_metas(self, item_ids: List[str]) -> List[Movie]:
        return self._repository.get_movie_metas(item_ids)

    def get_random_item_id(self) -> Optional[str]:
        return self._repository.get_random_item_id()
