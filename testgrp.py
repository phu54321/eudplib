from eudtrg import *
from eudtrg.auxlib import EUDGrp

LoadMap('outputmap/grpbasemap.scx')

a = EUDGrp(open('outputmap/inputgrp.grp', 'rb').read())

# change zergling grp to inputgrp.grp
k = Trigger(
    actions = SetMemory(0x51CED0 + 4 * 54, SetTo, a),
    preserved = False
)

SaveMap('outputmap/grptest.scx', k)
