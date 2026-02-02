# Setting default curve parameters for X25519
# equation: y^2 = x^3 + A*x^2 + x over the field defined by prime P

P = 2**255 - 19
A = 486662
A24 = (A - 2) // 4
BASE_X = 9
BASE_Y = 14781619447589544791020593568409986887264606134616475288964881837755586237401