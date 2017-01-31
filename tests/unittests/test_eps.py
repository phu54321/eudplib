from .test_eps_epsfile import f_square, f_constv_thing
from helper import *


@TestInstance
def test_epscript():
    test_equality("epScript compile test", f_square(4), 16)
    test_equality("epScript compile test", f_constv_thing(), 55)
