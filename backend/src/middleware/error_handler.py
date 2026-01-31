"""
Global Error Handler (T217, T219)

Handles exceptions globally with user-friendly messages and structured logging.
"""

import logging
import json
import traceback
import uuid
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_error(
    request_id: str,
    error: Exception,
    request: Request,
    user_id: str = None
):
    """
    Log error with structured format (T219).

    Args:
        request_id: Unique request identifier
        error: Exception that occurred
        request: FastAPI request object
        user_id: User ID if authenticated
    """
    error_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "method": request.method,
        "url": str(request.url),
        "user_id": user_id,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "stack_trace": traceback.format_exc(),
    }

    logger.error(json.dumps(error_log, indent=2))


def add_error_handlers(app: FastAPI) -> None:
    """
    Add global error handlers to FastAPI app (T217).

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions."""
        request_id = str(uuid.uuid4())

        # Log non-404 errors
        if exc.status_code != 404:
            log_error(request_id, exc, request)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.detail,
                    "status_code": exc.status_code,
                    "request_id": request_id,
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors with user-friendly messages."""
        request_id = str(uuid.uuid4())
        log_error(request_id, exc, request)

        # Format validation errors
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "message": "Validation error",
                    "details": errors,
                    "request_id": request_id,
                }
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        """Handle database errors."""
        request_id = str(uuid.uuid4())
        log_error(request_id, exc, request)

        # Don't expose database errors to users
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": "A database error occurred. Please try again later.",
                    "request_id": request_id,
                }
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        request_id = str(uuid.uuid4())
        log_error(request_id, exc, request)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": "An unexpected error occurred. Please try again later.",
                    "request_id": request_id,
                }
            }
        )

    logger.info("✓ Global error handlers configured")


# Request ID middleware for tracing
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to all requests for tracing."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Log request
    logger.info(json.dumps({
        "request_id": request_id,
        "method": request.method,
        "url": str(request.url),
        "timestamp": datetime.utcnow().isoformat(),
    }))

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response
