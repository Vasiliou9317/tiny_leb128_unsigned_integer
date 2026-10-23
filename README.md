# tiny_leb128_unsigned_integer

Reads and writes unsigned integers encoded as Little-Endian Base 128, consuming variable byte counts from a buffer.

```python
from tiny_leb128_unsigned_integer import encode, decode, DecodeError

assert encode(0) == b"\x00"
assert encode(300) == b"\xac\x02"
assert decode(b"\xac\x02") == 300

try:
    decode(b"\x80")
except DecodeError:
    pass  # unterminated sequence
```

## Why this exists

A project needed to read and write the unsigned LEB128 values found in
WebAssembly and DWARF without pulling in a parser framework. This is the
minimum that does that correctly.

## Edge case

`decode` does not reject over-long encodings such as `b"\x80\x00"` for
zero. If you need canonical form, compare the output of `encode(decode(x))`
to `x`.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

