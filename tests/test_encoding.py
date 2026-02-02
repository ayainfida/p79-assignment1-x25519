import unittest
from x25519.defaults import P
from x25519.encoding import encode_x_coordinate, decode_x_coordinate, clamp_scalar, decode_scalar

class TestEncoding(unittest.TestCase):
    def test_decode_x_coordinate_length(self):
        # Test that decode_x_coordinate raises ValueError for incorrect lengths and works for correct length

        # 1) Not 32 bytes, should raise ValueError
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'\xff\x22\x30')
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'\x11' * 31)
        
        # 2) Valid length (32 bytes), should not raise
        decode_x_coordinate(b'\xff\x22\x30\x32' * 8)
    
    def test_decode_x_coordinate_mask_msb(self):
        # The highest bit of the last byte should be cleared as defined in RFC 7748 for x-coordinate decoding
        b = bytearray(32)
        b[-1] = 0x80  # Set all bits in the last byte        
        decoded = decode_x_coordinate(bytes(b))
        self.assertEqual(decoded, 0)
    
    def test_encode_x_coordinate_length(self):
        # Length of encoded x-coordinate should always be 32 bytes

        # 1) Encode small values and check length
        self.assertEqual(len(encode_x_coordinate(1)), 32)
        self.assertEqual(len(encode_x_coordinate(128)), 32)

        # 2) Encode near P and check length
        self.assertEqual(len(encode_x_coordinate(P-1)), 32)
        self.assertEqual(len(encode_x_coordinate(P)), 32)

        #3) Encode bigger than P and check length
        self.assertEqual(len(encode_x_coordinate(P + 5)), 32)
        self.assertEqual(len(encode_x_coordinate(P + 123456789)), 32)

    def test_encode_decode_x_coordinate(self):
        # Test that encoding followed by decoding returns the original x-coordinate modulo P
        # Values cover small, near P, and larger than P cases
        test_values = [0, 1, 128, 123456789, P-1, P, P+5, P+123456789, 2*P+42]

        for x in test_values:
            encoded = encode_x_coordinate(x)
            decoded = decode_x_coordinate(encoded)
            self.assertEqual(decoded, x % P)
    
    def test_decode_scalar_length(self):
        # Test that decode_scalar raises ValueError for incorrect lengths and works for correct length
        with self.assertRaises(ValueError):
            decode_scalar(b'\x00\x01\x02')
        with self.assertRaises(ValueError):
            decode_scalar(b'\x00' * 31)
        decode_scalar(b'\x00' * 32)
    
    def test_decode_scalar(self):
        # Test that decode_scalar correctly clamps as per RFC 7748 and decodes the scalar
        
        # Example scalar before clamping
        original_scalar = bytearray(32)
        original_scalar[0] = 0xFF  # All bits set in first byte
        original_scalar[31] = 0xFF  # All bits set in last byte

        decoded_scalar = decode_scalar(bytes(original_scalar))

        # Check clamping
        self.assertEqual(decoded_scalar & 0b00000111, 0)  # 3 LSBs cleared
        self.assertEqual(decoded_scalar & (1 << 255), 0)  # MSB cleared
        self.assertEqual(decoded_scalar & (1 << 254), 1 << 254)  # Second MSB set


if __name__ == '__main__':
    unittest.main()