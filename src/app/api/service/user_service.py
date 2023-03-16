import logging
from typing import Optional

from fastapi import Depends

from app.api.component.database import get_connection
from app.api.repository.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, connection=Depends(get_connection)):
        self._repository = UserRepository(connection)

    def get_random_user_id(self) -> Optional[str]:
        return self._repository.get_random_user_id()
