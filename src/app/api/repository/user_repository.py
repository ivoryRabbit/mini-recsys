import logging
from typing import Optional

from duckdb import DuckDBPyConnection

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, connection: DuckDBPyConnection):
        self._connection = connection

    def get_random_user_id(self) -> Optional[str]:
        query = f"""
            SELECT user_id
            FROM users
            USING SAMPLE 1
            """

        row = self._connection.execute(query).fetchone()

        if row is None:
            return None

        return str(row[0])
