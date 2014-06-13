from eudtrg import *

main = NextTrigger()
ret_epd = f_epd.call(0x5993D4)
VTProc(ret_epd.GetVTable(), [
	ret_epd.QueueAssignTo(EPD(0x58A364))
])

Inject('outputmap/basemap.scx', 'outputmap/epdcalc.scx', main)