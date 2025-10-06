import logging
from typing import List, Optional

from api.component.database import get_connection
from api.model.movie_dto import MovieDTO

logger = logging.getLogger(__name__)


class MovieRepository:
    def __init__(self):
        self._connection = get_connection()

    def find_movie_by_id(self, item_id: int) -> Optional[MovieDTO]:
        query = f"""
            SELECT id, title, genres, year
            FROM movie
            WHERE id={item_id}
        """

        row = self._connection.execute(query).fetchone()
        return MovieDTO.deserialize(row)

    def find_movies_by_ids(self, item_ids: List[int]) -> List[MovieDTO]:
        if len(item_ids) == 0:
            return list()

        predicate = ", ".join([str(item_id) for item_id in item_ids])

        query = f"""
            SELECT id, title, genres, year
            FROM movie
            WHERE id IN ({predicate})
        """

        rows = self._connection.execute(query).fetchall()
        return MovieDTO.deserialize_list(rows)

    def find_movie_by_random(self) -> Optional[MovieDTO]:
        query = f"""
            SELECT id, title, genres, year
            FROM movie
            USING SAMPLE 1
        """

        row = self._connection.execute(query).fetchone()
        return MovieDTO.deserialize(row)
