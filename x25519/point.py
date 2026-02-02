from dataclasses import dataclass

from x25519.encoding import decode_little_endian, decode_x_coordinate
from .defaults import P, A
from .field import fadd, fsqrt, fsquare, fmul

@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int | None = None):
        self.x = x % P
        if y is not None:
            self.y = y % P
            if not self.is_valid():
                raise ValueError("The provided point is not a valid point on the curve.")
            
        else:
            y = self.calculate_y()  
            if y is None:
                raise ValueError("The provided x-coordinate does not correspond to a valid point on the curve.")
            self.y = y
    
    def is_valid(self) -> bool:
        """
        Check if the point lies on the curve defined by the equation:
        y^2 = x^3 + A*x^2 + x (mod P)
        """
        lhs = fsquare(self.y)
        rhs = fadd(fadd(fmul(fsquare(self.x), self.x), fmul(A, fsquare(self.x))), self.x)
        return lhs == rhs
    
    def calculate_y(self) -> int | None:
        """
        Given the x-coordinate, calculate the corresponding y-coordinate(s) on the curve.
        """
        xx = fsquare(self.x)
        x_cube = fmul(xx, self.x)
        ax2 = fmul(A, xx)
        rhs = fadd(fadd(x_cube, ax2), self.x)

        try:
            y = fsqrt(rhs)
        except ValueError:
            return None
        
        return y % P