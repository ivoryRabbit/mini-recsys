import os
import logging
import subprocess
import zipfile
from pathlib import Path

import pandas as pd
from fastapi import FastAPI

logger = logging.getLogger(__name__)

LOCAL_PREFIX = "/tmp/dataset"
MARKER = "_SUCCESS"
STATUS = "_RUNNING"


def download_data(app: FastAPI):
    logger.info("Start loading MovieLens dataset...")

    _local_path = Path(LOCAL_PREFIX).resolve()
    _local_path.mkdir(parents=True, exist_ok=True)

    filename = "ml-1m.zip"
    marker_path = str(_local_path.joinpath(MARKER))

    app.state.ratings_filename = f"{LOCAL_PREFIX}/ratings.csv"
    app.state.users_filename = f"{LOCAL_PREFIX}/users.csv"
    app.state.movies_filename = f"{LOCAL_PREFIX}/movies.csv"

    if Path(marker_path).is_file() is True:
        logger.info("MovieLens dataset already exists...")
        return

    if os.getenv("status") == STATUS:
        return

    os.environ["status"] = STATUS

    try:
        download_url = f"https://files.grouplens.org/datasets/movielens/{filename}"
        subprocess.check_call(f"curl -o {LOCAL_PREFIX}/{filename} {download_url}", shell=True)

        file_zip = zipfile.ZipFile(f"{LOCAL_PREFIX}/{filename}")
        file_zip.extractall(_local_path)

        ratings = pd.read_csv(
            f"{LOCAL_PREFIX}/ml-1m/ratings.dat",
            delimiter="::",
            names=["user_id", "item_id", "rating", "timestamp"],
            engine="python",
            encoding="ISO-8859-1",
        )

        ratings.to_csv(app.state.ratings_filename, index=False)

        users = pd.read_csv(
            f"{LOCAL_PREFIX}/ml-1m/users.dat",
            delimiter="::",
            names=["user_id", "gender", "age", "occupation", "zip_code"],
            engine="python",
            encoding="ISO-8859-1",
        )

        users.to_csv(app.state.users_filename, index=False)

        movies = pd.read_csv(
            f"{LOCAL_PREFIX}/ml-1m/movies.dat",
            delimiter="::",
            names=["item_id", "title", "genres"],
            engine="python",
            encoding="ISO-8859-1",
        )
        movies[["title", "year"]] = movies["title"].str.extract(r"(?P<title>.*) [(](?P<year>\d+)[)]$")
        movies.to_csv(app.state.movies_filename, index=False)

        subprocess.check_call(f"rm {LOCAL_PREFIX}/{filename}", shell=True)
        subprocess.check_call(f"rm -rf {LOCAL_PREFIX}/ml-1m", shell=True)
        subprocess.check_call(f"touch {marker_path}", shell=True)

        logger.info("Finished downloading dataset...")

    except Exception as ex:
        subprocess.check_call(f"rm -rf {LOCAL_PREFIX}", shell=True)

        logger.info("Failed to download dataset...: %s", ex)

    del os.environ["status"]
