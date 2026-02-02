from .defaults import p

def fadd(a: int, b: int) -> int:
    """
    Add two field elements modulo p.
    """
    return (a + b) % p

def fsub(a: int, b: int) -> int:
    """
    Subtract two field elements modulo p.
    """
    return (a - b) % p

def fmul(a: int, b: int) -> int:
    """
    Multiply two field elements modulo p.
    """
    return (a * b) % p

def fsquare(a: int) -> int:
    """
    Square a field element modulo p.
    """
    return fmul(a, a)

def finv(a: int) -> int:
    """
    Compute inverse by Fermat’s little theorem
    a^(p-1) = a.a^(p-2) ≡ 1 (mod p) 
    """
    if a == 0:
        raise ValueError("Cannot compute inverse of zero.")
    return pow(a, p - 2, p)

def fdiv(a: int, b: int) -> int:
    """
    Divide two field elements modulo p.
    """
    b_inv = finv(b)
    return fmul(a, b_inv)

def fsqrt(a: int) -> int:
    """
    Compute square root of a field element modulo p using the algorithm stated in Slide 116 (defined in RFC 8032).
    """
    a %= p
    if a == 0:
        return 0
    
    candidate_root_1 = pow(a, (p + 3) // 8, p)
    if fsquare(candidate_root_1) % p == a:
        return candidate_root_1
    
    candidate_root_2 = fmul(candidate_root_1, pow(2, (p - 1) // 4, p))
    if fsquare(candidate_root_2) % p == a:
        return candidate_root_2
    
    raise ValueError("No square root exists for the given element in the field.")