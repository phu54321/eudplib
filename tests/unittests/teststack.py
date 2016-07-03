from helper import *


@TestInstance
def test_stack():
    k = EUDStack(1024)
    k.push(123)
    k.push(456)
    t1 = k.pop()  # 456
    k.push(789)
    k.push(234)
    t2 = k.pop()  # 234
    t3 = EUDTernary(k.empty(), 1, 0)  # 0
    t4 = k.pop()  # 789
    t5 = k.pop()  # 123
    t6 = EUDTernary(k.empty(), 1, 0)  # 1

    test_equality(
        "Stack test",
        [t1, t2, t3, t4, t5, t6],
        [456, 234, 0, 789, 123, 1]
    )
