import logging
from typing import Optional, List

from fastapi import Depends

from api.model.dto import Movie
from api.repository.item_repository import ItemRepository

logger = logging.getLogger(__name__)


class ItemMetaService:
    def __init__(self, repository: ItemRepository = Depends()):
        self._repository = repository

    def get_item_meta(self, item_id: str) -> Optional[Movie]:
        return self._repository.get_movie_meta(item_id)

    def get_item_metas(self, item_ids: List[str]) -> List[Movie]:
        return self._repository.get_movie_metas(item_ids)
