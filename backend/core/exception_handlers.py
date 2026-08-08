"""
Global exception handlers for FastAPI.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from core.logger import logger


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Handles all unexpected exceptions.
    """

    logger.exception("Unhandled exception for %s: %s", request.url.path, exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )