from .encoding import clamp_scalar, decode_little_endian, decode_x_coordinate, decode_scalar, encode_x_coordinate
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

if __name__ == "__main__":
    # Example usage
    k = bytes.fromhex(
        "4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d"
    )

    u = bytes.fromhex(
        "e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493"
    )

    x25519_instance = X25519(X25519Algorithm.LADDER)
    shared_secret = x25519_instance.x25519(k, u)
    print(f"Shared secret (LADDER): {shared_secret.hex()}")

    x25519_instance_d = X25519(X25519Algorithm.DOUBLE_AND_ADD)
    shared_secret = x25519_instance_d.x25519(k, u)
    print(f"Shared secret (DOUBLE_AND_ADD): {shared_secret.hex()}")

    # alice_sk = bytes.fromhex(
    #     "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
    # )
    # print("Alice's private key:", alice_sk.hex())
    # alice_pk = x25519_instance.x25519_base(alice_sk)
    # print(f"Alice's public key: {alice_pk.hex()}")

    # bob_sk = bytes.fromhex(
    #     "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
    # )
    # print("Bob's private key:", bob_sk.hex())
    # bob_pk = x25519_instance.x25519_base(bob_sk)
    # print(f"Bob's public key: {bob_pk.hex()}")

    # alice_shared_secret = x25519_instance.x25519(alice_sk, bob_pk)
    # print(f"Alice's shared secret: {alice_shared_secret.hex()}")
    # bob_shared_secret = x25519_instance.x25519(bob_sk, alice_pk)
    # print(f"Bob's shared secret: {bob_shared_secret.hex()}")    