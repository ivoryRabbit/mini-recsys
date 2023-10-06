from dataclasses import dataclass
from typing import Optional, List


@dataclass
class GenreDTO:
    name: str

    @classmethod
    def deserialize(cls, row: Optional[str]) -> Optional['GenreDTO']:
        if row is None:
            return None
        return cls(row[0])

    @classmethod
    def deserialize_list(cls, rows: List[str]) -> List['GenreDTO']:
        return [cls(row[0]) for row in rows]
