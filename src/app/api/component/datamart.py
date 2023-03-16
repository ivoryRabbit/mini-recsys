import logging
from functools import lru_cache
from typing import Optional

import duckdb
from duckdb import DuckDBPyConnection
from fastapi import FastAPI

logger = logging.getLogger(__name__)

_connection: Optional[DuckDBPyConnection] = None


async def init_connection(app: FastAPI) -> None:
    logger.info("Initiate in-memory datamart connection...")

    global _connection
    _connection = duckdb.connect(":memory:")

    queries = [
        """
        PRAGMA threads=1;
        """,
        f"""
        CREATE TABLE item_statistic AS (
            SELECT item_id, COUNT(user_id) AS popular, AVG(rating) AS rating
            FROM '{app.state.ratings_filename}'
            GROUP BY 1
        );
        """,
        f"""
        CREATE TABLE user_recent_items AS (
            SELECT user_id, item_id
            FROM (
                SELECT *, row_number() OVER (PARTITION BY user_id ORDER BY "timestamp" DESC) AS rank
                FROM '{app.state.ratings_filename}'
            )
            WHERE rank <= 5
        );
        """,
    ]

    for query in queries:
        _connection.execute(query)

    logger.info("Finished acquiring in-memory datamart connection...")


async def close_connection() -> None:
    global _connection

    if _connection is not None:
        _connection.close()


@lru_cache(maxsize=None)
def get_connection() -> DuckDBPyConnection:
    global _connection
    assert _connection is not None
    return _connection
