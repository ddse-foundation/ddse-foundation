from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

class TaskFlowException(Exception):
    """Base exception class for TaskFlow application following EDR-002"""
    def __init__(self, detail: str, status_code: int = 500):
        self.detail = detail
        self.status_code = status_code

class TeamAccessDenied(TaskFlowException):
    """Exception for team-based access control violations"""
    def __init__(self, detail: str = "Access denied: insufficient team permissions"):
        super().__init__(detail, status.HTTP_403_FORBIDDEN)

class ResourceNotFound(TaskFlowException):
    """Exception for resource not found errors"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail, status.HTTP_404_NOT_FOUND)

async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler implementing EDR-002 error handling strategy"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "type": "internal_error",
            "path": str(request.url.path)
        }
    )

async def taskflow_exception_handler(request: Request, exc: TaskFlowException):
    """Handler for custom TaskFlow exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "application_error",
            "path": str(request.url.path)
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler for HTTP exceptions with standardized format per EDR-002"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "http_error",
            "path": str(request.url.path)
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for Pydantic validation errors per IDR-002"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "type": "validation_error",
            "errors": exc.errors(),
            "path": str(request.url.path)
        }
    )
