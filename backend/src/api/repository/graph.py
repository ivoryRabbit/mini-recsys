import logging
import random
from typing import List

import pandas as pd
import networkx as nx

logger = logging.getLogger(__name__)


class InteractionGraph:
    _USER_PREFIX = "U"
    _ITEM_PREFIX = "I"

    def __init__(self, path: str):
        self._graph = self._build_graph(path)

    def _build_graph(self, path: str) -> nx.Graph:
        logger.info("Build graph model...")

        edges = (
            pd.read_csv(
                path,
                usecols=["user_id", "movie_id"],
                converters={
                    "user_id": lambda x: self._USER_PREFIX + str(x),
                    "movie_id": lambda x: self._ITEM_PREFIX + str(x),
                }
            )
        )

        graph = nx.Graph()

        graph.add_nodes_from(edges["user_id"].unique(), bipartite="users")
        graph.add_nodes_from(edges["movie_id"].unique(), bipartite="items")
        graph.add_edges_from(edges.itertuples(index=False))

        logger.info("Finished building graph model...")
        return graph

    def get_user_node(self, user_id: int) -> str:
        node = self._USER_PREFIX + str(user_id)
        if self.is_valid_node(node) is False:
            raise Exception("Invalid node id")
        return node

    def get_item_node(self, item_id: int) -> str:
        node = self._ITEM_PREFIX + str(item_id)
        if self.is_valid_node(node) is False:
            raise Exception("Invalid node id")
        return node

    def get_sample_items_from_user(self, user_id: int, size: int = 5) -> List[int]:
        user_node = self.get_user_node(user_id)
        sample_items = list(self._graph.neighbors(user_node))

        if len(sample_items) > size:
            sample_items = random.sample(list(sample_items), size)

        return list(map(self.get_item_id, sample_items))

    def get_random_neighbor(self, node: str) -> str:
        return random.choice(list(self._graph.neighbors(node)))

    def get_item_id(self, node: str) -> int:
        if node.startswith(self._ITEM_PREFIX) is True:
            node = node.removeprefix(self._ITEM_PREFIX)
        return int(node)

    def is_valid_node(self, node: str) -> bool:
        return self._graph.has_node(node)
