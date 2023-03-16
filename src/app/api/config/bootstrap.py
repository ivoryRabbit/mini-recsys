import logging

from fastapi import FastAPI

from app.api.batch import bootstrap

logger = logging.getLogger(__name__)


def init_bootstrap(app: FastAPI) -> None:
    bootstrap.download_data(app)
