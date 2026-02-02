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
    
# if __name__ == "__main__":
#     # Example point validation
#     # pt = Point(6208869506345768410841466502331656783811117849709423753404619313487976949323)#, 57831201774152980679071250004583825374997192814258762277502187681216496958535)
#     print('--------------------------')
#     x = decode_x_coordinate(bytes.fromhex(
#         'e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c'
#     ))

#     x1 = decode_little_endian(bytes.fromhex(
#         'e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c'
#     ))

#     print(x == x1)

#     rhs = fadd(fadd(fmul(fsquare(x), x), fmul(A, fsquare(x))), x) % P
#     print("RHS:", rhs)

#     lhs = fsquare(4361149298140551963281614885053274602169670096990126099798427732476501230008) % P
#     print("LHS:", lhs)

#     from .encoding import encode_x_coordinate, clamp_scalar

#     k = decode_little_endian(clamp_scalar(bytes.fromhex(
#         'a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4'
#     )))

#     from .methods import double_and_add, montgomery_ladder

#     print(encode_x_coordinate(double_and_add(k, Point(x, 4361149298140551963281614885053274602169670096990126099798427732476501230008)).x).hex())

#     print(encode_x_coordinate(montgomery_ladder(k, x)).hex())

#     print('--------------------------')

#     x = decode_x_coordinate(bytes.fromhex(
#         'e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a4a3'
#     ))

#     print('x', x)

#     x1 = decode_little_endian(bytes.fromhex(
#         'e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a4a3'
#     ))

#     print('x1', x1)

#     print(x == x1)

#     rhs = fadd(fadd(fmul(fsquare(x), x), fmul(A, fsquare(x))), x) % P
#     print("RHS:", rhs)

#     lhs = fsquare(16154125192364555935288950380174260710202235663694825863245833351938259681156) % P
#     print("LHS:", lhs)

#     from .encoding import encode_x_coordinate, clamp_scalar

#     k = decode_little_endian(clamp_scalar(bytes.fromhex(
#         '4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d'
#     )))

#     from .methods import double_and_add, montgomery_ladder

#     print(encode_x_coordinate(double_and_add(k, Point(x, 16154125192364555935288950380174260710202235663694825863245833351938259681156)).x).hex())

#     print(encode_x_coordinate(montgomery_ladder(k, x)).hex())

#     print('--------------------------')
