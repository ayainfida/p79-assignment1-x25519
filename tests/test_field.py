import unittest
from random import random
from typing import Callable
from x25519.defaults import p
from x25519.field import fadd, fmul, fsub, finv

class TestFieldOperations(unittest.TestCase):
    def test_fadd(self):
        # Wrap around modulo p 
        self.assertEqual(fadd(2, p-1), 1)
        # Test addition resulting in zero modulo p
        self.assertEqual(fadd(p, p), 0)
    
    def test_fsub(self):
        # Simple subtraction
        self.assertEqual(fsub(p, 5), p - 5)
        # Subtraction resulting in wrap around modulo p
        self.assertEqual(fsub(1, 2), p - 1)
        # Subtraction resulting in zero
        self.assertEqual(fsub(p, p), 0)
    
    def test_fmul(self):
        # Simple multiplication
        self.assertEqual(fmul(3, 4), 12)
        # Multiplication resulting in wrap around modulo p
        self.assertEqual(fmul(p, 2), 0)
        # Multiplication by zero
        self.assertEqual(fmul(0, 123456), 0)

    def _test_abelian_group_operator(self, a: int, b: int, c: int, operator: Callable, identity: int, inverse: int):
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
            a = int(random() * p)
            b = int(random() * p)
            c = int(random() * p)
            self._test_abelian_group_operator(a, b, c, fadd, 0, -a)
    
    def test_abelian_group_fmul(self):
        for _ in range(10):
            a = int(random() * (p - 1)) + 1  # Avoid zero for multiplication
            b = int(random() * (p - 1)) + 1
            c = int(random() * (p - 1)) + 1
            self._test_abelian_group_operator(a, b, c, fmul, 1, finv(a))

if __name__ == "__main__":
    unittest.main()
