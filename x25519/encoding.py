from .defaults import p

def decode_little_endian(b: bytes) -> int:
    """
    Decode a little-endian byte sequence to an integer.
    """
    return sum((b[i] << (8 * i)) for i in range(len(b)))

def decode_x_coordinate(b: bytes) -> int:
    """
    Decode a 32-byte little-endian byte sequence to an x-coordinate integer.
    """
    assert len(b) == 32, "Input must be 32 bytes long."
    
    # Clear the highest bit of the last byte
    b = b[:-1] + bytes([b[-1] & 0x7F])

    return decode_little_endian(b) % p

def encode_x_coordinate(x: int) -> bytes:
    """
    Encode an x-coordinate integer to a 32-byte little-endian byte sequence.
    """
    x %= p
    
    b = bytearray(32)
    for i in range(32):
        b[i] = (x >> (8 * i)) & 0xFF
    
    return bytes(b)

def clamp_scalar(k: bytes) -> bytes:
    """
    Clamp a 32-byte scalar to avoid small subgroup attacks (detailed in Martin's Tutorial on X25519):
    - Set 3 least-significant bits to 0
    - Set the most-significant bit to 0
    - Set the second most-significant bit to 1
    """
    assert len(k) == 32, "Input must be 32 bytes long."

    k_arr = bytearray(k)
    k_arr[0] &= 248          
    k_arr[31] &= 127        
    k_arr[31] |= 64         
    
    return bytes(k_arr)

def decode_scalar(k: bytes) -> int:
    """
    Decode a 32-byte little-endian byte sequence to a clamped scalar integer.
    I did clamping first before decoding as per RFC 7748; it's the other way around in lecture notes.
    However, the result is the same either way.
    """
    assert len(k) == 32, "Input must be 32 bytes long."
    
    k_clamped = clamp_scalar(k)
    return decode_little_endian(k_clamped)
