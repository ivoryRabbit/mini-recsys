import logging
from typing import Tuple, List

from api.component.database import get_connection

logger = logging.getLogger(__name__)


class PopularRepository:
    def __init__(self):
        self._connection = get_connection()

    def find_popular_by_view(self, genre: str, size: int) -> Tuple[List[int], List[int]]:
        query = f"""
            SELECT p.movie_id, p.view
            FROM popular p
            JOIN movie m ON m.id = p.movie_id AND LOWER(m.genres) LIKE '%'||$genre||'%'
            ORDER BY p.view DESC, m.year DESC
            LIMIT {size}
        """

        rows = self._connection.execute(query, {"genre": genre.lower()}).fetchall()

        if rows is None:
            return list(), list()

        movie_ids = []
        views = []
        for row in rows:
            movie_ids.append(int(row[0]))
            views.append(int(row[1]))

        return movie_ids, views

    def find_popular_by_rating(self, genre: str, size: int) -> Tuple[List[int], List[float]]:
        query = f"""
            SELECT p.movie_id, p.rating
            FROM popular p
            JOIN movie m ON m.id = p.movie_id AND LOWER(m.genres) LIKE '%'||$genre||'%'
            ORDER BY p.rating DESC, m.year DESC
            LIMIT {size}
        """

        rows = self._connection.execute(query, {"genre": genre.lower()}).fetchall()

        movie_ids = []
        ratings = []
        for row in rows:
            movie_ids.append(int(row[0]))
            ratings.append(float(row[1]))

        return movie_ids, ratings
