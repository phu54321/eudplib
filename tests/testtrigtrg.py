import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap_trigtrg.scx')

CompressPayload(True)


@EUDFunc
def main():
    if EUDInfLoop():
        RunTrigTrigger()  # 기존 트리거 실행
        EUDDoEvents()
    EUDEndInfLoop()


SaveMap('outputmap/testtrigtrgcall.scx', main)
