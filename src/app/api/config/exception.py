import logging

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.model.response import Response, ErrorMessage, ErrorCode

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error(exc, exc_info=True)
    return Response.error(
        ErrorMessage(errorCode=ErrorCode.SERVER_ERROR, reason=str(exc.detail)),
        exc.status_code,
    )


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(exc, exc_info=True)
    return Response.internal_server_error(
        ErrorMessage(errorCode=ErrorCode.SERVER_ERROR, reason="Fail")
    )


async def request_validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(exc, exc_info=True)
    return Response.bad_request(
        ErrorMessage(errorCode=ErrorCode.INVALID_REQUEST, reason="Fail")
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=HTTPException, handler=http_exception_handler
    )

    app.add_exception_handler(
        exc_class_or_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        handler=request_validation_error_handler,
    )

    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=request_validation_error_handler,
    )

    app.add_exception_handler(
        exc_class_or_status_code=Exception, handler=exception_handler
    )
