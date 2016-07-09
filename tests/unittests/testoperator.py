from helper import *


test_operator("Multiplication", lambda x, y: x * y)
test_operator("Division", lambda x, y: x // y)
test_operator("Remainder", lambda x, y: x % y)
test_operator("Bitwise and", lambda x, y: x & y)
test_operator("Bitwise or", lambda x, y: x | y)
test_operator("Bitwise xor", lambda x, y: x ^ y)
test_operator("lshift", lambda x, y: f_bitlshift(x, y % 32))
test_operator("rshift", lambda x, y: f_bitrshift(x, y % 32))
