import logging
from typing import Dict, Optional, Any, List

from fastapi import APIRouter, Depends, Query

from api.model.movie_dto import MovieDTO
from api.service.item_meta_service import ItemMetaService
from api.service.popular_service import PopularService
from api.service.random_input_service import RandomInputService
from api.service.random_walk_service import RandomWalkService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/movie/popular", response_model=Dict[str, List[MovieDTO]])
def get_popular_item(
    genre: str = Query(""),
    size: int = Query(10),
    popular_service: PopularService = Depends(),
) -> Dict[str, List[MovieDTO]]:
    popular_by_view = popular_service.get_most_viewed_movies(genre, size)
    popular_by_rating = popular_service.get_high_rated_movies(genre, size)

    return {"view": popular_by_view, "rating": popular_by_rating}


@router.get("/movie/related", response_model=Dict[str, Any])
def get_related_item(
    item_id: Optional[int] = Query(None),
    size: int = Query(10),
    is_random: bool = Query(False),
    random_input_service: RandomInputService = Depends(),
    random_walk_service: RandomWalkService = Depends(),
    item_meta_service: ItemMetaService = Depends(),
) -> Dict[str, Any]:
    if (item_id is None) ^ (is_random is True):
        raise Exception("user_id should be given or is_random is true")

    if is_random is True:
        item_id = random_input_service.get_random_movie_id()

    seed_items = [item_meta_service.get_item_meta(item_id)]
    rec_items = random_walk_service.inference([item_id], size)

    return {"item_id": item_id, "seed": seed_items, "rec": rec_items}


@router.get("/movie/personalized", response_model=Dict[str, Any])
def get_personalized_item(
    user_id: Optional[int] = Query(None),
    size: int = Query(10),
    is_random: bool = Query(False),
    random_input_service: RandomInputService = Depends(),
    random_walk_service: RandomWalkService = Depends(),
    item_meta_service: ItemMetaService = Depends(),
) -> Dict[str, Any]:
    if (user_id is None) ^ (is_random is True):
        raise Exception("user_id should be given or is_random is true")

    if is_random is True:
        user_id = random_input_service.get_random_user_id()

    queries = random_walk_service.get_sample_items_from_user(user_id)

    seed_items = item_meta_service.get_item_metas(queries)
    rec_items = random_walk_service.inference(queries, size)

    return {"user_id": user_id, "seed": seed_items, "rec": rec_items}
