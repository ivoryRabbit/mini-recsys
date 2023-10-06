import logging
from typing import List

from fastapi import APIRouter, Depends

from api.service.item_meta_service import ItemMetaService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/all", response_model=List[str])
def get_all_genre(
    item_meta_service: ItemMetaService = Depends(),
) -> List[str]:
    genres = item_meta_service.get_all_genres()
    return [genre.name for genre in genres]
