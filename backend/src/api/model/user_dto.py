from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UserDTO:
    id: int

    @classmethod
    def deserialize(cls, row: Optional[str]) -> Optional['UserDTO']:
        if row is None:
            return None
        return cls(int(row[0]))

    @classmethod
    def deserialize_list(cls, rows: List[str]) -> List['UserDTO']:
        return [cls(int(row[0])) for row in rows]
