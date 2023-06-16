import logging
from typing import List

from fastapi import APIRouter, Depends, Query

from api.model.dto import Movie
from api.service.bestseller_service import BestsellerService
from api.service.random_walk_service import RandomWalkService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/movie/bestseller", response_model=List[Movie])
async def get_bestseller_item(
    genre: str = Query(""),
    size: int = Query(10),
    bestseller_service: BestsellerService = Depends(),
) -> List[Movie]:
    return bestseller_service.get_high_rated_movies(genre, size)


@router.get("/movie/{item_id}", response_model=List[Movie])
async def get_related_item(
    item_id: str = Query(...),
    size: int = Query(10),
    random_walk_service: RandomWalkService = Depends(),
) -> List[Movie]:
    return random_walk_service.inference([item_id], size)


@router.get("/movie/{user_id}", response_model=List[Movie])
async def get_personalized_item(
    user_id: str = Query(...),
    size: int = Query(10),
    random_walk_service: RandomWalkService = Depends(),
) -> List[Movie]:
    queries = random_walk_service.get_sample_items_from_user(user_id)
    return random_walk_service.inference(queries, size)
