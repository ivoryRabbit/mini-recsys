import logging

from fastapi import APIRouter, Depends, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.component.template import get_template
from app.api.service.bestseller_service import BestsellerService
from app.api.service.item_meta_service import ItemMetaService
from app.api.service.random_input_service import RandomInputService
from app.api.service.random_walk_service import RandomWalkService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/bestseller_item", response_class=HTMLResponse, name="get_bestseller_item")
async def get_bestseller_item(
    request: Request,
    genre: str = Query(""),
    is_random: bool = Query(False),
    template: Jinja2Templates = Depends(get_template),
    random_input_service: RandomInputService = Depends(),
    bestseller_service: BestsellerService = Depends(),
):
    context = {"request": request}

    if is_random is True:
        genre = random_input_service.get_random_genre()

    popular_items = bestseller_service.get_popular_movies(genre, 10)
    high_rated_items = bestseller_service.get_high_rated_movies(genre, 10)

    context["genre"] = genre
    context["popular_items"] = [item.as_dict() for item in popular_items]
    context["high_rated_items"] = [item.as_dict() for item in high_rated_items]

    return template.TemplateResponse("bestseller_item.html", context)


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
        item_id = random_input_service.get_random_item_id()

    if item_id == "":
        return template.TemplateResponse("related_item.html", context)

    seed_item = item_meta_service.get_item_meta(item_id)

    if seed_item is None:
        return template.TemplateResponse("related_item.html", context)

    rec_items = random_walk_service.inference([item_id], 10)

    context["item_id"] = item_id
    context["seed_item"] = seed_item.as_dict()
    context["rec_items"] = [item.as_dict() for item in rec_items]

    return template.TemplateResponse("related_item.html", context)


@router.get("/personalized_item", response_class=HTMLResponse, name="get_personalized_item")
async def get_personalized_item(
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

    if user_id == "":
        return template.TemplateResponse("personalized_item.html", context)

    queries = random_walk_service.get_sample_items_from_user(user_id)
    seed_items = item_meta_service.get_item_metas(queries)

    if len(seed_items) == 0:
        return template.TemplateResponse("personalized_item.html", context)

    rec_items = random_walk_service.inference(queries, 10)

    context["user_id"] = user_id
    context["seed_items"] = [item.as_dict() for item in seed_items]
    context["rec_items"] = [item.as_dict() for item in rec_items]

    return template.TemplateResponse("personalized_item.html", context)
