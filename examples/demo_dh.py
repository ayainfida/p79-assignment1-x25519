import argparse
from hashlib import sha256
from x25519 import X25519, X25519Algorithm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo X25519 DH exchange")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--l', action='store_true', help='Use Montgomery ladder algorithm')
    group.add_argument('--d', action='store_true', help='Use double-and-add algorithm')
    args = parser.parse_args()

    if args.l:
        algo = X25519Algorithm.LADDER
        print("Using Montgomery ladder algorithm.")
    elif args.d:
        algo = X25519Algorithm.DOUBLE_AND_ADD
        print("Using double-and-add algorithm.")

    x25519_instance = X25519(algo)

    alice_sk = x25519_instance.generate_private_key()
    bob_sk = x25519_instance.generate_private_key()

    alice_pk = x25519_instance.derive_public_key(alice_sk)
    bob_pk = x25519_instance.derive_public_key(bob_sk)

    alice_shared_secret = x25519_instance.x25519(alice_sk, bob_pk)
    bob_shared_secret = x25519_instance.x25519(bob_sk, alice_pk)
    alice_shared_secret_hashed = sha256(alice_shared_secret).digest()
    bob_shared_secret_hashed = sha256(bob_shared_secret).digest()

    print("Alice's Public Key: ", alice_pk.hex())
    print("Bob's Public Key:   ", bob_pk.hex())
    print("Alice's Shared Secret (hashed):", alice_shared_secret_hashed.hex())
    print("Bob's Shared Secret (hashed):  ", bob_shared_secret_hashed.hex())

    assert alice_shared_secret_hashed == bob_shared_secret_hashed, "Shared secrets do not match!"
                                             
                                    
