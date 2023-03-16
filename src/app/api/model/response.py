from enum import Enum, auto

from fastapi import status
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class ErrorCode(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    INVALID_REQUEST = auto()
    SERVER_ERROR = auto()


class ErrorMessage(BaseModel):
    errorCode: ErrorCode = None
    reason: str = None


class Response:
    @staticmethod
    def ok(content: BaseModel, status_code=status.HTTP_200_OK):
        return JSONResponse(content=content.dict(), status_code=status_code)

    @staticmethod
    def error(content: ErrorMessage, status_code=status.HTTP_400_BAD_REQUEST):
        return JSONResponse(content=content.dict(), status_code=status_code)

    @staticmethod
    def bad_request(content: ErrorMessage):
        return JSONResponse(
            content=content.dict(), status_code=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def unprocessable_entity(content: ErrorMessage):
        return JSONResponse(
            content=content.dict(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @staticmethod
    def internal_server_error(content: ErrorMessage):
        return JSONResponse(
            content=content.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


DEFAULT_RESPONSES = {
    400: {"model": ErrorMessage, "description": "Bad Request"},
    422: {"model": ErrorMessage, "description": "Unprocessable Entity"},
    500: {"model": ErrorMessage, "description": "Internal Server Error"},
}
