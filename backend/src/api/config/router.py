from fastapi import APIRouter

from api.router import ping, recommend, genre

router = APIRouter()

router.include_router(router=ping.router, prefix="", tags=["ping"])

router.include_router(router=recommend.router, prefix="/rec", tags=["recommend"])

router.include_router(router=genre.router, prefix="/genre", tags=["genre"])
