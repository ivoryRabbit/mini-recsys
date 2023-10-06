import logging
from typing import Optional, List

from api.component.database import get_connection
from api.model.genre_dto import GenreDTO

logger = logging.getLogger(__name__)


class GenreRepository:
    def __init__(self):
        self._connection = get_connection()

    def find_genre_by_random(self) -> Optional[GenreDTO]:
        query = f"""
            SELECT name
            FROM genre
            USING SAMPLE 1
        """

        row = self._connection.execute(query).fetchone()
        return GenreDTO.deserialize(row)

    def find_all_genre(self) -> List[GenreDTO]:
        query = f"""
            SELECT name
            FROM genre
        """

        rows = self._connection.execute(query).fetchall()
        return GenreDTO.deserialize_list(rows)
