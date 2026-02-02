import unittest
from x25519.defaults import BASE_X, BASE_Y, INF
from x25519.point import Point
from x25519.group_law import point_addition, point_doubling

"""
Unit tests for group law operations on Curve25519.
These are not exhaustive but cover basic properties, necessary for correctness.
"""

class TestGroupLaw(unittest.TestCase):
    def setUp(self):
        self.Pt = Point(BASE_X, BASE_Y)

    def test_base_point_is_valid(self):
        self.assertTrue(self.Pt.is_valid())

    def test_identity(self):
        self.assertEqual(point_addition(self.Pt, INF), self.Pt)
        self.assertEqual(point_addition(INF, self.Pt), self.Pt)

    def test_doubling_matches_addition(self):
        self.assertEqual(point_doubling(self.Pt), point_addition(self.Pt, self.Pt))

    def test_result_is_on_curve(self):
        Q = point_doubling(self.Pt)
        self.assertTrue(Q.is_valid())


if __name__ == "__main__":
    unittest.main()