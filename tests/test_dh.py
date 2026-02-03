import unittest
from x25519 import X25519, X25519Algorithm


class TestRFCdh(unittest.TestCase):
    def setUp(self):
        # Set up X25519 instances for both algorithms
        self.x25519_ladder = X25519(X25519Algorithm.LADDER)
        self.x25519_double_and_add = X25519(X25519Algorithm.DOUBLE_AND_ADD)

    """
    Helper function to test Diffie-Hellman key exchange using provided vectors
    It tests key generation, public key derivation, and shared secret computation
    """

    def _set_dh_vectors(self, alice_sk: bytes, bob_sk: bytes, alice_pk: bytes, bob_pk: bytes, shared_secret: bytes):
        # Return a dictionary of the provided DH vectors
        return {
            "alice_sk": alice_sk,
            "bob_sk": bob_sk,
            "alice_expected_pk": alice_pk,
            "bob_expected_pk": bob_pk,
            "expected_shared_secret": shared_secret,
        }

    def _test_dh_vectors(self, x25519_instance: X25519, dh_vectors: dict):
        # Test Diffie-Hellman key exchange using provided vectors
        alice_pk = x25519_instance.x25519_base(dh_vectors["alice_sk"])
        self.assertEqual(alice_pk, dh_vectors["alice_expected_pk"])

        bob_pk = x25519_instance.x25519_base(dh_vectors["bob_sk"])
        self.assertEqual(bob_pk, dh_vectors["bob_expected_pk"])
        alice_shared_secret = x25519_instance.x25519(dh_vectors["alice_sk"], bob_pk)
        bob_shared_secret = x25519_instance.x25519(dh_vectors["bob_sk"], alice_pk)

        self.assertEqual(alice_shared_secret, bob_shared_secret)
        self.assertEqual(alice_shared_secret, dh_vectors["expected_shared_secret"])

    """
    Test vectors from RFC 7748 Section 6.2 -- Diffie-Hellman key exchange
    """

    def _test_rfc7748_dh(self, x25519_instance: X25519):
        dh_vectors = self._set_dh_vectors(
            alice_sk=bytes.fromhex(
                "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
            ),
            bob_sk=bytes.fromhex(
                "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
            ),
            alice_pk=bytes.fromhex(
                "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
            ),
            bob_pk=bytes.fromhex(
                "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
            ),
            shared_secret=bytes.fromhex(
                "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"
            ),
        )

        self._test_dh_vectors(x25519_instance, dh_vectors)

    def test_rfc7748_dh_double_and_add(self):
        self._test_rfc7748_dh(self.x25519_double_and_add)

    def test_rfc7748_dh_montgomery_ladder(self):
        self._test_rfc7748_dh(self.x25519_ladder)
    
    """
    Test vectors sourced from https://github.com/TomCrypto/pycurve25519/tree/master -- Diffie-Hellman key exchange
    """

    def _test_pycurve25519_dh(self, x25519_instance: X25519):
        dh_vectors = self._set_dh_vectors(
            alice_sk = bytes.fromhex(
                "a8abababababababababababababababababababababababababababababab6b"
            ),
            bob_sk = bytes.fromhex(
                "c8cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd4d"
            ),
            alice_pk = bytes.fromhex(
                "e3712d851a0e5d79b831c5e34ab22b41a198171de209b8b8faca23a11c624859"
            ),
            bob_pk = bytes.fromhex(
                "b5bea823d9c9ff576091c54b7c596c0ae296884f0e150290e88455d7fba6126f"
            ),
            shared_secret = bytes.fromhex(
                "235101b705734aae8d4c2d9d0f1baf90bbb2a8c233d831a80d43815bb47ead10"
            )   
        )

        self._test_dh_vectors(x25519_instance, dh_vectors)

    def test_pycurve25519_dh_double_and_add(self):
        self._test_pycurve25519_dh(self.x25519_double_and_add)

    def test_pycurve25519_dh_montgomery_ladder(self):
        self._test_pycurve25519_dh(self.x25519_ladder)

    """
    Test vectors generated using randomly selected private keys -- Diffie-Hellman key exchange
    """

    def _test_random_dh(self, x25519_instance: X25519):
        alice_sk = x25519_instance.generate_private_key()
        bob_sk = x25519_instance.generate_private_key()

        alice_pk = x25519_instance.x25519_base(alice_sk)
        bob_pk = x25519_instance.x25519_base(bob_sk)

        alice_shared_secret = x25519_instance.x25519(alice_sk, bob_pk)
        bob_shared_secret = x25519_instance.x25519(bob_sk, alice_pk)
        self.assertEqual(alice_shared_secret, bob_shared_secret)

    def test_random_dh_double_and_add(self):
        self._test_random_dh(self.x25519_double_and_add)

    def test_random_dh_montgomery_ladder(self):
        self._test_random_dh(self.x25519_ladder)

if __name__ == '__main__':
    unittest.main()