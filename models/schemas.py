from pydantic import BaseModel
from typing import Optional

class DecodeRequest(BaseModel):
    """
    Base class for all decode request types.
    """
    make: str
    serial_number: Optional[str] = None
    vin: Optional[str] = None
    security_hash: Optional[str] = None

class DecodeResponse(BaseModel):
    """
    Base class for all decode response types.
    """
    make: str
    unlock_code: str
    serial_number: Optional[str] = None
    vin: Optional[str] = None
    security_hash: Optional[str] = None