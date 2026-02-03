import unittest
from x25519 import X25519, X25519Algorithm

class TestX25519Boundary(unittest.TestCase):
    def setUp(self):
        self.x25519_ladder = X25519(X25519Algorithm.LADDER)

    """
    A good API should validate input lengths and types.
    These tests ensure that the X25519 methods raise appropriate exceptions when given invalid input lengths.
    """

    def test_scalar_length_x25519_base(self):
        # Test if scalar given is not 32 bytes raises ValueError for incorrect lengths and works for correct length

        # 1) Not 32 bytes, should raise ValueError
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519_base(b'\xff\x22\x30')
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519_base(b'\x11' * 31)

        # 2) Empty byte string, should raise ValueError
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519_base(b'')
        
        # 3) Valid length (32 bytes), should not raise
        self.x25519_ladder.x25519_base(b'\xff\x22\x30\x32' * 8)

        # 4) Overlength should raise ValueError
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519_base(b'\x00' * 33)
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519_base(b'\x01' * 64)
    
    def test_x_and_scalar_length_x25519(self):
        # Test if scalar and x-coordinate given are not 32 bytes raises ValueError for incorrect lengths and works for correct length
        # 1) Scalar not 32 bytes, should raise ValueError
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519(b'\x11' * 31, b'\x22' * 32)
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519(b'\x33' * 33, b'\x44' * 32)

        # 2) x-coordinate not 32 bytes, should raise ValueError
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519(b'\x11' * 32, b'\x22' * 31)
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519(b'\x33' * 32, b'\x44' * 33)

        # 3) Both scalar and x-coordinate valid length (32 bytes), should not raise
        self.x25519_ladder.x25519(b'\x11' * 32, b'\x22' * 32)

        # 4) Either of them empty byte string, should raise ValueError
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519(b'', b'\x22' * 32)
        with self.assertRaises(ValueError):
            self.x25519_ladder.x25519(b'\x11' * 32, b'')

    
if __name__ == '__main__':
    unittest.main()