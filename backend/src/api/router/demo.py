import logging

from fastapi import APIRouter, Depends, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.component.template import get_template
from api.service.popular_service import PopularService
from api.service.item_meta_service import ItemMetaService
from api.service.random_input_service import RandomInputService
from api.service.random_walk_service import RandomWalkService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/popular_item", response_class=HTMLResponse, name="get_popular_item")
def get_popular_item(
    request: Request,
    genre: str = Query(""),
    is_random: bool = Query(False),
    template: Jinja2Templates = Depends(get_template),
    random_input_service: RandomInputService = Depends(),
    popular_service: PopularService = Depends(),
):
    context = {"request": request}

    if is_random is True:
        genre = random_input_service.get_random_genre_name()

    most_viewed_items = popular_service.get_most_viewed_movies(genre, 10)
    high_rated_items = popular_service.get_high_rated_movies(genre, 10)

    context["genre"] = genre
    context["most_viewed_items"] = [item.to_dict() for item in most_viewed_items]
    context["high_rated_items"] = [item.to_dict() for item in high_rated_items]

    return template.TemplateResponse("popular_item.html", context)


@router.get("/related_item", response_class=HTMLResponse, name="get_related_item")
async def get_related_item(
    request: Request,
    item_id: str = Query(""),
    is_random: bool = Query(False),
    template: Jinja2Templates = Depends(get_template),
    random_input_service: RandomInputService = Depends(),
    random_walk_service: RandomWalkService = Depends(),
    item_meta_service: ItemMetaService = Depends(),
):
    context = {"request": request}

    if is_random is True:
        item_id = random_input_service.get_random_movie_id()

    if item_id is None or item_id == "":
        return template.TemplateResponse("related_item.html", context)

    seed_item = item_meta_service.get_item_meta(int(item_id))

    if seed_item is None:
        return template.TemplateResponse("related_item.html", context)

    rec_items = random_walk_service.inference([int(item_id)], 10)

    context["item_id"] = item_id
    context["seed_item"] = seed_item.to_dict()
    context["rec_items"] = [item.to_dict() for item in rec_items]

    return template.TemplateResponse("related_item.html", context)


@router.get("/personalized_item", response_class=HTMLResponse, name="get_personalized_item")
def get_personalized_item(
    request: Request,
    user_id: str = Query(""),
    is_random: bool = Query(False),
    template: Jinja2Templates = Depends(get_template),
    random_input_service: RandomInputService = Depends(),
    random_walk_service: RandomWalkService = Depends(),
    item_meta_service: ItemMetaService = Depends(),
):
    context = {"request": request}

    if is_random is True:
        user_id = random_input_service.get_random_user_id()

    if user_id is None or user_id == "":
        return template.TemplateResponse("personalized_item.html", context)

    queries = random_walk_service.get_sample_items_from_user(int(user_id))
    seed_items = item_meta_service.get_item_metas(queries)

    if len(seed_items) == 0:
        return template.TemplateResponse("personalized_item.html", context)

    rec_items = random_walk_service.inference(queries, 10)

    context["user_id"] = user_id
    context["seed_items"] = [item.to_dict() for item in seed_items]
    context["rec_items"] = [item.to_dict() for item in rec_items]

    return template.TemplateResponse("personalized_item.html", context)
