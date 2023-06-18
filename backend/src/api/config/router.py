from fastapi import APIRouter

from api.router import index, demo, recommend, genre

router = APIRouter()

router.include_router(router=demo.router, prefix="/demo", tags=["demo"])

router.include_router(router=index.router, prefix="", tags=["index"])

router.include_router(router=recommend.router, prefix="/rec", tags=["recommend"])

router.include_router(router=genre.router, prefix="/genre", tags=["genre"])
