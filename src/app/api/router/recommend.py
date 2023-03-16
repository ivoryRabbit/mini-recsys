import logging
from typing import List

from fastapi import APIRouter, Depends, Query

from app.api.model.dto import Movie
from app.api.service.item_service import ItemService
from app.api.service.random_walk_service import RandomWalkService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/movie/{item_id}", response_model=List[Movie])
async def get_related_item(
    item_id: str = Query(...),
    size: int = Query(10),
    random_walk_service: RandomWalkService = Depends(),
    item_service: ItemService = Depends(),
) -> List[Movie]:
    item_ids = random_walk_service.inference([item_id], size)
    rec_items = item_service.get_item_metas(item_ids)
    return rec_items


@router.get("/movie/{user_id}", response_model=List[Movie])
async def get_personalized_item(
    user_id: str = Query(...),
    size: int = Query(10),
    random_walk_service: RandomWalkService = Depends(),
    item_service: ItemService = Depends(),
) -> List[Movie]:
    queries = random_walk_service.get_sample_items_from_user(user_id)
    item_ids = random_walk_service.inference(queries, size)
    rec_items = item_service.get_item_metas(item_ids)
    return rec_items
