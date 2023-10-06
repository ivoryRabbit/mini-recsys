import logging
from functools import lru_cache
from typing import Optional

import duckdb
from duckdb import DuckDBPyConnection
from fastapi import FastAPI

logger = logging.getLogger(__name__)

_connection: Optional[DuckDBPyConnection] = None


async def init_connection(app: FastAPI) -> None:
    logger.info("Initiate in-memory database connection...")

    global _connection
    _connection = duckdb.connect(":memory:")

    queries = [
        """
            CREATE TABLE user (
                "id"         INT PRIMARY KEY,
                "gender"     VARCHAR(2),
                "age"        SMALLINT,
                "occupation" SMALLINT,
                "zip_code"   VARCHAR(10)
            );
        """,
        f"""
            COPY user FROM '{app.state.users_filename}' (
                AUTO_DETECT FALSE, HEADER TRUE
            );
        """,
        """
            CREATE TABLE movie (
                "id"      INT PRIMARY KEY,
                "title"   VARCHAR(100),
                "genres"  VARCHAR(100),
                "year"    INT
            );
        """,
        f"""
            COPY movie FROM '{app.state.movies_filename}' (
                AUTO_DETECT FALSE, HEADER TRUE
            );
        """,
        f"""
            CREATE TABLE popular AS (
                SELECT 
                    movie_id::INT AS movie_id, 
                    COUNT(user_id) AS view,
                    ROUND(AVG(rating), 3) AS rating
                FROM '{app.state.ratings_filename}'
                GROUP BY 1
            );
        """,
        f"""
            CREATE TABLE genre AS (
                SELECT DISTINCT UNNEST(STR_SPLIT(genres, '|')) AS name
                FROM movie
                ORDER BY 1
            );
        """,
    ]

    for query in queries:
        _connection.execute(query)

    logger.info("Finished acquiring in-memory database connection...")


async def close_connection() -> None:
    global _connection

    if _connection is not None:
        _connection.close()


@lru_cache(maxsize=None)
def get_connection() -> DuckDBPyConnection:
    global _connection
    assert _connection is not None
    return _connection
