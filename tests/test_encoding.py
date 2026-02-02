import unittest
from x25519.defaults import p
from x25519.encoding import decode_little_endian, encode_x_coordinate, decode_x_coordinate, decode_scalar

class TestEncoding(unittest.TestCase):
    def test_decode_x_coordinate_length(self):
        # Test that decode_x_coordinate raises ValueError for incorrect lengths and works for correct length

        # 1) Not 32 bytes, should raise ValueError
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'\xff\x22\x30')
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'\x11' * 31)

        # 2) Empty byte string, should raise ValueError
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'')
        
        # 3) Valid length (32 bytes), should not raise
        decode_x_coordinate(b'\xff\x22\x30\x32' * 8)

        # 4) Overlength should raise ValueError
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'\x00' * 33)
        with self.assertRaises(ValueError):
            decode_x_coordinate(b'\x01' * 64)
    
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

        # 2) Encode near p and check length
        self.assertEqual(len(encode_x_coordinate(p-1)), 32)
        self.assertEqual(len(encode_x_coordinate(p)), 32)

        #3) Encode bigger than p and check length
        self.assertEqual(len(encode_x_coordinate(p + 5)), 32)
        self.assertEqual(len(encode_x_coordinate(p + 123456789)), 32)

    def test_encode_decode_x_coordinate(self):
        # Test that encoding followed by decoding returns the original x-coordinate modulo p
        # Values cover small, near p, and larger than p cases
        test_values = [0, 1, 128, 123456789, p-1, p, p+5, p+123456789, 2*p+42]

        for x in test_values:
            encoded = encode_x_coordinate(x)
            decoded = decode_x_coordinate(encoded)
            self.assertEqual(decoded, x % p)
    
    def test_decode_scalar_length(self):
        # Test that decode_scalar raises ValueError for incorrect lengths and works for correct length
        # Fewer than 32 bytes, should raise ValueError
        with self.assertRaises(ValueError):
            decode_scalar(b'\x00\x01\x02')
        with self.assertRaises(ValueError):
            decode_scalar(b'')
        with self.assertRaises(ValueError):
            decode_scalar(b'\x00' * 31)
        # Overlength should raise ValueError
        with self.assertRaises(ValueError):
            decode_scalar(b'\x00' * 33)
        # Valid length (32 bytes), should not raise
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

        # As per RFC 7748, the decoded scalar is 2^254 + something between 0 and 2^251 - 1
        self.assertGreater(decoded_scalar, 2**254)

        # No effect on values that are already clamped, so decoding a clamped scalar should return the same integer
        test_scalar = bytearray(32)
        test_scalar[0] = 0xF8
        test_scalar[31] = 0x40
        self.assertEqual(decode_scalar(bytes(test_scalar)), decode_little_endian(bytes(test_scalar)))

if __name__ == '__main__':
    unittest.main()