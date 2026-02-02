import unittest
from random import random
from x25519.defaults import P
from x25519.field import fadd, fmul, fsub, finv

class TestFieldOperations(unittest.TestCase):
    def test_fadd(self):
        # Wrap around modulo P 
        self.assertEqual(fadd(2, P-1), 1)
        # Test addition resulting in zero modulo P
        self.assertEqual(fadd(P, P), 0)
    
    def test_fsub(self):
        # Simple subtraction
        self.assertEqual(fsub(P, 5), P - 5)
        # Subtraction resulting in wrap around modulo P
        self.assertEqual(fsub(1, 2), P - 1)
        # Subtraction resulting in zero
        self.assertEqual(fsub(P, P), 0)
    
    def test_fmul(self):
        # Simple multiplication
        self.assertEqual(fmul(3, 4), 12)
        # Multiplication resulting in wrap around modulo P
        self.assertEqual(fmul(P, 2), 0)
        # Multiplication by zero
        self.assertEqual(fmul(0, 123456), 0)

    def _test_abelian_group_operator(self, a: int, b: int, c: int, operator: callable, identity: int, inverse: int):
        # 1) Closure
        self.assertIsInstance(operator(a, b), int)

        # 2) Commutativity: a ⊕ b = b ⊕ a
        self.assertEqual(operator(a, b), operator(b, a))

        # 3) Associativity: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)
        self.assertEqual(operator(operator(a, b), c), operator(a, operator(b, c)))

        # 4) Identity exists: a ⊕ e = a
        self.assertEqual(operator(a, identity), a)

        # 5) Inverse exists: a ⊕ a_inv = e
        self.assertEqual(operator(a, inverse), identity)
    
    def test_abelian_group_fadd(self):
        for _ in range(10):
            a = int(random() * P)
            b = int(random() * P)
            c = int(random() * P)
            self._test_abelian_group_operator(a, b, c, fadd, 0, -a)
    
    def test_abelian_group_fmul(self):
        for _ in range(10):
            a = int(random() * (P - 1)) + 1  # Avoid zero for multiplication
            b = int(random() * (P - 1)) + 1
            c = int(random() * (P - 1)) + 1
            self._test_abelian_group_operator(a, b, c, fmul, 1, finv(a))

if __name__ == "__main__":
    unittest.main()
