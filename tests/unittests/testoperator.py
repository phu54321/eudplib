from helper import *
import random


def create_operator_test(name, realf, exptf=None):
    if exptf is None:
        exptf = realf

    @TestInstance
    def test_operator():
        a = EUDVariable()
        b = EUDVariable()
        expt, real = [], []

        for i in range(20):
            r1 = random.randint(0, 0xFFFFFFFF)
            r2 = random.randint(0, 0xFFFFFFFF)
            SetVariables([a, b], [r1, r2])
            real.append(realf(a, b))
            expt.append(exptf(r1, r2) & 0xFFFFFFFF)

        test_assert(
            "Operator test : %s" % name,
            [r == e for r, e in zip(real, expt)]
        )

create_operator_test("Multiplication", lambda x, y: x * y)
create_operator_test("Division", lambda x, y: x // y)
create_operator_test("Remainder", lambda x, y: x % y)
create_operator_test("Bitwise and", lambda x, y: x & y)
create_operator_test("Bitwise or", lambda x, y: x | y)
create_operator_test("Bitwise xor", lambda x, y: x ^ y)
