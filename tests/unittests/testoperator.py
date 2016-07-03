from helper import *


test_operator("Multiplication", lambda x, y: x * y)
test_operator("Division", lambda x, y: x // y)
test_operator("Remainder", lambda x, y: x % y)
test_operator("Bitwise and", lambda x, y: x & y)
test_operator("Bitwise or", lambda x, y: x | y)
test_operator("Bitwise xor", lambda x, y: x ^ y)
