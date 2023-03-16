import logging

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.component.template import get_template

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, template: Jinja2Templates = Depends(get_template)):
    return template.TemplateResponse("index.html", {"request": request})
