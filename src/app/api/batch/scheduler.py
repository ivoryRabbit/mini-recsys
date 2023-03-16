from fastapi import FastAPI

from app.api.component import scheduler
from app.api.repository.graph import InteractionGraph


@scheduler.scheduled(seconds=24 * 60 * 60, raise_exceptions=True)
def build_graph(app: FastAPI):
    app.state.graph = InteractionGraph(app.state.ratings_filename)
