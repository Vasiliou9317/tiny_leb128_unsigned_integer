"""tiny_leb128_unsigned_integer — read and write unsigned LEB128 integers."""

from .core import encode, decode, DecodeError

__all__ = ["encode", "decode", "DecodeError"]
