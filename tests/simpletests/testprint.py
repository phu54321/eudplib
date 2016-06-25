from helper import *


@TestInstance
def main():
    f_initextstr()

    a = EUDVariable(5)
    b = a * a * a * a * a
    f_simpleprint(" \x03- \x04 Print testing")
    f_simpleprint('    \x04test ', a, ' b: ', hptr(b), ' test')
    f_simpleprint('    \x04test  5  b:  00000C35  test')
    test_wait(36)
