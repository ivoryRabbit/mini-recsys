import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ping")
@router.get("/health")
def health_check(request: Request) -> JSONResponse:
    if hasattr(request.app.state, "graph") is False:
        logger.error("Graph is not yet built")
        raise HTTPException(status_code=400)

    return JSONResponse(content={"ok": "ok"})
