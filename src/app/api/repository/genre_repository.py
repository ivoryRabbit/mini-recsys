import logging
from typing import Optional

from app.api.component.database import get_connection

logger = logging.getLogger(__name__)


class GenreRepository:
    def __init__(self):
        self._connection = get_connection()

    def get_random_genre(self) -> Optional[str]:
        query = f"""
            SELECT genre
            FROM genres
            USING SAMPLE 1
            """

        row = self._connection.execute(query).fetchone()

        if row is None:
            return None

        return str(row[0])
