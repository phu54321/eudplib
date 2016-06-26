from helper import *


@TestInstance
def main():
    f_initextstr()

    a = EUDVariable(5)
    b = a * a * a * a * a

    x = DBString(1024)
    y = DBString(1024)
    f_dbstr_print(x, '    \x04test ', a, ' b: ', hptr(b), ' test', 1, hptr(21))
    f_dbstr_print(y, '    \x04test 5 b: 00000C35 test100000015')
    test_assert("f_dbstr_print test", f_strcmp(x, y) == 0)
