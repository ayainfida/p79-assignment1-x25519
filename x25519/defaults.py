# Setting default curve parameters for X25519
# equation: y^2 = x^3 + A*x^2 + x over the field defined by prime p

# Prime number defining the field
p = 2**255 - 19

# Curve parameter A and derived constant A24
A = 486662
A24 = (A - 2) // 4

# Base point coordinates
BASE_X = 9
BASE_Y = 14781619447589544791020593568409986887264606134616475288964881837755586237401