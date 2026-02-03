# Assignment 1: Elliptic Curve Diffie-Hellman (X25519)

This assignment implements X25519 key exchange from scratch in Python, following RFC 7748. It supports both Montgomery ladder and double-and-add scalar multiplication algorithms.

## ⚠️ Security Disclaimer

**This implementation is for educational purposes only (in particular, submission for Assignment 1 of P79: Cryptography and Protocol Engineering offered at the University of Cambridge) and is NOT suitable for production use.**

## Features

- **Two scalar multiplication algorithms**: Montgomery ladder and double-and-add
- **Complete X25519 API**: Private key generation, public key derivation, and shared secret computation using x25519(.,.)
- **RFC 7748 compliance**: All test vectors pass on montgomery ladder 
- **Comprehensive testing**: Tests covering RFC vectors, DH agreement, field operations, group laws and encodings

## Repo Structure

```
x25519/              # Core implementation
├── x25519.py        # Main X25519 API with algorithm selection
├── point.py         # Point and PointAtInfinity defined
├── field.py         # Field arithmetic (add, mul, inv, sqrt, div, sub)
├── group_law.py     # Point addition and doubling
├── methods.py       # Montgomery ladder and double-and-add
├── encoding.py      # Byte encoding/decoding and scalar clamping
└── defaults.py      # Curve parameters and constants

tests/                       # Test suite
├── test_rfc7748_vectors.py  # RFC 7748 test vectors
├── test_dh.py               # Diffie-Hellman key exchange
├── test_field.py            # Field operation properties
├── test_group_law.py        # Point operation correctness
├── test_encoding.py         # Encoding/decoding edge cases
└── test_agreement.py        # Key agreement validation

examples/
└── demo_dh.py       # DH key exchange demo

report/
└── P79_mafr2_A1.pdf         # report 
```

## Setup

You will need to install the following:

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-docker/)

## Development

For local development, clone the repository and let `uv` create a virtual environment with the required dependencies.

```bash
git clone https://github.com/ayainfida/p79-assignment1-x25519.git
cd p79-assignment1-x25519
uv sync
```

The `run.sh` script builds and runs the Docker image. It executes the type checker and linter during the build process and then runs the unit tests in a container.

```bash
./run.sh
```

You can run the type checker, linter, and the unit tests locally as well:

```bash
uv run ty check      # Static type checking
uv run ruff check    # Linting
uv run -m unittest   # Run all tests
```

### Running the Demo

The repo includes a Diffie-Hellman demo that supports both algorithms:

```bash
# Using Montgomery ladder
python -m examples.demo_dh --l

# Using double-and-add
python -m examples.demo_dh --d
```

This generates random key pairs for Alice and Bob, performs DH key exchange, and verifies that both parties derive the same shared secret.

### Running Specific Test Suites

```bash
python -m unittest tests.test_rfc7748_vectors  # RFC test vectors (section 5.2) only
python -m unittest tests.test_dh               # DH key exchange
python -m unittest tests.test_field            # Field operations
python -m unittest tests.test_encoding -v      # Encoding/decoding/clamping
```

## Algorithm Details

### Montgomery Ladder
- Works with x-coordinates only
- Suitable for arbitrary point multiplication
- Follows RFC 7748 specification exactly

### Double-and-Add
- Requires a valid (x, y) coordinates
- Computes y coordinate using the square root method specified in RFC 8032
- Recursive implementation

The API allows to select the appropriate algorithm for scalar multiplication (default is set to use ladder based scalar multiplication). You can use the X25519 API in your own Python code as follows:

```python
from x25519 import X25519, X25519Algorithm

# x25519 using montgomery ladder 
x25519_ladder = X25519(X25519Algorithm.LADDER)

# x25519 using group laws
x25519_group_laws = X25519(X25519Algorithm.DOUBLE_AND_ADD)
```

## References

- [RFC 7748: Elliptic Curves for Security](https://www.rfc-editor.org/rfc/rfc7748)
- [RFC 8032: Edwards-Curve Digital Signature Algorithm (EdDSA)](https://www.rfc-editor.org/rfc/rfc8032)
- [Curve25519: New Diffie-Hellman Speed Records](https://cr.yp.to/ecdh.html) by Daniel J. Bernstein
- [Implementing Curve25519/X25519: A Tutorial on Elliptic Curve Cryptography](http://martin.kleppmann.com/papers/curve25519.pdf) by Martin Kelppmann

## License

MIT License - See [LICENSE](LICENSE) file for details.
