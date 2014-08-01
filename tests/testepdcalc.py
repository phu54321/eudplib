import sys, os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')

main = NextTrigger()
ret_epd = f_epd(0x5993D4)
VTProc(ret_epd.GetVTable(), [
	ret_epd.QueueAssignTo(EPD(0x58A364))
])

SaveMap('outputmap/epdcalc.scx', main)
