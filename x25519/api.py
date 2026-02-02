from .encoding import clamp_scalar, decode_x_coordinate, decode_scalar, encode_x_coordinate
from .methods import montgomery_ladder, double_and_add
from .defaults import BASE_X, BASE_Y
from .point import Point
from enum import Enum
import os

class X25519Algorithm(Enum):
    LADDER = "ladder"
    DOUBLE_AND_ADD = "double_and_add"

class X25519:
    def __init__(self, algorithm: X25519Algorithm):
        self.algorithm = algorithm
        self.base_point = Point(BASE_X, BASE_Y)
        self.base_x_bytes = encode_x_coordinate(BASE_X)

    def scalar_mult(self, k: int, x: int) -> bytes:
        if self.algorithm == X25519Algorithm.LADDER:
            result = montgomery_ladder(k, x)
        else:
            result = double_and_add(k, Point(x))
            if result is None:
                raise ValueError("Resulting point is at infinity.")
            result = result.x
        
        return encode_x_coordinate(result)

    def x25519_base(self, sk: bytes) -> bytes:
        k = decode_scalar(sk)
        return self.scalar_mult(k, self.base_point.x)
    
    def x25519(self, sk: bytes, pk: bytes) -> bytes:
        k = decode_scalar(sk)
        x = decode_x_coordinate(pk)
        return self.scalar_mult(k, x)
    
    @staticmethod
    def generate_private_key() -> bytes:
        sk = os.urandom(32)
        return clamp_scalar(sk)
    
    def derive_public_key(self, sk: bytes) -> bytes:
        return self.x25519_base(sk)