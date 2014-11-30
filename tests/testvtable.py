import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')
a, b, ret = EUDCreateVariables(3)

main = NextTrigger()

SeqCompute([
    (EPD(0x58A364), SetTo, a.GetVTable()),
    (EPD(0x58A368), SetTo, b.GetVTable()),
    (EPD(0x58A36C), SetTo, ret.GetVTable()),
    (a, SetTo, 10),
    (b, SetTo, 20),
    (ret, SetTo, a),
    (ret, Add, b)
])

SaveMap('outputmap/vtable.scx', main)
