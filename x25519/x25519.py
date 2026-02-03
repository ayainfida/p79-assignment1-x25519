from .encoding import clamp_scalar, decode_x_coordinate, decode_scalar, encode_x_coordinate
from .methods import montgomery_ladder, double_and_add
from .defaults import BASE_X, BASE_Y
from .point import Point, is_infinity
from os import urandom
from enum import Enum

class X25519Algorithm(Enum):
    LADDER = "ladder"
    DOUBLE_AND_ADD = "double_and_add"

class X25519:
    def __init__(self, algorithm: X25519Algorithm = X25519Algorithm.LADDER):
        """
        Initialize the X25519 class with the specified algorithm.
        
        :param algorithm: The method to use for scalar multiplication (double_and_add or ladder).
        """
        self.algorithm = algorithm
        self.base_point = Point(BASE_X, BASE_Y)
        self.base_x_bytes = encode_x_coordinate(BASE_X)

    def scalar_mult(self, k: int, x: int) -> bytes:
        """
        Perform scalar multiplication on the given x-coordinate using the specified algorithm.
        
        :param k: The scalar multiplier.
        :param x: The x-coordinate to multiply.
        :return: The resulting x-coordinate as bytes.
        """
        if self.algorithm == X25519Algorithm.LADDER:
            result = montgomery_ladder(k, x)
        elif self.algorithm == X25519Algorithm.DOUBLE_AND_ADD:
            result = double_and_add(k, Point(x))
            if is_infinity(result):
                raise ValueError("Resulting point is at infinity.")
            assert isinstance(result, Point), "Result must be a Point after infinity check"
            result = result.x
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        return encode_x_coordinate(result)

    def x25519_base(self, sk: bytes) -> bytes:
        """
        Perform X25519 scalar multiplication with the base point.
        
        :param sk: The private key as bytes.
        :return: The resulting public key as bytes.
        """
        if len(sk) != 32:
            raise ValueError(f"Private key must be 32 bytes long. Provided length: {len(sk)}")
        k = decode_scalar(sk)
        return self.scalar_mult(k, self.base_point.x)
    
    def x25519(self, sk: bytes, pk: bytes) -> bytes:
        """
        Perform X25519 scalar multiplication with the given public key.
        
        :param sk: The private key as bytes.
        :param pk: The public key as bytes.
        :return: The resulting shared secret as bytes.
        """
        if len(sk) != 32:
            raise ValueError(f"Private key must be 32 bytes long. Provided length: {len(sk)}")
        if len(pk) != 32:
            raise ValueError(f"Public key must be 32 bytes long. Provided length: {len(pk)}")
        
        k = decode_scalar(sk) # This includes clamping as well (see encoding.py)
        x = decode_x_coordinate(pk)
        return self.scalar_mult(k, x)
    
    @staticmethod
    def generate_private_key() -> bytes:
        """
        Generate a new private key.
        """
        sk = urandom(32)
        return clamp_scalar(sk)
    
    def derive_public_key(self, sk: bytes) -> bytes:
        """
        Derive the public key from the given private key.
        
        :param sk: The private key as bytes.
        :return: The corresponding public key as bytes.
        """
        if len(sk) != 32:
            raise ValueError(f"Private key must be 32 bytes long. Provided length: {len(sk)}")
        
        return self.x25519_base(sk)