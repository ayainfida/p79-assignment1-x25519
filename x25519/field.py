from .defaults import P

def fadd(a: int, b: int) -> int:
    """
    Add two field elements modulo P.
    """
    return (a + b) % P

def fsub(a: int, b: int) -> int:
    """
    Subtract two field elements modulo P.
    """
    return (a - b) % P

def fmul(a: int, b: int) -> int:
    """
    Multiply two field elements modulo P.
    """
    return (a * b) % P

def fsquare(a: int) -> int:
    """
    Square a field element modulo P.
    """
    return fmul(a, a)

def finv(a: int) -> int:
    """
    Compute inverse by Fermat’s little theorem
    a^(P-1) = a.a^(P-2) ≡ 1 (mod P) 
    """
    if a == 0:
        raise ValueError("Cannot compute inverse of zero.")
    return pow(a, P - 2, P)

def fdiv(a: int, b: int) -> int:
    """
    Divide two field elements modulo P.
    """
    b_inv = finv(b)
    return fmul(a, b_inv)

def fsqrt(a: int) -> int:
    """
    Compute square root of a field element modulo P using the algorithm stated in Slide 116 (defined in RFC 8032).
    """
    a %= P
    if a == 0:
        return 0
    
    candidate_root_1 = pow(a, (P + 3) // 8, P)
    if fsquare(candidate_root_1) % P == a:
        return candidate_root_1
    
    candidate_root_2 = fmul(candidate_root_1, pow(2, (P - 1) // 4, P))
    if fsquare(candidate_root_2) % P == a:
        return candidate_root_2
    
    raise ValueError("No square root exists for the given element in the field.")