import pyximport
pyximport.install()
from stackobjs import StackObjects
import pickle

obj = pickle.load(open('stackdata.bin', 'rb'))
found_objects = obj['found_objects']
dwoccupmap_dict = obj['dwoccupmap_dict']
dsdict = obj['dsdict']
alloctable = {}

import os

testvector = bytearray(os.urandom(10 * 1024 * 1024))


import cProfile
import pstats

cProfile.runctx(
    'StackObjects(found_objects, dwoccupmap_dict, alloctable, dsdict)',
    globals(),
    locals(),
    "Profile.prof"
)

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats('time').print_stats()
