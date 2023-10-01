import logging
import subprocess
import zipfile
from pathlib import Path

import pandas as pd
from fastapi import FastAPI

logger = logging.getLogger(__name__)

LOCAL_PREFIX = "/tmp/dataset"
FILENAME = "ml-1m"
MARKER = "_SUCCESS"


def download_data(app: FastAPI):
    logger.info("Start loading MovieLens dataset...")

    local_path = Path(LOCAL_PREFIX).resolve()
    local_path.mkdir(parents=True, exist_ok=True)

    marker_path = str(local_path.joinpath(MARKER))

    app.state.ratings_filename = f"{LOCAL_PREFIX}/ratings.csv"
    app.state.users_filename = f"{LOCAL_PREFIX}/users.csv"
    app.state.movies_filename = f"{LOCAL_PREFIX}/movies.csv"

    if Path(marker_path).is_file() is True:
        logger.info("MovieLens dataset already exists...")
        return

    try:
        zip_filename = f"{FILENAME}.zip"
        download_url = f"https://files.grouplens.org/datasets/movielens/{zip_filename}"
        subprocess.check_call(f"curl -o {LOCAL_PREFIX}/{zip_filename} {download_url}", shell=True)

        file_zip = zipfile.ZipFile(f"{LOCAL_PREFIX}/{zip_filename}")
        file_zip.extractall(local_path)

        ratings = pd.read_csv(
            f"{LOCAL_PREFIX}/{FILENAME}/ratings.dat",
            delimiter="::",
            names=["user_id", "movie_id", "rating", "timestamp"],
            engine="python",
            encoding="ISO-8859-1",
        )

        ratings.to_csv(app.state.ratings_filename, index=False)

        users = pd.read_csv(
            f"{LOCAL_PREFIX}/{FILENAME}/users.dat",
            delimiter="::",
            names=["id", "gender", "age", "occupation", "zip_code"],
            engine="python",
            encoding="ISO-8859-1",
        )

        users.to_csv(app.state.users_filename, index=False)

        movies = pd.read_csv(
            f"{LOCAL_PREFIX}/{FILENAME}/movies.dat",
            delimiter="::",
            names=["id", "title", "genres"],
            engine="python",
            encoding="ISO-8859-1",
        )
        movies[["title", "year"]] = movies["title"].str.extract(
            r"(?P<title>.*) [(](?P<year>\d+)[)]$"
        )
        movies.to_csv(app.state.movies_filename, index=False)

        subprocess.check_call(f"rm {LOCAL_PREFIX}/{zip_filename}", shell=True)
        subprocess.check_call(f"rm -rf {LOCAL_PREFIX}/{FILENAME}", shell=True)
        subprocess.check_call(f"touch {marker_path}", shell=True)

        logger.info("Finished downloading dataset...")

    except Exception as ex:
        subprocess.check_call(f"rm -rf {LOCAL_PREFIX}", shell=True)

        logger.info("Failed to download dataset...: %s", ex)
