from fastapi import APIRouter

from api.router import index, recommend, demo

router = APIRouter()

router.include_router(router=demo.router, prefix="/demo", tags=["demo"])

router.include_router(router=index.router, prefix="", tags=["index"])

router.include_router(router=recommend.router, prefix="/rec", tags=["recommend"])
