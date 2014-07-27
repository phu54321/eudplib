from eudtrglib import *

LoadMap('outputmap/basemap/basemap.scx')

main = NextTrigger()
ret_epd = f_epd(0x5993D4)
VTProc(ret_epd.GetVTable(), [
	ret_epd.QueueAssignTo(EPD(0x58A364))
])

SaveMap('outputmap/epdcalc.scx', main)
