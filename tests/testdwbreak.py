import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')

word0, word1, byte0, byte1, byte2, byte3 = f_dwbreak(0x12345678)
SeqCompute([
    (EPD(0x58A364 + 4 * 0), SetTo, word0),
    (EPD(0x58A364 + 4 * 1), SetTo, word1),
    (EPD(0x58A364 + 4 * 2), SetTo, byte0),
    (EPD(0x58A364 + 4 * 3), SetTo, byte1),
    (EPD(0x58A364 + 4 * 4), SetTo, byte2),
    (EPD(0x58A364 + 4 * 5), SetTo, byte3)
])

SaveMap('outputmap/dwbreak.scx')
