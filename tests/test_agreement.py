import os
import unittest
from x25519.api import X25519, X25519Algorithm
from x25519.encoding import decode_x_coordinate
from x25519.point import Point

class TestX25519Agreement(unittest.TestCase):
    def setUp(self):
        # Set up X25519 instances for both algorithms
        self.x25519_ladder = X25519(X25519Algorithm.LADDER)
        self.x25519_double_and_add = X25519(X25519Algorithm.DOUBLE_AND_ADD)
        self.runs = 20 # Number of iterations for random tests

    """
    Test Diffie-Hellman key exchange on the base point
    Since base point is valid, both algorithms should yield the same shared secret, otherwise it's 
    """
    def test_agreement_on_base_point(self):
        # Test Diffie-Hellman key exchange on the base point
        for i in range(self.runs):
            sk = self.x25519_ladder.generate_private_key()
            pk = self.x25519_ladder.derive_public_key(sk)
            shared_secret_ladder = self.x25519_ladder.x25519(sk, pk)
            shared_secret_double_and_add = self.x25519_double_and_add.x25519(sk, pk)
            self.assertEqual(shared_secret_ladder, shared_secret_double_and_add)

    """
    Test Diffie-Hellman key exchange with random keys
    Since random keys may not correspond to valid points, we first check validity before performing the agreement
    """
    def test_agreement_with_random_keys(self):
        # Test Diffie-Hellman key exchange with random keys
        count_valid_points = 0
        while count_valid_points < self.runs:
            try:
                x = os.urandom(32)
                Point(decode_x_coordinate(x))
            except ValueError:
                continue  # Invalid point, try again

            count_valid_points += 1

            sk = self.x25519_ladder.generate_private_key()
            pk = self.x25519_ladder.x25519(sk, x)

            shared_secret_ladder = self.x25519_ladder.x25519(sk, pk)
            shared_secret_double_and_add = self.x25519_double_and_add.x25519(sk, pk)
            self.assertEqual(shared_secret_ladder, shared_secret_double_and_add)

if __name__ == "__main__":
    unittest.main()