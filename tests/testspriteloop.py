# Test for complex map

import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *


LoadMap('outputmap/basemap/creeptest_basemap.scx')
# CompressPayload(True)


@EUDFunc
def main():
    cnt = EUDVariable()
    for ptr, epd in EUDLoopSprite():
        cnt += 1
    f_simpleprint(cnt)

SaveMap('outputmap/testsprites.scx', main)
