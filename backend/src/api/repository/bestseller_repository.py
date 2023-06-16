import logging
from typing import Tuple, List

from api.component.database import get_connection

logger = logging.getLogger(__name__)


class BestsellerRepository:
    def __init__(self):
        self._connection = get_connection()

    def get_bestseller_by_popular(self, genre: str, size: int) -> Tuple[List[str], List[int]]:
        query = f"""
            SELECT b.item_id, b.popular
            FROM bestseller b
            JOIN movies m ON m.item_id = b.item_id AND LOWER(m.genres) LIKE '%{genre.lower()}%'
            ORDER BY b.popular DESC, m.year DESC
            LIMIT {size}
        """

        logger.info(query)

        rows = self._connection.execute(query).fetchall()

        if rows is None:
            return list(), list()

        item_ids = []
        populars = []
        for row in rows:
            item_ids.append(str(row[0]))
            populars.append(int(row[1]))

        return item_ids, populars

    def get_bestseller_by_rating(self, genre: str, size: int) -> Tuple[List[str], List[float]]:
        query = f"""
            SELECT b.item_id, b.rating
            FROM bestseller b
            JOIN movies m ON m.item_id = b.item_id AND LOWER(m.genres) LIKE '%{genre.lower()}%'
            ORDER BY b.rating DESC, m.year DESC
            LIMIT {size}
        """

        logger.info(query)

        rows = self._connection.execute(query).fetchall()

        if rows is None:
            return list(), list()

        item_ids = []
        ratings = []
        for row in rows:
            item_ids.append(str(row[0]))
            ratings.append(float(row[1]))

        return item_ids, ratings
