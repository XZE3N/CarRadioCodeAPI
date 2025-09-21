import re

from decoders.base import BaseDecoder
from models.schemas import DecodeResponse

class DaciaDecoder(BaseDecoder):
    def decode(self) -> DecodeResponse:
        if not self.request.security_hash:
            raise ValueError("Dacia requires a security_hash")

        unlock_code = self.compute()

        return DecodeResponse(
            make="Dacia",
            security_hash = self.request.security_hash,
            unlock_code = unlock_code
        )

    def compute(self) -> str:
        code = self.request.security_hash.strip().upper()

        if not re.fullmatch(r"[A-Z]\d{3}", code) or code.startswith("A0"):
            raise ValueError("Invalid Dacia security hash format (Expected format: B123, C321, D456, etc.)")

        x = ord(code[1]) + ord(code[0]) * 10 - 698
        y = ord(code[3]) + ord(code[2]) * 10 + x - 528
        z = (y * 7) % 100

        code = z // 10 + (z % 10) * 10 + ((259 % x) % 100) * 100

        return str(code)

# Self-register plugin
DaciaDecoder.register("dacia")