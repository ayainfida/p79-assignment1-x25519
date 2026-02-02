from .group_law import point_addition, point_doubling
from .defaults import A24, p
from .field import fadd, fdiv, fmul, fsub, fsquare
from .point import Point, PointAtInfinity

def cswap(swap: int, a: int, b: int) -> tuple[int, int]:
    """
    Conditional swap of two integers based on the swap bit.
    Its made to be constant-time to avoid side-channel attacks as described in RFC 7748.
    Args:
        swap (int): 0 or 1 indicating whether to swap.
        a (int): First integer.
        b (int): Second integer.

    Regardless of the value of swap, the function takes the same amount of time to execute.

    Returns:
        tuple[int, int]: The (possibly swapped) integers.
    """

    dummy = swap * (a - b) % p
    a = (a - dummy) % p
    b = (b + dummy) % p
    return a, b

def montgomery_ladder(k: int, x: int) -> int:
    """
    Perform scalar multiplication on the Curve25519 using the Montgomery ladder algorithm.
    Args:
        k (int): The scalar multiplier.
        x (int): The x-coordinate of the point to be multiplied.

    The intuition is to calculate k*p, where p is the point with x-coordinate x. 
    
    Returns:
        int: The x-coordinate of the resulting point after multiplication.
    """

    x_1 = x
    x_2 = 1
    z_2 = 0
    x_3 = x
    z_3 = 1
    swap = 0

    for t in range(254, -1, -1):
        k_t = (k >> t) & 1
        swap ^= k_t

        x_2, x_3 = cswap(swap, x_2, x_3)
        z_2, z_3 = cswap(swap, z_2, z_3)
        swap = k_t

        A = fadd(x_2, z_2)
        AA = fsquare(A)
        B = fsub(x_2, z_2)
        BB = fsquare(B)
        E = fsub(AA, BB)
        C = fadd(x_3, z_3)
        D = fsub(x_3, z_3)
        DA = fmul(D, A)
        CB = fmul(C, B)

        x_3 = fsquare(fadd(DA, CB))
        z_3 = fmul(x_1, fsquare(fsub(DA, CB)))
        x_2 = fmul(AA, BB)
        z_2 = fmul(E, fadd(AA, fmul(A24, E)))
    
    x_2, x_3 = cswap(swap, x_2, x_3)
    z_2, z_3 = cswap(swap, z_2, z_3)

    result = fdiv(x_2, z_2)

    return result

def double_and_add(k: int, Pt: Point) -> Point | PointAtInfinity:
    """
    Perform scalar multiplication on the Curve25519 using the double-and-add algorithm.
    Args:
        k (int): The scalar multiplier.
        Pt (Point): The point to be multiplied.

    Returns:
        Point | PointAtInfinity: The resulting point after multiplication.
    """

    if k == 1:
        return Pt
    elif k & 1 == 0:
        return point_doubling(double_and_add(k // 2, Pt))
    else:
        return point_addition(point_doubling(double_and_add((k - 1) // 2, Pt)), Pt)