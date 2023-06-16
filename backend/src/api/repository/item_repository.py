import logging
from typing import List, Optional

from api.component.database import get_connection
from api.model.dto import Movie

logger = logging.getLogger(__name__)


class ItemRepository:
    def __init__(self):
        self._connection = get_connection()

    def get_movie_meta(self, item_id: str) -> Optional[Movie]:
        query = f"""
            SELECT item_id, title, genres, year
            FROM movies
            WHERE item_id={item_id}
        """

        row = self._connection.execute(query).fetchone()

        if row is None:
            return None

        movie = Movie(
            item_id=str(row[0]),
            title=str(row[1]),
            genres=str(row[2]),
            year=int(row[3]),
        )

        return movie

    def get_movie_metas(self, item_ids: List[str]) -> List[Movie]:
        if len(item_ids) == 0:
            return list()

        predicate = ", ".join([str(item_id) for item_id in item_ids])

        query = f"""
            SELECT item_id, title, genres, year
            FROM movies
            WHERE item_id IN ({predicate})
        """

        logger.info(query)

        rows = self._connection.execute(query).fetchall()

        if rows is None:
            return list()

        result_map = {}
        for row in rows:
            item_id = str(row[0])
            result_map[item_id] = Movie(
                item_id=item_id,
                title=str(row[1]),
                genres=str(row[2]),
                year=int(row[3]),
            )

        return [result_map[item_id] for item_id in item_ids]

    def get_random_item_id(self) -> Optional[str]:
        query = f"""
            SELECT item_id
            FROM movies
            USING SAMPLE 1
            """

        row = self._connection.execute(query).fetchone()

        if row is None:
            return None

        return str(row[0])
