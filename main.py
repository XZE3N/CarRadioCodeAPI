from fastapi import FastAPI, HTTPException

from exceptions.handlers import http_exception_handler, general_exception_handler
from models.schemas import DecodeRequest, DecodeResponse
from decoders.base import DECODER_REGISTRY

app = FastAPI(
    title = "Car Radio Decoder API",
    description = "An API for decoding car radio security codes.",
    version = "1.0.0"
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/", include_in_schema = False)
def root():
    return {
        "service": "Car Radio Decoder API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "manufacturers": sorted(list(DECODER_REGISTRY.keys()))
    }

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@app.get("/manufacturers", tags=["system"], response_model=dict)
def list_manufacturers():
    """
    Returns a list of all supported manufacturers.
    """
    return {"manufacturers": sorted(list(DECODER_REGISTRY.keys()))}

@app.post(
    "/decode",
    tags=["decoder"],
    response_model=DecodeResponse,
    response_model_exclude_none=True, # Removes null fields from JSON response
    responses={
        400: {"description": "Bad Request: Unsupported manufacturer or invalid input"},
        401: {"description": "Unauthorized: Invalid API Key"},
        500: {"description": "Internal Server Error"}
    }
)
def decode(req: DecodeRequest):
    """
    Decodes the car radio code based on the input request data.
    """
    decoder_class = DECODER_REGISTRY.get(req.make.strip().lower())
    if not decoder_class:
        raise HTTPException(status_code=400, detail=f"Unsupported manufacturer: {req.make}")
    try:
        decoder = decoder_class(req)
        return decoder.decode()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")