import math
import random
import logging
from collections import Counter
from typing import List, Tuple

from fastapi import Depends
from fastapi.requests import Request

from api.model.movie_dto import MovieDTO
from api.repository.graph import InteractionGraph
from api.repository.movie_repository import MovieRepository

logger = logging.getLogger(__name__)


class RandomWalkService:
    def __init__(
        self,
        request: Request,
        total_steps: int = 10000,
        alpha: float = 0.3,
        n_p: int = 100,
        n_v: int = 10,
        beta: float = 0.95,
        movie_repository: MovieRepository = Depends(),
    ):
        self.total_steps = total_steps
        self.alpha = alpha
        self.n_p = n_p
        self.n_v = n_v
        self.beta = beta
        self._graph: InteractionGraph = request.app.state.graph
        self._movie_repository = movie_repository

    def inference(self, queries: List[int], top_k: int = 10) -> List[MovieDTO]:
        total_counter = Counter()
        max_step = self.total_steps // len(queries)

        for query in queries:
            node_name = self._graph.get_item_node(query)
            counter = self.walk_randomly(node_name, max_step=max_step)

            for item in counter:
                if query == item:
                    continue

                score = math.pow(counter[item], 0.5)
                total_counter.update({item: score})

        results = total_counter.most_common(top_k)
        item_ids = self._refine_recommendation(results)
        return self._movie_repository.find_movies_by_ids(item_ids)

    def get_sample_items_from_user(self, user_id: int, size: int = 5) -> List[int]:
        return self._graph.get_sample_items_from_user(user_id, size)

    def walk_randomly(self, query: str, max_step: int) -> Counter:
        curr_step = 0
        max_visited = 0
        len_walks = math.ceil(self.alpha * max_step)

        visit_counter = Counter()

        if self._graph.has_node(query) is False:
            return visit_counter

        while curr_step < max_step and max_visited < self.n_p:
            curr_item = query

            for _ in range(len_walks):
                curr_user = self._graph.get_random_neighbor(curr_item)
                curr_item = self._graph.get_random_neighbor(curr_user)

                visit_counter.update([curr_item])

                if visit_counter.get(curr_item) == self.n_v:
                    max_visited += 1

                curr_step += len_walks

                if random.random() > self.beta:
                    curr_item = query

        return visit_counter

    def _refine_recommendation(self, results: List[Tuple[str, int]]) -> List[int]:
        item_ids = []
        for node_name, _ in results:
            item_id = self._graph.get_item_id(node_name)
            item_ids.append(int(item_id))

        return item_ids
