from fastapi import APIRouter

from app.api.router import index, demo, recommend

router = APIRouter()

router.include_router(router=demo.router, prefix="/demo", tags=["demo"])

router.include_router(router=index.router, prefix="", tags=["index"])

router.include_router(router=recommend.router, prefix="/rec", tags=["recommend"])
