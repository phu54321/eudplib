import pyximport
pyximport.install()

import verifyf
import os

testvector = bytearray(os.urandom(10 * 1024 * 1024))


import cProfile
import pstats

cProfile.runctx(
    'verifyf.verifyf(testvector)',
    globals(),
    locals(),
    "Profile.prof"
)

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats('time').print_stats()

print(verifyf.verifyf(testvector))
