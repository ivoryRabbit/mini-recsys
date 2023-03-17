import yaml
import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.model.response import DEFAULT_RESPONSES
from app.api.config.router import router
from app.api.config import scheduler, bootstrap
from app.api.component import template, database

with open("src/app/logging.yml") as f:
    logging_config = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="mini-recommender-system",
    version="0.1.0",
    responses=DEFAULT_RESPONSES
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.mount(
    "/static",
    StaticFiles(directory="src/app/client/static"),
    name="static",
)


@app.on_event("startup")
async def app_startup() -> None:
    logger.info("App startup")

    # Bootstrap
    template.init_template()
    bootstrap.init_bootstrap(app)

    await scheduler.init_scheduler(app)
    await database.init_connection(app)


@app.on_event("shutdown")
async def app_shutdown() -> None:
    logger.info("App shutdown")


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=5000,
        access_log=False,
        reload=True,
    )
