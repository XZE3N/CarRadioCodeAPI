import re
import struct
from pathlib import Path

from decoders.base import BaseDecoder
from models.schemas import DecodeResponse

class FordDecoder(BaseDecoder):
    """
    Ford M and V series radio code decoder.
    Uses a binary lookup table (radiocodes.bin).
    """

    SERIAL_PATTERN = re.compile(r"^[MV]\d{6}$")

    def __init__(self, request):
        super().__init__(request)
        # Load the binary database path once per instance
        self.db_path = Path(__file__).parent / "radiocodes.bin"
        if not self.db_path.exists():
            raise FileNotFoundError(f"Radio code database not found at {self.db_path.resolve()}")

    def decode(self) -> DecodeResponse:
        if not self.request.serial_number:
            raise ValueError("Ford requires a serial_number")

        unlock_code = self.compute()

        return DecodeResponse(
            make="Ford",
            serial_number = self.request.serial_number,
            unlock_code = unlock_code
        )

    def compute(self) -> str:
        serial = self.request.serial_number.strip().upper()

        if not self.SERIAL_PATTERN.fullmatch(serial):
            raise ValueError("Invalid Ford serial format (Expected format: M123456 or V123456)")

        # Compute file offset
        index = int(serial[1:])
        offset = index * 2

        if serial.startswith("V"):
            offset += 2000000

        # Read 2 bytes at offset
        with open(self.db_path, "rb") as f:
            f.seek(offset)
            data = f.read(2)
            if len(data) != 2:
                raise ValueError("Serial number out of range")

            # Little-endian 16-bit unsigned integer
            code = struct.unpack("<H", data)[0]

        return str(code).zfill(4)

# Self-register plugin
FordDecoder.register("ford")