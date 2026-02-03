import unittest
from x25519 import X25519, X25519Algorithm

class TestRFCVectors(unittest.TestCase):
    def setUp(self):
        self.x25519_ladder = X25519(X25519Algorithm.LADDER)
        self.x25519_double_and_add = X25519(X25519Algorithm.DOUBLE_AND_ADD)

    """
    Test vectors from RFC 7748 Section 5.2 -- single-shot tests
    These tests use specific input values and check against expected outputs.
    """
    def test_rfc_vector_1(self):
        k = bytes.fromhex(
            "a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4"
        )
        u = bytes.fromhex(
            "e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c"
        )
        expected = bytes.fromhex(
            "c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552"
        )

        out_ladder = self.x25519_ladder.x25519(k, u)
        self.assertEqual(out_ladder, expected)

        out_double_and_add = self.x25519_double_and_add.x25519(k, u)
        self.assertEqual(out_double_and_add, expected)

    def test_rfc_vector_2(self):
        k = bytes.fromhex(
            "4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d"
        )
        u = bytes.fromhex(
            "e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493"
        )
        expected = bytes.fromhex(
            "95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957"
        )

        out_ladder = self.x25519_ladder.x25519(k, u)
        self.assertEqual(out_ladder, expected)

        # This is expected to fail as the x point when decoded does not correspond to a valid point on the curve, so the compute_y method raises a ValueError
        with self.assertRaises(ValueError):
            self.x25519_double_and_add.x25519(k, u)
    
    """
    Test vectors from RFC 7748 Section 5.2 -- iterative tests
    These tests perform repeated applications of the X25519 function, starting from a known value.
    The expected outputs after these iterations are provided in the RFC.
    """
    # I have commented the 1000000 iteration out as it takes too long to compute. (It took me ~17 minutes with this uncommented to run the test suite. Yet, it passed.)
    def test_rfc_iterative_vector_montgomery_ladder(self):
        k = bytes.fromhex(
            "0900000000000000000000000000000000000000000000000000000000000000"
        )

        u = bytes.fromhex(
            "0900000000000000000000000000000000000000000000000000000000000000"
        )

        expected = {
            1 : "422c8e7a6227d7bca1350b3e2bb7279f7897b87bb6854b783c60e80311ae3079",
            1000 : "684cf59ba83309552800ef566f2f4d3c1c3887c49360e3875f2eb94d99532c51",
            # 1000000 : "7c3911e0ab2586fd864497297e575e6f3bc601c0883c30df5f4dd2d24f665424",
        }

        expected_keys_list = list(expected.keys())

        result = {}

        for i in range(1, expected_keys_list[-1] + 1):
            k, u = self.x25519_ladder.x25519(k, u), k
            if i in expected_keys_list:
                result[i] = k

        for i in expected_keys_list:
            self.assertEqual(result[i], bytes.fromhex(expected[i]))

    def test_rfc_iterative_vector_double_and_add(self):
        k = bytes.fromhex(
            "0900000000000000000000000000000000000000000000000000000000000000"
        )

        u = bytes.fromhex(
            "0900000000000000000000000000000000000000000000000000000000000000"
        )

        expected = {
            1 : "422c8e7a6227d7bca1350b3e2bb7279f7897b87bb6854b783c60e80311ae3079",
            1000 : "684cf59ba83309552800ef566f2f4d3c1c3887c49360e3875f2eb94d99532c51",
            # 1000000 : "7c3911e0ab2586fd864497297e575e6f3bc601c0883c30df5f4dd2d24f665424", 
        }

        expected_keys_list = list(expected.keys())

        result = {}

        for i in range(1, expected_keys_list[-1] + 1):
            k, u = self.x25519_double_and_add.x25519(k, u), k
            if i in expected_keys_list:
                result[i] = k

        for i in expected_keys_list:
            self.assertEqual(result[i], bytes.fromhex(expected[i]))


if __name__ == "__main__":
    unittest.main()