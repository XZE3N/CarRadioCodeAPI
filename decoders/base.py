from abc import ABC, abstractmethod
from models.schemas import DecodeRequest, DecodeResponse

# Shared decoder registry which contains all the supported manufacturers
DECODER_REGISTRY = {}

class BaseDecoder(ABC):
    """
    Abstract base class for all car radio decoders.
    """

    def __init__(self, request: DecodeRequest):
        self.request = request

    @abstractmethod
    def decode(self) -> DecodeResponse:
        """
        Must be implemented by each subclass.
        :return: Returns a DecodeResponse object containing the decoded data.
        """
        pass

    @abstractmethod
    def compute(self) -> str:
        """
        Must be implemented by each subclass. Used by the decode function.
        :return: Returns the radio code as a string.
        """
        pass

    @classmethod
    def register(cls, make: str) -> None:
        """
        Must be called by each subclass so that it is added to the decoder registry.
        :param make: The decoder's make.
        :return: None. The decoder is added to the registry.
        """
        DECODER_REGISTRY[make.lower()] = cls
