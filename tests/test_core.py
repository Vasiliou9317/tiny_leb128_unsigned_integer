import unittest

from tiny_leb128_unsigned_integer import encode, decode, DecodeError


class TestEncode(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(encode(0), b"\x00")

    def test_single_byte(self):
        self.assertEqual(encode(127), b"\x7f")

    def test_two_bytes(self):
        self.assertEqual(encode(128), b"\x80\x01")

    def test_300(self):
        self.assertEqual(encode(300), b"\xac\x02")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            encode(-1)

    def test_bool_rejected(self):
        with self.assertRaises(TypeError):
            encode(True)

    def test_large(self):
        value = (1 << 63) - 1
        self.assertEqual(decode(encode(value)), value)


class TestDecode(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(decode(b"\x00"), 0)

    def test_single_byte(self):
        self.assertEqual(decode(b"\x7f"), 127)

    def test_two_bytes(self):
        self.assertEqual(decode(b"\x80\x01"), 128)

    def test_300(self):
        self.assertEqual(decode(b"\xac\x02"), 300)

    def test_extra_low_zero(self):
        # 0x80 0x00 encodes the same value as 0x00; decoder does not reject.
        self.assertEqual(decode(b"\x80\x00"), 0)

    def test_empty_raises(self):
        with self.assertRaises(DecodeError):
            decode(b"")

    def test_unterminated_raises(self):
        with self.assertRaises(DecodeError):
            decode(b"\x80")

    def test_roundtrip(self):
        for value in [0, 1, 127, 128, 255, 256, 16383, 16384, 1000000]:
            with self.subTest(value=value):
                self.assertEqual(decode(encode(value)), value)


if __name__ == "__main__":
    unittest.main()
