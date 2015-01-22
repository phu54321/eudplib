import pyximport
pyximport.install()

import verifyf
import os

testvector = bytearray(os.urandom(10))


import cProfile
import pstats

cProfile.runctx(
    'verifyf.verifyf(testvector, len(testvector))',
    globals(),
    locals(),
    "Profile.prof"
)

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats('time').print_stats()

