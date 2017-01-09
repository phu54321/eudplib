from .test_eps_epsfile import f_square
from helper import *


@TestInstance
def test_epscript():
    test_equality("epScript compile test", f_square(4), 16)
