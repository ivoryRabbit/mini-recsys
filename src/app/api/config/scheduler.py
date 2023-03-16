import logging

from fastapi import FastAPI

from app.api.batch import scheduler

logger = logging.getLogger(__name__)


async def init_scheduler(app: FastAPI) -> None:
    await scheduler.build_graph(app)
