from .defaults import A
from .field import fadd, fmul, fsquare, fsub, fdiv
from .point import Point, PointAtInfinity, INF


def point_addition(P: Point | PointAtInfinity, Q: Point | PointAtInfinity) -> Point | PointAtInfinity:
    """
    Add two points P and Q on the Curve25519.

    Args:
        P (Point | PointAtInfinity): First point.
        Q (Point | PointAtInfinity): Second point.

    Returns:
        Point | PointAtInfinity: The resulting point P + Q.
    """

    if P == INF:
        return Q
    elif Q == INF:
        return P
    
    x1, y1 = P.x, P.y
    x2, y2 = Q.x, Q.y

    if x1 == x2 and fadd(y1, y2) == 0:
        return INF
    elif x1 == x2:
        return point_doubling(P)
    
    # Computing x3
    slope = fdiv(fsub(y2, y1), fsub(x2, x1))
    slope_square = fsquare(slope)
    x3 = fsub(fsub(slope_square, A), fadd(x1, x2))

    # Computing y3
    y3 = fsub(fmul(slope, fsub(x1, x3)), y1)

    return Point(x3, y3)

def point_doubling(P: Point | PointAtInfinity) -> Point | PointAtInfinity:
    """
    Double a point P on the Curve25519.
    Args:
        P (Point | PointAtInfinity): The point to double.

    Returns:
        Point | PointAtInfinity: The resulting point 2P.
    """
    if P == INF:
        return INF
    
    x, y = P.x, P.y

    if y == 0:
        return INF

    # Computing x3
    xx = fsquare(x)
    ax = fmul(A, x)
    slope = fdiv(
        fadd(fadd(fmul(3, xx), fmul(2, ax)), 1), 
        fadd(y, y))
    slope_square = fsquare(slope)
    x3 = fsub(fsub(slope_square, A), fadd(x, x))

    # Computing y3
    y3 = fsub(fmul(slope, fsub(x, x3)), y)

    return Point(x3, y3)