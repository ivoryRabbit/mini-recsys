import logging
from typing import Optional

from api.component.database import get_connection
from api.model.user_dto import UserDTO

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self):
        self._connection = get_connection()

    def find_user_by_random(self) -> Optional[UserDTO]:
        query = f"""
            SELECT id
            FROM user
            USING SAMPLE 1
        """

        row = self._connection.execute(query).fetchone()
        return UserDTO.deserialize(row)
