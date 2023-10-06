from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple


@dataclass
class MovieDTO:
    id: int
    title: str
    genres: str
    year: int
    view: Optional[int] = None
    rating: Optional[float] = None

    def __post_init__(self):
        self.url = f"https://movielens.org/movies/{self.id}"
        self.genres = ", ".join(self.genres.split("|"))

    @classmethod
    def deserialize(cls, row: Optional[str]) -> Optional['MovieDTO']:
        if row is None:
            return None
        return cls(int(row[0]), row[1], row[2], int(row[3]))

    @classmethod
    def deserialize_list(cls, rows: List[Tuple[str]]) -> List['MovieDTO']:
        return [cls(int(row[0]), row[1], row[2], int(row[3])) for row in rows]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.id,
            "title": self.title,
            "year": self.year,
            "genres": self.genres,
            "url": self.url,
            "view": self.view,
            "rating": self.rating,
        }
