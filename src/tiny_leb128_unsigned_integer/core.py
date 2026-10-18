"""Little-Endian Base 128 encoding for unsigned integers.

LEB128 packs each 7 bits of the integer into one byte, storing the
continuation bit in the most-significant bit. Low bits are written
first so a reader can accumulate value as it reads.
"""


class DecodeError(Exception):
    """Raised when the input to decode is malformed."""


def encode(value: int) -> bytes:
    """Encode a non-negative integer as unsigned LEB128.

    Raises ValueError when value is negative or not an int.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be int")
    if value < 0:
        raise ValueError("value must be non-negative")

    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def decode(data: bytes) -> int:
    """Decode unsigned LEB128 bytes into an int.

    A byte with its top bit clear terminates the sequence. Raises
    DecodeError if data is empty or contains no terminating byte.
    """
    if not data:
        raise DecodeError("empty input")

    result = 0
    shift = 0
    for i, byte in enumerate(data):
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return result
        shift += 7

    raise DecodeError("unterminated sequence")
