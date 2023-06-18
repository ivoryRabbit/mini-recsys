import logging
from typing import List

from fastapi import APIRouter, Depends, Query

from api.model.movie_dto import MovieDTO
from api.service.popular_service import PopularService
from api.service.random_walk_service import RandomWalkService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/movie/popular", response_model=List[MovieDTO])
async def get_popular_item(
    genre: str = Query(""),
    size: int = Query(10),
    popular_service: PopularService = Depends(),
) -> List[MovieDTO]:
    return popular_service.get_high_rated_movies(genre, size)


@router.get("/movie/related", response_model=List[MovieDTO])
async def get_related_item(
    item_id: int = Query(...),
    size: int = Query(10),
    random_walk_service: RandomWalkService = Depends(),
) -> List[MovieDTO]:
    return random_walk_service.inference([item_id], size)


@router.get("/movie/personalized", response_model=List[MovieDTO])
async def get_personalized_item(
    user_id: int = Query(...),
    size: int = Query(10),
    random_walk_service: RandomWalkService = Depends(),
) -> List[MovieDTO]:
    queries = random_walk_service.get_sample_items_from_user(user_id)
    return random_walk_service.inference(queries, size)
