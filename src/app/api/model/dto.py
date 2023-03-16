from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Movie:
    item_id: str
    title: str
    year: int
    genres: str

    def __post_init__(self):
        self.url = f"https://movielens.org/movies/{self.item_id}"
        self.genres = ", ".join(self.genres.split("|"))

    def as_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "year": self.year,
            "genres": self.genres,
            "url": self.url,
        }
