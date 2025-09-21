from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Custom exception handler.
    :param request: Request object.
    :param exc: Exception object.
    :return: Error JSONResponse.
    """
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "hint": "Check your request and try again"
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom general exception handler.
    :param request: Request object.
    :param exc: Exception object.
    :return: Error JSONResponse.
    """
    return JSONResponse(
        status_code = 500,
        content = {
            "error": {
                "code": 500,
                "message": "Internal server error",
                "hint": "Contact support if this persists"
            }
        }
    )